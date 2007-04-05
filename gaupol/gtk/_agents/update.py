# Copyright (C) 2005-2007 Osmo Salomaa
#
# This file is part of Gaupol.
#
# Gaupol is free software; you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.
#
# Gaupol is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# Gaupol; if not, write to the Free Software Foundation, Inc., 51 Franklin
# Street, Fifth Floor, Boston, MA 02110-1301, USA.


"""Updating the application GUI."""


import gobject
import gtk
import os
from gettext import gettext as _

from gaupol.base import Delegate
from gaupol.gtk import conf, const, util
from gaupol.gtk._actions import *
from gaupol.gtk._actions import ACTIONS


class UpdateAgent(Delegate):

    """Updating the application GUI.

    Instance attributes:

        _message_id:  Statusbar message ID
        _message_tag: Statusbar GObject timeout tag
    """

    # pylint: disable-msg=E0203,W0201

    def __init__(self, master):

        Delegate.__init__(self, master)

        self._message_id  = None
        self._message_tag = None

    def _update_actions(self, page):
        """Update sensitivities of all UI manager actions for page."""

        for name in ACTIONS:
            cls = eval(name)
            doable = cls.is_doable(self, page)
            for path in cls.paths:
                self.uim.get_action(path).set_sensitive(doable)
            for widget in cls.widgets:
                getattr(self, widget).set_sensitive(doable)

    def _update_revert(self, page):
        """Update tooltips for undo and redo."""

        if page is not None and page.project.can_undo():
            tip = _('Undo "%s"') % page.project.undoables[0].description
            self.undo_button.set_tooltip(self.tooltips, tip)
            self.uim.get_action("/ui/menubar/edit/undo").props.tooltip = tip
        if page is not None and page.project.can_redo():
            tip = _('Redo "%s"') % page.project.redoables[0].description
            self.redo_button.set_tooltip(self.tooltips, tip)
            self.uim.get_action("/ui/menubar/edit/redo").props.tooltip = tip

    def _update_widgets(self, page):
        """Update the states of widgets."""

        if page is None:
            self.tooltips.disable()
            self.window.set_title("Gaupol")
            self.video_button.get_data("label").set_text("")
            self.push_message(None)
            return
        self.tooltips.enable()
        self.window.set_title(page.tab_label.get_text())
        self.uim.get_action(page.edit_mode.uim_path).set_active(True)
        path = const.FRAMERATE.uim_paths[page.project.framerate]
        self.uim.get_action(path).set_active(True)
        self.framerate_combo.set_active(page.project.framerate)
        for i, path in enumerate(const.COLUMN.uim_paths):
            visible = page.view.get_column(i).props.visible
            self.uim.get_action(path).set_active(visible)
        if page.project.video_path is not None:
            basename = os.path.basename(page.project.video_path)
            self.video_button.get_data("label").set_text(basename)
        else:
            self.video_button.get_data("label").set_text("")
        self.tooltips.set_tip(self.video_button, page.project.video_path)

    def on_activate_next_project_activate(self, *args):
        """Activate the project in the next tab."""

        self.notebook.next_page()

    def on_activate_previous_project_activate(self, *args):
        """Activate the project in the previous tab."""

        self.notebook.prev_page()

    def on_conf_application_window_notify_toolbar_style(self, *args):
        """Change the style of the main toolbar."""

        toolbar = self.uim.get_widget("/ui/main_toolbar")
        style = conf.application_window.toolbar_style
        if style == const.TOOLBAR_STYLE.DEFAULT:
            return toolbar.unset_style()
        toolbar.set_style(style.value)

    def on_move_tab_left_activate(self, *args):
        """Move the current tab to the left."""

        page = self.get_current_page()
        scroller = page.view.get_parent()
        index = self.pages.index(page)
        self.notebook.reorder_child(scroller, index - 1)

    def on_move_tab_right_activate(self, *args):
        """Move the current tab to the right."""

        page = self.get_current_page()
        scroller = page.view.get_parent()
        index = self.pages.index(page)
        self.notebook.reorder_child(scroller, index + 1)

    def on_notebook_page_reordered(self, notebook, scroller, index):
        """Update the list of pages to match the new order."""

        view = scroller.get_child()
        for page in self.pages:
            if page.view == view:
                break
        # pylint: disable-msg=W0631
        self.pages.remove(page)
        self.pages.insert(index, page)
        self.update_gui()
        self.emit("pages-reordered", page, index)

    @util.silent(AssertionError)
    def on_notebook_switch_page(self, notebook, pointer, index):
        """Update GUI for the page switched to."""

        assert self.pages
        page = self.pages[index]
        self.update_gui()
        page.view.grab_focus()

    def on_view_button_press_event(self, view, event):
        """Display a pop-up menu to edit data."""

        if event.button != 3:
            return False
        x = int(event.x)
        y = int(event.y)
        value = view.get_path_at_pos(x, y)
        if value is None:
            return False
        path, column, x, y = value
        if path[0] not in view.get_selected_rows():
            view.set_cursor(path[0], column)
            view.update_headers()
        menu = self.uim.get_widget("/ui/view_popup")
        menu.popup(None, None, None, event.button, event.time)
        return True

    def on_view_move_cursor(self, *args):
        """Update GUI after moving cursor in the view."""

        self.update_gui()

    def on_view_selection_changed(self, *args):
        """Update GUI after changing selection in the view."""

        self.update_gui()

    def on_window_window_state_event(self, window, event):
        """Save window maximization."""

        state = event.new_window_state
        maximized = bool(state & gtk.gdk.WINDOW_STATE_MAXIMIZED)
        conf.application_window.maximized = maximized

    def push_message(self, message, clear=True):
        """Push message to the statusbar."""

        if self._message_tag is not None:
            gobject.source_remove(self._message_tag)
        if self._message_id is not None:
            self.statusbar.remove(0, self._message_id)
        event_box = util.get_event_box(self.statusbar)
        self.tooltips.set_tip(event_box, message)
        if message is not None:
            self._message_id = self.statusbar.push(0, message)
            if clear:
                method = self.push_message
                self._message_tag = gobject.timeout_add(6000, method, None)
        return False

    def update_gui(self):
        """Update widget sensitivities and states for the current page."""

        page = self.get_current_page()
        self._update_actions(page)
        self._update_widgets(page)
        self._update_revert(page)
