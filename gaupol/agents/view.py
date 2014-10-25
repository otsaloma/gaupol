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

"""Changing the visual appearance of application and its documents."""

import aeidon
import gaupol


class ViewAgent(aeidon.Delegate):

    """Changing the visual appearance of application and its documents."""

    @aeidon.deco.export
    def _on_output_window_notify_visible(self, output_window, visible):
        """Sync menu item to output window's visibility."""
        action = self.get_action("toggle_output_window")
        action.set_active(output_window.get_visible())

    @aeidon.deco.export
    def _on_show_framerate_23_976_changed(self, item, active_item):
        """Change the framerate with which nonnative units are calculated."""
        page = self.get_current_page()
        framerate = active_item.framerate
        if framerate == page.project.framerate: return
        gaupol.util.set_cursor_busy(self.window)
        page.project.set_framerate(framerate, register=None)
        gaupol.conf.editor.framerate = framerate
        if page.edit_mode != page.project.main_file.mode:
            rows = list(range(len(page.project.subtitles)))
            fields = [x for x in gaupol.fields if x.is_position]
            page.reload_view(rows, fields)
        gaupol.util.set_cursor_normal(self.window)

    @aeidon.deco.export
    def _on_show_times_changed(self, item, active_item):
        """Change the units in which positions are shown."""
        page = self.get_current_page()
        edit_mode = active_item.mode
        if edit_mode == page.edit_mode: return
        gaupol.util.set_cursor_busy(self.window)
        page.edit_mode = edit_mode
        gaupol.conf.editor.mode = edit_mode
        has_focus = page.view.has_focus()
        focus_row, focus_col = page.view.get_focus()
        selected_rows = page.view.get_selected_rows()
        scroller = page.view.get_parent()
        scroller.remove(page.view)
        page.view = gaupol.View(edit_mode)
        self.connect_view_signals(page.view)
        scroller.add(page.view)
        scroller.show_all()
        page.reload_view_all()
        if focus_row is not None:
            page.view.set_focus(focus_row, focus_col)
            page.view.scroll_to_row(focus_row)
        page.view.select_rows(selected_rows)
        page.view.props.has_focus = has_focus
        gaupol.util.set_cursor_normal(self.window)
        page.emit("view-created", page.view)

    @aeidon.deco.export
    def _on_toggle_duration_column_toggled(self, *args):
        """Show or hide the duration column."""
        self._toggle_column(gaupol.fields.DURATION)

    @aeidon.deco.export
    def _on_toggle_end_column_toggled(self, *args):
        """Show or hide the end column."""
        self._toggle_column(gaupol.fields.END)

    @aeidon.deco.export
    def _on_toggle_main_text_column_toggled(self, *args):
        """Show or hide the main text column."""
        self._toggle_column(gaupol.fields.MAIN_TEXT)

    @aeidon.deco.export
    def _on_toggle_main_toolbar_toggled(self, *args):
        """Show or hide the main toolbar."""
        toolbar = self.uim.get_widget("/ui/main_toolbar")
        visible = toolbar.get_visible()
        toolbar.set_visible(not visible)
        gaupol.conf.application_window.show_main_toolbar = not visible

    @aeidon.deco.export
    def _on_toggle_number_column_toggled(self, *args):
        """Show or hide the number column."""
        self._toggle_column(gaupol.fields.NUMBER)

    @aeidon.deco.export
    def _on_toggle_output_window_toggled(self, *args):
        """Show or hide the output window."""
        visible = self.output_window.get_visible()
        action = self.get_action("toggle_output_window")
        active = action.get_active()
        if visible is active: return
        self.output_window.set_visible(not visible)

    @aeidon.deco.export
    def _on_toggle_player_toggled(self, *args):
        """Show or hide the video player."""
        action = self.get_action("toggle_player")
        self.player_box.set_visible(action.get_active())
        self.update_gui()

    @aeidon.deco.export
    def _on_toggle_start_column_toggled(self, *args):
        """Show or hide the start column."""
        self._toggle_column(gaupol.fields.START)

    @aeidon.deco.export
    def _on_toggle_translation_text_column_toggled(self, *args):
        """Show or hide the translation text column."""
        self._toggle_column(gaupol.fields.TRAN_TEXT)

    @aeidon.deco.export
    def _on_view_header_button_press_event(self, button, event):
        """Display a column visibility pop-up menu."""
        if event.button != 3: return
        menu = self.uim.get_widget("/ui/view_header_popup")
        menu.popup(parent_menu_shell=None,
                   parent_menu_item=None,
                   func=None,
                   data=None,
                   button=event.button,
                   activate_time=event.time)

        return True

    def _toggle_column(self, field):
        """Show or hide column corresponding to `field`."""
        page = self.get_current_page()
        col = getattr(page.view.columns, field.name)
        column = page.view.get_column(col)
        visible = column.get_visible()
        active = self.get_column_action(field).get_active()
        if visible is active: return
        gaupol.util.set_cursor_busy(self.window)
        column.set_visible(not visible)
        visible_fields = []
        for field in gaupol.fields:
            col = getattr(page.view.columns, field.name)
            if page.view.get_column(col).get_visible():
                visible_fields.append(field)
        gaupol.conf.editor.visible_fields = visible_fields
        self.update_gui()
        page.view.columns_autosize()
        gaupol.util.set_cursor_normal(self.window)

    @aeidon.deco.export
    def _on_use_horizontal_layout_changed(self, item, active_item):
        """Change how window is split to video and subtitles."""
        orientation = active_item.orientation
        if orientation == gaupol.orientation.HORIZONTAL:
            self.paned.set_orientation(gaupol.orientation.HORIZONTAL)
            self.player_box.orientation = gaupol.orientation.VERTICAL
        if orientation == gaupol.orientation.VERTICAL:
            self.paned.set_orientation(gaupol.orientation.VERTICAL)
            self.player_box.orientation = gaupol.orientation.HORIZONTAL
        gaupol.conf.application_window.layout = orientation
