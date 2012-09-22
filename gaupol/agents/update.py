# -*- coding: utf-8 -*-

# Copyright (C) 2005-2008,2010,2012 Osmo Salomaa
#
# This file is part of Gaupol.
#
# Gaupol is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# Gaupol is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# Gaupol. If not, see <http://www.gnu.org/licenses/>.

"""Updating the application GUI."""

import aeidon
import gaupol
import os
_ = aeidon.i18n._

from gi.repository import Gdk
from gi.repository import GObject


class UpdateAgent(aeidon.Delegate, metaclass=aeidon.Contractual):

    """
    Updating the application GUI.

    :ivar _message_id: A :class:`Gtk.Statusbar` message ID
    :ivar _message_tag: A timeout from :func:`GObject.timeout_add`
    """

    def __init__(self, master):
        """Initialize an :class:`UpdateAgent` object."""
        aeidon.Delegate.__init__(self, master)
        self._message_id = None
        self._message_tag = None

    def _disable_widgets(self):
        """Make widgets insensitive and blank."""
        self.window.set_title("Gaupol")
        self.video_button.gaupol_label.set_text("")
        self.push_message(None)

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
        toolbar = self.uim.get_widget("/ui/main_toolbar")
        style = gaupol.conf.application_window.toolbar_style
        if style == gaupol.toolbar_styles.DEFAULT:
            return toolbar.unset_style()
        toolbar.set_style(style.value)

    @aeidon.deco.export
    def _on_move_tab_left_activate(self, *args):
        """Move the current tab to the left."""
        page = self.get_current_page()
        scroller = page.view.get_parent()
        index = self.pages.index(page)
        self.notebook.reorder_child(scroller, index - 1)

    @aeidon.deco.export
    def _on_move_tab_right_activate(self, *args):
        """Move the current tab to the right."""
        page = self.get_current_page()
        scroller = page.view.get_parent()
        index = self.pages.index(page)
        self.notebook.reorder_child(scroller, index + 1)

    def _on_notebook_page_reordered_ensure(self, value, *args, **kwargs):
        for i, page in enumerate(self.pages):
            ith_page = self.notebook.get_nth_page(i)
            assert ith_page.get_child() == page.view

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
        menu = self.uim.get_widget("/ui/view_popup")
        menu.popup(parent_menu_shell=None,
                   parent_menu_item=None,
                   func=None,
                   data=None,
                   button=event.button,
                   activate_time=event.time)

        return True

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

    def _update_actions(self, page):
        """Update sensitivities of all actions for page."""
        for name in ("main-safe", "main-unsafe"):
            action_group = self.get_action_group(name)
            for action in action_group.list_actions():
                action.update_sensitivity(self, page)

    def _update_revert(self, page):
        """Update tooltips for undo and redo actions."""
        if page is None: return
        if page.project.can_undo():
            action = self.get_action("undo_action")
            action.props.tooltip = _('Undo "{}"').format(
                page.project.undoables[0].description)
        if page.project.can_redo():
            action = self.get_action("redo_action")
            action.props.tooltip = _('Redo "{}"').format(
                page.project.redoables[0].description)

    def _update_widgets(self, page):
        """Update states of all widgets for `page`."""
        if page is None: return self._disable_widgets()
        self.window.set_title(page.tab_label.get_text())
        self.get_mode_action(page.edit_mode).set_active(True)
        self.get_framerate_action(page.project.framerate).set_active(True)
        self.framerate_combo.set_active(page.project.framerate)
        for field in gaupol.fields:
            col = getattr(page.view.columns, field.name)
            visible = page.view.get_column(col).props.visible
            self.get_column_action(field).set_active(visible)
        video = os.path.basename(page.project.video_path or "")
        self.video_button.gaupol_label.set_text(video)
        self.video_button.set_has_tooltip(bool(video))
        self.video_button.set_tooltip_text(video)

    @aeidon.deco.export
    def flash_message(self, message):
        """Show `message` in statusbar for a short while."""
        self.push_message(message)
        self._message_tag = gaupol.util.delay_add(6000,
                                                  self.push_message,
                                                  None)

    @aeidon.deco.export
    def push_message(self, message):
        """
        Show `message` in the statusbar until explicitly cleared.

        Use ``None`` or a blank string as `message` to clear any possible
        existing message in the statusbar.
        """
        if self._message_tag is not None:
            GObject.source_remove(self._message_tag)
        if self._message_id is not None:
            self.statusbar.remove(0, self._message_id)
        message = message or ""
        self.statusbar.set_tooltip_text(message)
        self._message_id = self.statusbar.push(0, message)

    @aeidon.deco.export
    def update_gui(self):
        """Update widget sensitivities and states for the current page."""
        page = self.get_current_page()
        self._update_actions(page)
        self._update_widgets(page)
        self._update_revert(page)
        self.extension_manager.update_extensions(page)
