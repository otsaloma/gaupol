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


"""Changing the visual appearance of the application and its documents."""


from gaupol.base import Delegate
from gaupol.gtk import conf, cons, util
from gaupol.gtk.index import *
from gaupol.gtk.view import View


class ViewAgent(Delegate):

    """Changing the visual appearance of the application and its documents."""

    # pylint: disable-msg=E0203,W0201

    @util.silent(AssertionError)
    def _toggle_column(self, col):
        """Show or hide column."""

        page = self.get_current_page()
        column = page.view.get_column(col)
        visible = column.get_visible()
        active = self.uim.get_action(col.uim_path).get_active()
        assert visible is not active
        util.set_cursor_busy(self.window)
        column.set_visible(not visible)
        visible_columns = []
        for col in cons.COLUMN.members:
            if page.view.get_column(col).get_visible():
                visible_columns.append(col)
        conf.editor.visible_cols = visible_columns
        self.update_gui()
        util.set_cursor_normal(self.window)

    @util.silent(AssertionError)
    def on_framerate_combo_changed(self, *args):
        """Change the framerate with which unnative units are calculated."""

        page = self.get_current_page()
        index = self.framerate_combo.get_active()
        framerate = cons.FRAMERATE.members[index]
        assert framerate != page.project.framerate
        util.set_cursor_busy(self.window)
        page.project.change_framerate(framerate)
        conf.editor.framerate = framerate
        self.uim.get_widget(framerate.uim_path).set_active(True)
        if page.edit_mode != page.project.main_file.mode:
            rows = range(len(page.project.times))
            page.reload_view(rows, [SHOW, HIDE, DURN])
        util.set_cursor_normal(self.window)

    def on_output_window_notify_visible(self, *args):
        """Sync the menu item to the output window's visibility."""

        action = self.uim.get_action("/ui/menubar/view/output_window")
        action.set_active(self.output_window.props.visible)

    @util.silent(AssertionError)
    def on_show_framerate_23_976_activate(self, item, active_item):
        """Change the framerate with which unnative units are calculated."""

        page = self.get_current_page()
        name = active_item.get_name()
        index = cons.FRAMERATE.uim_action_names.index(name)
        framerate = cons.FRAMERATE.members[index]
        assert framerate != page.project.framerate
        util.set_cursor_busy(self.window)
        page.project.change_framerate(framerate)
        conf.editor.framerate = framerate
        self.framerate_combo.set_active(framerate)
        if page.edit_mode != page.project.main_file.mode:
            rows = range(len(page.project.times))
            page.reload_view(rows, [SHOW, HIDE, DURN])
        util.set_cursor_normal(self.window)

    @util.gc_collected
    @util.silent(AssertionError)
    def on_show_times_activate(self, item, active_item):
        """Change the units in which postions are shown."""

        page = self.get_current_page()
        name = active_item.get_name()
        index = cons.MODE.uim_action_names.index(name)
        edit_mode = cons.MODE.members[index]
        assert edit_mode != page.edit_mode
        util.set_cursor_busy(self.window)
        page.edit_mode = edit_mode
        conf.editor.mode = edit_mode
        has_focus = page.view.props.has_focus
        focus_row, focus_col = page.view.get_focus()
        selected_rows = page.view.get_selected_rows()
        scroller = page.view.get_parent()
        scroller.remove(page.view)
        page.view = View(edit_mode)
        self.connect_to_view_signals(page.view)
        scroller.add(page.view)
        scroller.show_all()
        page.reload_view_all()
        if not None in (focus_row, focus_col):
            page.view.set_focus(focus_row, focus_col)
        page.view.select_rows(selected_rows)
        if focus_row is not None:
            page.view.scroll_to_row(focus_row)
        page.view.props.has_focus = has_focus
        util.set_cursor_normal(self.window)

    def on_toggle_duration_column_activate(self, *args):
        """Show or hide the 'Duration' column."""

        self._toggle_column(cons.COLUMN.DURN)

    def on_toggle_hide_column_activate(self, *args):
        """Show or hide the 'Hide' column."""

        self._toggle_column(cons.COLUMN.HIDE)

    def on_toggle_main_text_column_activate(self, *args):
        """Show or hide the 'Main Text' column."""

        self._toggle_column(cons.COLUMN.MTXT)

    def on_toggle_main_toolbar_activate(self, *args):
        """Show or hide the main toolbar."""

        toolbar = self.uim.get_widget("/ui/main_toolbar")
        visible = toolbar.props.visible
        toolbar.props.visible = not visible
        conf.application_window.show_main_toolbar = not visible

    def on_toggle_number_column_activate(self, *args):
        """Show or hide the 'No.' column."""

        self._toggle_column(cons.COLUMN.NO)

    def on_toggle_output_window_activate(self, *args):
        """Show or hide the output window."""

        visible = self.output_window.props.visible
        action = self.uim.get_action("/ui/menubar/view/output_window")
        active = action.get_active()
        if visible is not active:
            if self.output_window.props.visible:
                return self.output_window.hide()
            self.output_window.show()

    def on_toggle_show_column_activate(self, *args):
        """Show or hide the 'Show' column."""

        self._toggle_column(cons.COLUMN.SHOW)

    def on_toggle_statusbar_activate(self, *args):
        """Show or hide the statusbar."""

        visible = self.statusbar.props.visible
        self.statusbar.props.visible = not visible
        conf.application_window.show_statusbar = not visible

    def on_toggle_translation_text_column_activate(self, *args):
        """Show or hide the 'Translation Text' column."""

        self._toggle_column(cons.COLUMN.TTXT)

    def on_toggle_video_toolbar_activate(self, *args):
        """Show or hide the video toolbar."""

        visible = self.video_toolbar.props.visible
        self.video_toolbar.props.visible = not visible
        conf.application_window.show_video_toolbar = not visible

    @util.silent(AssertionError)
    def on_view_header_button_press_event(self, button, event):
        """Display a column visibility pop-up menu."""

        assert event.button == 3
        menu = self.uim.get_widget("/ui/view_header_popup")
        menu.popup(None, None, None, event.button, event.time)
