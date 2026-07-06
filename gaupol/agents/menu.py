# -*- coding: utf-8 -*-

# Copyright (C) 2005 Osmo Salomaa
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""Building and updating dynamic menus."""

import aeidon
import gaupol
import os

from aeidon.i18n   import _
from gi.repository import Gdk
from gi.repository import GLib
from gi.repository import Gtk


class MenuAgent(aeidon.Delegate):

    """Building and updating dynamic menus."""

    def __init__(self, master):
        """Initialize a :class:`MenuAgent` instance."""
        aeidon.Delegate.__init__(self, master)
        self._columns_popup = None
        self._tab_popup = None
        self._view_popup = None
        self._init_signal_handlers()

    def _get_recent_paths(self):
        """Return a list of recently used subtitle file paths."""
        mime_types = [x.mime_type for x in aeidon.formats]
        items = [x for x in self.recent_manager.get_items()
                 if x.has_application("gaupol")
                 and x.get_mime_type() in mime_types]
        if not gaupol.conf.recent.show_not_found:
            # Can be really slow with network drives.
            # https://github.com/otsaloma/gaupol/issues/175
            items = [x for x in items if x.exists()]
        items.sort(key=lambda x: x.get_modified().to_unix(), reverse=True)
        return [aeidon.util.uri_to_path(x.get_uri()) for x in items[:10]]

    def _init_signal_handlers(self):
        """Initialize signal handlers."""
        self.connect("page-added", self._update_projects_menu)
        self.connect("page-closed", self._update_projects_menu)
        self.connect("page-saved", self._update_projects_menu)
        self.connect("page-switched", self._update_projects_menu)
        self.connect("pages-reordered", self._update_projects_menu)
        self.connect("init-done", self._update_recent_menus)
        self.connect("page-added", self._update_recent_menus)
        self.connect("page-saved", self._update_recent_menus)

    @aeidon.deco.export
    def _on_activate_project_activate(self, action, parameter):
        """Activate the requested page."""
        index = int(parameter.get_string())
        self.set_current_page(self.pages[index])

    @aeidon.deco.export
    def _on_open_recent_main_file_activate(self, action, *args):
        """Open recent file as main document."""
        if not os.path.isfile(action.gaupol_path):
            return self.flash_message(_("File not found"))
        self.open_main(action.gaupol_path)

    @aeidon.deco.export
    def _on_open_recent_translation_file_activate(self, action, *args):
        """Open recent file as translation document."""
        if not os.path.isfile(action.gaupol_path):
            return self.flash_message(_("File not found"))
        self.open_translation(action.gaupol_path)

    @aeidon.deco.export
    def _on_tab_widget_pressed(self, gesture, n_press, x, y, page):
        """Display a pop-up menu with tab-related actions."""
        if self._tab_popup is None:
            path = os.path.join(aeidon.DATA_DIR, "ui", "tab-popup.ui")
            builder = Gtk.Builder.new_from_file(path)
            self._tab_popup = builder.get_object("tab-popup")
        self._show_popover_menu(gesture, x, y, self._tab_popup)

    @aeidon.deco.export
    def _on_view_pressed(self, gesture, n_press, x, y):
        """Display a right-click pop-up menu to edit data."""
        view = gesture.get_widget()
        bx, by = view.convert_widget_to_bin_window_coords(int(x), int(y))
        value = view.get_path_at_pos(bx, by)
        if value is None: return
        path, column = value[:2]
        row = gaupol.util.tree_path_to_row(path)
        if not row in view.get_selected_rows():
            view.set_cursor(path, column)
            view.update_headers()
        if self._view_popup is None:
            path = os.path.join(aeidon.DATA_DIR, "ui", "view-popup.ui")
            builder = Gtk.Builder.new_from_file(path)
            self._view_popup = builder.get_object("view-popup")
        self._show_popover_menu(gesture, x, y, self._view_popup)

    @aeidon.deco.export
    def _on_view_header_pressed(self, gesture, n_press, x, y):
        """Display a column visibility pop-up menu."""
        if self._columns_popup is None:
            path = os.path.join(aeidon.DATA_DIR, "ui", "columns-popup.ui")
            builder = Gtk.Builder.new_from_file(path)
            self._columns_popup = builder.get_object("columns-popup")
        self._show_popover_menu(gesture, x, y, self._columns_popup)

    def _show_popover_menu(self, gesture, x, y, model):
        """Show a pop-up menu for `model` at coordinates."""
        gesture.set_state(Gtk.EventSequenceState.CLAIMED)
        menu = Gtk.PopoverMenu.new_from_model(model)
        menu.set_parent(gesture.get_widget())
        rect = Gdk.Rectangle()
        rect.x, rect.y = int(x), int(y)
        rect.width = rect.height = 1
        menu.set_pointing_to(rect)
        menu.set_has_arrow(False)
        menu.connect("closed", lambda menu: GLib.idle_add(menu.unparent))
        menu.popup()

    def _update_projects_menu(self, *args):
        """Update the project menu list of projects."""
        menu = self.get_menubar_section("projects-placeholder")
        # Menubar not available when running unit tests.
        if menu is None: return
        menu.remove_all()
        current = self.get_current_page()
        for i, page in enumerate(self.pages):
            label = page.get_main_basename()
            if len(label) > 100:
                label = label[:100] + "…"
            action = "win.activate-project::{:d}".format(i)
            menu.append(label, action)
            if page is current:
                action = self.get_action("activate-project")
                action.set_state(str(i))

    def _update_recent_main_menu(self, *args):
        """Update the file menu list of recent main files."""
        menu = self.get_menubar_section("open-recent-main-placeholder")
        # Menubar not available when running unit tests.
        if menu is None: return
        menu.remove_all()
        for i, path in enumerate(self._get_recent_paths()):
            label = os.path.basename(path)
            if len(label) > 100:
                label = label[:100] + "…"
            action = "win.open-recent-main-file-{:d}".format(i)
            menu.append(label, action)
            action = action.replace("win.", "")
            if self.get_action(action):
                # If action i exists, update the file path.
                self.get_action(action).gaupol_path = path
            else:
                # Otherwise, create the action and add to self.window.
                # XXX: For some reason, this can sometimes fail.
                with aeidon.util.silent(Exception):
                    ao = gaupol.Action(action)
                    ao.gaupol_path = path
                    callback = self._on_open_recent_main_file_activate
                    ao.connect("activate", callback)
                    self.window.add_action(ao)

    def _update_recent_menus(self, *args):
        """Update the file menu lists of recent files."""
        self._update_recent_main_menu()
        self._update_recent_translation_menu()
        # Update enabled states of added actions.
        self.update_gui()

    def _update_recent_translation_menu(self, *args):
        """Update the file menu list of recent translation files."""
        menu = self.get_menubar_section("open-recent-translation-placeholder")
        # Menubar not available when running unit tests.
        if menu is None: return
        menu.remove_all()
        for i, path in enumerate(self._get_recent_paths()):
            label = os.path.basename(path)
            if len(label) > 100:
                label = label[:100] + "…"
            action = "win.open-recent-translation-file-{:d}".format(i)
            menu.append(label, action)
            action = action.replace("win.", "")
            if not self.get_action(action):
                ao = gaupol.OpenRecentTranslationFileAction(action)
                callback = self._on_open_recent_translation_file_activate
                ao.connect("activate", callback)
                self.window.add_action(ao)
            self.get_action(action).gaupol_path = path
