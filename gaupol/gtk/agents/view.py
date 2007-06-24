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


import gaupol.gtk


class ViewAgent(gaupol.Delegate):

    """Changing the visual appearance of the application and its documents."""

    # pylint: disable-msg=E0203,W0201

    @gaupol.gtk.util.asserted_return
    def _toggle_column(self, col):
        """Show or hide column."""

        page = self.get_current_page()
        column = page.view.get_column(col)
        visible = column.get_visible()
        active = self.get_action(col.action).get_active()
        assert visible is not active
        gaupol.gtk.util.set_cursor_busy(self.window)
        column.set_visible(not visible)
        visible_columns = []
        for col in gaupol.gtk.COLUMN.members:
            if page.view.get_column(col).get_visible():
                visible_columns.append(col)
        gaupol.gtk.conf.editor.visible_columns = visible_columns
        self.update_gui()
        gaupol.gtk.util.set_cursor_normal(self.window)

    @gaupol.gtk.util.asserted_return
    def on_framerate_combo_changed(self, *args):
        """Change the framerate with which unnative units are calculated."""

        page = self.get_current_page()
        index = self.framerate_combo.get_active()
        framerate = gaupol.gtk.FRAMERATE.members[index]
        assert framerate != page.project.framerate
        gaupol.gtk.util.set_cursor_busy(self.window)
        page.project.set_framerate(framerate)
        gaupol.gtk.conf.editor.framerate = framerate
        self.get_menu_item(framerate.action).set_active(True)
        if page.edit_mode != page.project.main_file.mode:
            rows = range(len(page.project.subtitles))
            COLUMN = gaupol.gtk.COLUMN
            cols = (COLUMN.START, COLUMN.END, COLUMN.DURATION)
            page.reload_view(rows, cols)
        gaupol.gtk.util.set_cursor_normal(self.window)

    def on_output_window_notify_visible(self, *args):
        """Sync menu item to the output window's visibility."""

        action = self.get_action("toggle_output_window")
        action.set_active(self.output_window.props.visible)

    @gaupol.gtk.util.asserted_return
    def on_show_framerate_24_changed(self, item, active_item):
        """Change the framerate with which unnative units are calculated."""

        page = self.get_current_page()
        name = active_item.get_name()
        index = gaupol.gtk.FRAMERATE.actions.index(name)
        framerate = gaupol.gtk.FRAMERATE.members[index]
        assert framerate != page.project.framerate
        gaupol.gtk.util.set_cursor_busy(self.window)
        page.project.set_framerate(framerate)
        gaupol.gtk.conf.editor.framerate = framerate
        self.framerate_combo.set_active(framerate)
        if page.edit_mode != page.project.main_file.mode:
            rows = range(len(page.project.subtitles))
            COLUMN = gaupol.gtk.COLUMN
            cols = (COLUMN.START, COLUMN.END, COLUMN.DURATION)
            page.reload_view(rows, cols)
        gaupol.gtk.util.set_cursor_normal(self.window)

    @gaupol.gtk.util.asserted_return
    def on_show_times_changed(self, item, active_item):
        """Change the units in which postions are shown."""

        page = self.get_current_page()
        name = active_item.get_name()
        index = gaupol.gtk.MODE.actions.index(name)
        edit_mode = gaupol.gtk.MODE.members[index]
        assert edit_mode != page.edit_mode
        gaupol.gtk.util.set_cursor_busy(self.window)
        page.edit_mode = edit_mode
        gaupol.gtk.conf.editor.mode = edit_mode
        has_focus = page.view.props.has_focus
        focus_row, focus_col = page.view.get_focus()
        selected_rows = page.view.get_selected_rows()
        scroller = page.view.get_parent()
        scroller.remove(page.view)
        page.view = gaupol.gtk.View(edit_mode)
        self.connect_to_view_signals(page.view)
        scroller.add(page.view)
        scroller.show_all()
        page.reload_view_all()
        if focus_row is not None:
            page.view.set_focus(focus_row, focus_col)
            page.view.scroll_to_row(focus_row)
        page.view.select_rows(selected_rows)
        page.view.props.has_focus = has_focus
        gaupol.gtk.util.set_cursor_normal(self.window)

    def on_toggle_duration_column_toggled(self, *args):
        """Show or hide the 'Duration' column."""

        self._toggle_column(gaupol.gtk.COLUMN.DURATION)

    def on_toggle_end_column_toggled(self, *args):
        """Show or hide the 'End' column."""

        self._toggle_column(gaupol.gtk.COLUMN.END)

    def on_toggle_main_text_column_toggled(self, *args):
        """Show or hide the 'Main Text' column."""

        self._toggle_column(gaupol.gtk.COLUMN.MAIN_TEXT)

    def on_toggle_main_toolbar_toggled(self, *args):
        """Show or hide the main toolbar."""

        toolbar = self.uim.get_widget("/ui/main_toolbar")
        visible = toolbar.props.visible
        toolbar.props.visible = not visible
        gaupol.gtk.conf.application_window.show_main_toolbar = not visible

    def on_toggle_number_column_toggled(self, *args):
        """Show or hide the 'No.' column."""

        self._toggle_column(gaupol.gtk.COLUMN.NUMBER)

    @gaupol.gtk.util.asserted_return
    def on_toggle_output_window_toggled(self, *args):
        """Show or hide the output window."""

        visible = self.output_window.props.visible
        action = self.get_action("toggle_output_window")
        active = action.get_active()
        assert visible is not active
        if self.output_window.props.visible:
            return self.output_window.hide()
        self.output_window.show()

    def on_toggle_start_column_toggled(self, *args):
        """Show or hide the 'Start' column."""

        self._toggle_column(gaupol.gtk.COLUMN.START)

    def on_toggle_statusbar_toggled(self, *args):
        """Show or hide the statusbar."""

        visible = self.statusbar.props.visible
        self.statusbar.props.visible = not visible
        gaupol.gtk.conf.application_window.show_statusbar = not visible

    def on_toggle_translation_text_column_toggled(self, *args):
        """Show or hide the 'Translation Text' column."""

        self._toggle_column(gaupol.gtk.COLUMN.TRAN_TEXT)

    def on_toggle_video_toolbar_toggled(self, *args):
        """Show or hide the video toolbar."""

        visible = self.video_toolbar.props.visible
        self.video_toolbar.props.visible = not visible
        gaupol.gtk.conf.application_window.show_video_toolbar = not visible

    @gaupol.gtk.util.asserted_return
    def on_view_header_button_press_event(self, button, event):
        """Display a column visibility pop-up menu."""

        assert event.button == 3
        menu = self.uim.get_widget("/ui/view_header_popup")
        menu.popup(None, None, None, event.button, event.time)
