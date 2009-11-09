# Copyright (C) 2005-2008 Osmo Salomaa
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

import gaupol.gtk
import gobject
import gtk
import os
_ = gaupol.i18n._


class UpdateAgent(gaupol.Delegate):

    """Updating the application GUI.

    Instance attribute '_message_id' stores the statusbar message ID as
    returned by 'statusbar.push' and '_message_tag' the statusbar message
    timeout tag as returned by 'gobject.timeout_add'.
    """

    __metaclass__ = gaupol.Contractual

    def __init__(self, master):
        """Initialize an UpdateAgent object."""

        gaupol.Delegate.__init__(self, master)
        self._message_id = None
        self._message_tag = None

    def _disable_widgets(self):
        """Make widgets insensitive and blank."""

        self.window.set_title("Gaupol")
        self.video_button.get_data("label").set_text("")
        self.push_message(None)

    def _update_actions(self, page):
        """Update sensitivities of all UI manager actions for page."""

        action_group = self.get_action_group("main-safe")
        for action in action_group.list_actions():
            action.update_sensitivity(self, page)
        action_group = self.get_action_group("main-unsafe")
        for action in action_group.list_actions():
            action.update_sensitivity(self, page)

    def _update_revert(self, page):
        """Update tooltips for undo and redo."""

        if page is None: return
        if page.project.can_undo():
            description = page.project.undoables[0].description
            tooltip = _('Undo "%s"') % description
            self.get_action("undo_action").props.tooltip = tooltip
        if page.project.can_redo():
            description = page.project.redoables[0].description
            tooltip = _('Redo "%s"') % description
            self.get_action("redo_action").props.tooltip = tooltip

    def _update_widgets(self, page):
        """Update the states of widgets."""

        if page is None: return self._disable_widgets()
        self.window.set_title(page.tab_label.get_text())
        self.get_mode_action(page.edit_mode).set_active(True)
        self.get_framerate_action(page.project.framerate).set_active(True)
        self.framerate_combo.set_active(page.project.framerate)
        for field in gaupol.gtk.fields:
            col = getattr(page.view.columns, field.name)
            visible = page.view.get_column(col).props.visible
            self.get_column_action(field).set_active(visible)
        video = os.path.basename(page.project.video_path or "")
        self.video_button.get_data("label").set_text(video)
        self.video_button.set_tooltip_text(video or None)

    def flash_message(self, message):
        """Show message in the statusbar for a short while."""

        self.push_message(message)
        push = self.push_message
        self._message_tag = gaupol.gtk.util.delay_add(6000, push, None)

    def on_activate_next_project_activate(self, *args):
        """Activate the project in the next tab."""

        self.notebook.next_page()

    def on_activate_previous_project_activate(self, *args):
        """Activate the project in the previous tab."""

        self.notebook.prev_page()

    def on_conf_application_window_notify_toolbar_style(self, *args):
        """Change the style of the main toolbar."""

        toolbar = self.uim.get_widget("/ui/main_toolbar")
        style = gaupol.gtk.conf.application_window.toolbar_style
        if style == gaupol.gtk.toolbar_styles.DEFAULT:
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

    def on_notebook_page_reordered_ensure(self, value, *args, **kwargs):
        for i, page in enumerate(self.pages):
            ith_page = self.notebook.get_nth_page(i)
            assert ith_page.get_child() == page.view

    def on_notebook_page_reordered(self, notebook, scroller, index):
        """Update the list of pages to match the new order."""

        view = scroller.get_child()
        page = [x for x in self.pages if x.view is view][0]
        self.pages.remove(page)
        self.pages.insert(index, page)
        self.update_gui()
        self.emit("pages-reordered", page, index)

    def on_notebook_switch_page(self, notebook, pointer, index):
        """Update GUI for the page switched to."""

        if not self.pages: return
        page = self.pages[index]
        self.update_gui()
        page.view.grab_focus()
        self.emit("page-switched", page)

    def on_view_button_press_event(self, view, event):
        """Display a right-click pop-up menu to edit data."""

        if event.button != 3: return
        x = int(event.x)
        y = int(event.y)
        value = view.get_path_at_pos(x, y)
        if value is None: return
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
        gaupol.gtk.conf.application_window.maximized = maximized

    def push_message(self, message):
        """Show message in the statusbar."""

        if self._message_tag is not None:
            gobject.source_remove(self._message_tag)
        if self._message_id is not None:
            self.statusbar.remove_message(0, self._message_id)
        event_box = self.statusbar.get_ancestor(gtk.EventBox)
        self.statusbar.set_tooltip_text(message)
        if message is not None:
            self._message_id = self.statusbar.push(0, message)

    def update_gui(self):
        """Update widget sensitivities and states for the current page."""

        page = self.get_current_page()
        self.extension_manager.update_extensions(page)
        self._update_actions(page)
        self._update_widgets(page)
        self._update_revert(page)
