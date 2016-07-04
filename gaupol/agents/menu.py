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
import sys

from gi.repository import Gtk


class MenuAgent(aeidon.Delegate):

    """Building and updating dynamic menus."""

    def __init__(self, master):
        """Initialize a :class:`MenuAgent` instance."""
        aeidon.Delegate.__init__(self, master)
        self._columns_popup = None
        self._redo_menu_items = []
        self._tab_popup = None
        self._undo_menu_items = []
        self._view_popup = None
        self._init_signal_handlers()

    @aeidon.deco.once
    def _get_recent_chooser_menu(self):
        """Return a new recent chooser menu."""
        menu = Gtk.RecentChooserMenu()
        menu.set_show_icons(sys.platform != "win32")
        menu.set_show_not_found(False)
        menu.set_show_numbers(False)
        menu.set_show_tips(True)
        menu.set_sort_type(Gtk.RecentSortType.MRU)
        menu.connect("item-activated", self._on_recent_menu_item_activated)
        recent_filter = Gtk.RecentFilter()
        recent_filter.add_application("gaupol")
        menu.add_filter(recent_filter)
        menu.set_filter(recent_filter)
        menu.set_limit(10)
        return menu

    def _init_signal_handlers(self):
        """Initialize signal handlers."""
        self.connect("page-added", self._update_projects_menu)
        self.connect("page-closed", self._update_projects_menu)
        self.connect("page-saved", self._update_projects_menu)
        self.connect("page-switched", self._update_projects_menu)
        self.connect("pages-reordered", self._update_projects_menu)
        self.connect("page-added", self._update_recent_menus)
        self.connect("page-saved", self._update_recent_menus)

    @aeidon.deco.export
    def _on_activate_project_activate(self, action, parameter):
        """Activate the requested page."""
        index = int(parameter.get_string())
        self.set_current_page(self.pages[index])

    @aeidon.deco.export
    def _on_open_button_show_menu(self, *args):
        """Show a menu listing recent files to open."""
        menu = self._get_recent_chooser_menu()
        if self.open_button.get_menu():
            self.open_button.get_menu().detach()
        self.open_button.set_menu(menu)

    @aeidon.deco.export
    def _on_open_recent_main_file_activate(self, action, *args):
        """Open recent file as main document."""
        self.open_main(action.gaupol_path)

    def _on_recent_menu_item_activated(self, chooser, *args):
        """Open recent file as main document."""
        uri = chooser.get_current_uri()
        path = aeidon.util.uri_to_path(uri)
        self.open_button.get_menu().hide()
        self.open_main(path)

    @aeidon.deco.export
    def _on_open_recent_translation_file_activate(self, action, *args):
        """Open recent file as translation document."""
        self.open_translation(action.gaupol_path)

    @aeidon.deco.export
    def _on_redo_button_show_menu(self, *args):
        """Show a menu listing all redoable actions."""
        menu = Gtk.Menu()
        self._redo_menu_items = []
        page = self.get_current_page()
        for i, action in enumerate(page.project.redoables):
            item = Gtk.MenuItem(label=action.description)
            item.gaupol_index = i
            item.connect("activate", self._on_redo_menu_item_activate)
            item.connect("enter-notify-event", self._on_redo_menu_item_enter_notify_event)
            item.connect("leave-notify-event", self._on_redo_menu_item_leave_notify_event)
            self._redo_menu_items.append(item)
            menu.append(item)
        menu.show_all()
        if self.redo_button.get_menu():
            self.redo_button.get_menu().detach()
        self.redo_button.set_menu(menu)

    def _on_redo_menu_item_activate(self, menu_item):
        """Redo the selected action and all those above it."""
        self.redo(menu_item.gaupol_index + 1)
        self.redo_button.get_menu().hide()

    def _on_redo_menu_item_enter_notify_event(self, menu_item, event):
        """Select all actions above `menu_item`."""
        index = menu_item.gaupol_index
        for item in self._redo_menu_items[:index]:
            item.set_state(Gtk.StateType.PRELIGHT)

    def _on_redo_menu_item_leave_notify_event(self, menu_item, event):
        """Unselect all actions above `menu_item`."""
        index = menu_item.gaupol_index
        for item in self._redo_menu_items[:index]:
            item.set_state(Gtk.StateType.NORMAL)

    @aeidon.deco.export
    def _on_tab_widget_button_press_event(self, button, event, page):
        """Display a pop-up menu with tab-related actions."""
        if event.button != 3: return
        if self._tab_popup is None:
            path = os.path.join(aeidon.DATA_DIR, "ui", "tab-popup.ui")
            builder = Gtk.Builder.new_from_file(path)
            self._tab_popup = builder.get_object("tab-popup")
        menu = Gtk.Menu.new_from_model(self._tab_popup)
        menu.attach_to_widget(self.notebook, None)
        menu.popup(parent_menu_shell=None,
                   parent_menu_item=None,
                   func=None,
                   data=None,
                   button=event.button,
                   activate_time=event.time)

        return True

    @aeidon.deco.export
    def _on_undo_button_show_menu(self, *args):
        """Show a menu listing all undoable actions."""
        menu = Gtk.Menu()
        self._undo_menu_items = []
        page = self.get_current_page()
        for i, action in enumerate(page.project.undoables):
            item = Gtk.MenuItem(label=action.description)
            item.gaupol_index = i
            item.connect("activate", self._on_undo_menu_item_activate)
            item.connect("enter-notify-event", self._on_undo_menu_item_enter_notify_event)
            item.connect("leave-notify-event", self._on_undo_menu_item_leave_notify_event)
            self._undo_menu_items.append(item)
            menu.append(item)
        menu.show_all()
        if self.undo_button.get_menu():
            self.undo_button.get_menu().detach()
        self.undo_button.set_menu(menu)

    def _on_undo_menu_item_activate(self, menu_item):
        """Undo the selected action and all those above it."""
        self.undo(menu_item.gaupol_index + 1)
        self.undo_button.get_menu().hide()

    def _on_undo_menu_item_enter_notify_event(self, menu_item, event):
        """Select all actions above `menu_item`."""
        index = menu_item.gaupol_index
        for item in self._undo_menu_items[:index]:
            item.set_state(Gtk.StateType.PRELIGHT)

    def _on_undo_menu_item_leave_notify_event(self, menu_item, event):
        """Unselect all actions above `menu_item`."""
        index = menu_item.gaupol_index
        for item in self._undo_menu_items[:index]:
            item.set_state(Gtk.StateType.NORMAL)

    @aeidon.deco.export
    def _on_view_button_press_event(self, view, event):
        """Display a right-click pop-up menu to edit data."""
        if event.button != 3: return
        x = int(event.x)
        y = int(event.y)
        value = view.get_path_at_pos(x, y)
        if value is None: return
        path, column, x, y = value
        row = gaupol.util.tree_path_to_row(path)
        if not row in view.get_selected_rows():
            view.set_cursor(path, column)
            view.update_headers()
        if self._view_popup is None:
            path = os.path.join(aeidon.DATA_DIR, "ui", "view-popup.ui")
            builder = Gtk.Builder.new_from_file(path)
            self._view_popup = builder.get_object("view-popup")
        menu = Gtk.Menu.new_from_model(self._view_popup)
        menu.attach_to_widget(view, None)
        menu.popup(parent_menu_shell=None,
                   parent_menu_item=None,
                   func=None,
                   data=None,
                   button=event.button,
                   activate_time=event.time)

        return True

    @aeidon.deco.export
    def _on_view_header_button_press_event(self, button, event):
        """Display a column visibility pop-up menu."""
        if event.button != 3: return
        if self._columns_popup is None:
            path = os.path.join(aeidon.DATA_DIR, "ui", "columns-popup.ui")
            builder = Gtk.Builder.new_from_file(path)
            self._columns_popup = builder.get_object("columns-popup")
        menu = Gtk.Menu.new_from_model(self._columns_popup)
        menu.attach_to_widget(self.get_current_page().view, None)
        menu.popup(parent_menu_shell=None,
                   parent_menu_item=None,
                   func=None,
                   data=None,
                   button=event.button,
                   activate_time=event.time)

        return True

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
        recent = self._get_recent_chooser_menu()
        for i, uri in enumerate(recent.get_uris()):
            path = aeidon.util.uri_to_path(uri)
            label = os.path.basename(path)
            if len(label) > 100:
                label = label[:100] + "…"
            action = "win.open-recent-main-file-{:d}".format(i)
            menu.append(label, action)
            action = action.replace("win.", "")
            if not self.get_action(action):
                ao = gaupol.Action(action)
                callback = self._on_open_recent_main_file_activate
                ao.connect("activate", callback)
                self.window.add_action(ao)
            self.get_action(action).gaupol_path = path

    def _update_recent_menus(self, *args):
        """Update the file menu lists of recent files."""
        self._update_recent_main_menu()
        self._update_recent_translation_menu()

    def _update_recent_translation_menu(self, *args):
        """Update the file menu list of recent translation files."""
        menu = self.get_menubar_section("open-recent-translation-placeholder")
        # Menubar not available when running unit tests.
        if menu is None: return
        menu.remove_all()
        recent = self._get_recent_chooser_menu()
        for i, uri in enumerate(recent.get_uris()):
            path = aeidon.util.uri_to_path(uri)
            label = os.path.basename(path)
            if len(label) > 100:
                label = label[:100] + "…"
            action = "win.open-recent-translation-file-{:d}".format(i)
            menu.append(label, action)
            action = action.replace("win.", "")
            if not self.get_action(action):
                ao = gaupol.Action(action)
                callback = self._on_open_recent_translation_file_activate
                ao.connect("activate", callback)
                self.window.add_action(ao)
            self.get_action(action).gaupol_path = path
