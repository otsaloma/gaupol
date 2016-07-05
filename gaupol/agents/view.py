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
    def _on_set_edit_mode_activate(self, action, parameter):
        """Change the units in which positions are shown."""
        page = self.get_current_page()
        edit_mode = getattr(aeidon.modes, parameter.get_string())
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
        self.update_gui()
        gaupol.util.set_cursor_normal(self.window)
        page.emit("view-created", page.view)

    @aeidon.deco.export
    def _on_set_framerate_activate(self, action, parameter):
        """Change the framerate to use."""
        page = self.get_current_page()
        framerate = getattr(aeidon.framerates, parameter.get_string())
        if framerate == page.project.framerate: return
        gaupol.util.set_cursor_busy(self.window)
        page.project.set_framerate(framerate, register=None)
        gaupol.conf.editor.framerate = framerate
        if page.edit_mode != page.project.main_file.mode:
            rows = list(range(len(page.project.subtitles)))
            fields = [x for x in gaupol.fields if x.is_position]
            page.reload_view(rows, fields)
        self.update_gui()
        gaupol.util.set_cursor_normal(self.window)

    @aeidon.deco.export
    def _on_set_layout_activate(self, action, parameter):
        """Change the application window layout direction to use."""
        orientation = getattr(gaupol.orientation, parameter.get_string())
        if orientation == gaupol.orientation.HORIZONTAL:
            self.paned.set_orientation(gaupol.orientation.HORIZONTAL)
            self.player_box.orientation = gaupol.orientation.VERTICAL
        if orientation == gaupol.orientation.VERTICAL:
            self.paned.set_orientation(gaupol.orientation.VERTICAL)
            self.player_box.orientation = gaupol.orientation.HORIZONTAL
        gaupol.conf.application_window.layout = orientation
        self.update_gui()

    @aeidon.deco.export
    def _on_toggle_duration_column_activate(self, *args):
        """Show or hide the duration column."""
        self._toggle_column(gaupol.fields.DURATION)

    @aeidon.deco.export
    def _on_toggle_end_column_activate(self, *args):
        """Show or hide the end column."""
        self._toggle_column(gaupol.fields.END)

    @aeidon.deco.export
    def _on_toggle_main_text_column_activate(self, *args):
        """Show or hide the main text column."""
        self._toggle_column(gaupol.fields.MAIN_TEXT)

    @aeidon.deco.export
    def _on_toggle_main_toolbar_activate(self, *args):
        """Show or hide the main toolbar."""
        visible = self.main_toolbar.get_visible()
        self.main_toolbar.set_visible(not visible)
        self.notebook_separator.set_visible(not visible)
        gaupol.conf.application_window.show_main_toolbar = not visible
        self.get_action("toggle-main-toolbar").set_state(not visible)

    @aeidon.deco.export
    def _on_toggle_number_column_activate(self, *args):
        """Show or hide the number column."""
        self._toggle_column(gaupol.fields.NUMBER)

    @aeidon.deco.export
    def _on_toggle_player_activate(self, *args):
        """Show or hide the video player."""
        visible = self.player_box.get_visible()
        self.player_box.set_visible(not visible)
        self.get_action("toggle-player").set_state(not visible)
        self.update_gui()

    @aeidon.deco.export
    def _on_toggle_start_column_activate(self, *args):
        """Show or hide the start column."""
        self._toggle_column(gaupol.fields.START)

    @aeidon.deco.export
    def _on_toggle_translation_text_column_activate(self, *args):
        """Show or hide the translation text column."""
        self._toggle_column(gaupol.fields.TRAN_TEXT)

    def _toggle_column(self, field):
        """Show or hide column corresponding to `field`."""
        page = self.get_current_page()
        col = getattr(page.view.columns, field.name)
        column = page.view.get_column(col)
        visible = column.get_visible()
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
