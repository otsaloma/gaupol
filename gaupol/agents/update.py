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

"""Updating the application GUI."""

import aeidon
import gaupol

from gi.repository import Gdk


class UpdateAgent(aeidon.Delegate):

    """Updating the application GUI."""

    def _disable_widgets(self):
        """Make widgets insensitive and blank."""
        self.window.set_title("Gaupol")
        self.show_message(None)

    @aeidon.deco.export
    def flash_message(self, message, duration=6):
        """Show `message` in statuslabel for `duration` seconds."""
        self.statuslabel.flash_text(message, duration=duration)
        self.statuslabel.register_hide_event(self.window, "button-press-event")
        self.statuslabel.register_hide_event(self.window, "key-press-event")
        self.statuslabel.register_hide_event(self.window, "scroll-event")
        with aeidon.util.silent(AttributeError):
            self.statuslabel.register_hide_event(
                self.get_current_page().view, "button-press-event")

    @aeidon.deco.export
    def _on_activate_next_project_activate(self, *args):
        """Activate the project in the next tab."""
        self.notebook.next_page()

    @aeidon.deco.export
    def _on_activate_previous_project_activate(self, *args):
        """Activate the project in the previous tab."""
        self.notebook.prev_page()

    @aeidon.deco.export
    def _on_conf_application_window_notify_toolbar_style(self, *args):
        """Change the style of the main toolbar."""
        style = gaupol.conf.application_window.toolbar_style
        self.main_toolbar.set_style(style.value)

    @aeidon.deco.export
    def _on_move_tab_left_activate(self, *args):
        """Move the current tab to the left."""
        page = self.get_current_page()
        scroller = page.view.get_parent()
        index = self.pages.index(page)
        self.notebook.reorder_child(scroller, index-1)

    @aeidon.deco.export
    def _on_move_tab_right_activate(self, *args):
        """Move the current tab to the right."""
        page = self.get_current_page()
        scroller = page.view.get_parent()
        index = self.pages.index(page)
        self.notebook.reorder_child(scroller, index + 1)

    @aeidon.deco.export
    def _on_notebook_page_reordered(self, notebook, scroller, index):
        """Update the list of pages to match the new order."""
        view = scroller.get_child()
        page = [x for x in self.pages if x.view is view][0]
        self.pages.remove(page)
        self.pages.insert(index, page)
        self.update_gui()
        self.emit("pages-reordered", page, index)

    @aeidon.deco.export
    def _on_notebook_switch_page(self, notebook, pointer, index):
        """Update GUI for the page switched to."""
        if not self.pages: return
        self.update_gui()
        page = self.pages[index]
        page.view.grab_focus()
        self.emit("page-switched", page)

    @aeidon.deco.export
    def _on_view_move_cursor(self, *args):
        """Update GUI after moving cursor in the view."""
        self.update_gui()

    @aeidon.deco.export
    def _on_view_selection_changed(self, *args):
        """Update GUI after changing selection in the view."""
        self.update_gui()

    @aeidon.deco.export
    def _on_window_window_state_event(self, window, event):
        """Save window maximization."""
        state = event.new_window_state
        maximized = bool(state & Gdk.WindowState.MAXIMIZED)
        gaupol.conf.application_window.maximized = maximized

    @aeidon.deco.export
    def show_message(self, message):
        """Show `message` in the statuslabel or hide label with `None`."""
        self.statuslabel.set_text(message)

    def _update_actions(self, page):
        """Update sensitivities of all actions for page."""
        rows = []
        with aeidon.util.silent(AttributeError):
            rows = page.view.get_selected_rows()
        for name in self.window.list_actions():
            action = self.get_action(name)
            action.update_enabled(self, page, rows)

    @aeidon.deco.export
    def update_gui(self):
        """Update widget sensitivities and states for the current page."""
        page = self.get_current_page()
        self._update_actions(page)
        self._update_widgets(page)
        self.extension_manager.update_extensions(page)

    def _update_widgets(self, page):
        """Update states of all widgets for `page`."""
        if page is None:
            return self._disable_widgets()
        self.window.set_title(page.tab_label.get_text())
        self.notebook.set_menu_label_text(
            page.view.get_parent(), page.tab_label.get_text())
        tabs = len(self.pages) > 1 and not self.player_box.get_visible()
        self.notebook.set_show_tabs(tabs)
        self.get_action("set-edit-mode").set_state(str(page.edit_mode))
        self.get_action("set-framerate").set_state(str(page.project.framerate))
        if self.player is not None:
            layout = gaupol.conf.application_window.layout
            self.get_action("set-layout").set_state(str(layout))
        for field in gaupol.fields:
            col = getattr(page.view.columns, field.name)
            visible = page.view.get_column(col).get_visible()
            self.get_column_action(field).set_state(visible)
