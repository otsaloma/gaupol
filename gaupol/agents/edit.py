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

"""Editing subtitle data."""

import aeidon
import bisect
import gaupol
_ = aeidon.i18n._


class EditAgent(aeidon.Delegate):

    """Editing subtitle data."""

    def __init__(self, master):
        """Initialize an :class:`EditAgent` instance."""
        aeidon.Delegate.__init__(self, master)
        self._pref_dialog = None

    def _on_pref_dialog_response(self, *args):
        """Destroy the preferences dialog."""
        self._pref_dialog.destroy()
        self._pref_dialog = None
        gaupol.conf.write_to_file()

    def _set_unsafe_sensitivities(self, sensitive):
        """Set sensitivities of unsafe UI manager actions."""
        action_group = self.get_action_group("main-unsafe")
        action_group.set_sensitive(sensitive)

    def _sync_clipboards(self, page):
        """Synchronize all clipboards to match that of `page`."""
        texts = page.project.clipboard.get_texts()
        self.clipboard.set_texts(texts)
        for item in self.pages:
            item.project.clipboard.set_texts(texts)
        text = page.project.clipboard.get_string()
        self.x_clipboard.set_text(text, -1)
        self.update_gui()

    @aeidon.deco.export
    def _on_clear_texts_activate(self, *args):
        """Clear the selected texts."""
        page = self.get_current_page()
        rows = page.view.get_selected_rows()
        col = page.view.get_focus()[1]
        doc = page.text_column_to_document(col)
        page.project.clear_texts(rows, doc)

    @aeidon.deco.export
    def _on_copy_texts_activate(self, *args):
        """Copy the selected texts to the clipboard."""
        page = self.get_current_page()
        rows = page.view.get_selected_rows()
        col = page.view.get_focus()[1]
        doc = page.text_column_to_document(col)
        page.project.copy_texts(rows, doc)
        self._sync_clipboards(page)

    @aeidon.deco.export
    def _on_cut_texts_activate(self, *args):
        """Cut the selected texts to the clipboard."""
        page = self.get_current_page()
        rows = page.view.get_selected_rows()
        col = page.view.get_focus()[1]
        doc = page.text_column_to_document(col)
        page.project.cut_texts(rows, doc)
        self._sync_clipboards(page)

    @aeidon.deco.export
    def _on_edit_headers_activate(self, *args):
        """Edit file headers."""
        dialog = gaupol.HeaderDialog(self.window, self)
        gaupol.util.flash_dialog(dialog)

    @aeidon.deco.export
    def _on_edit_next_value_activate(self, *args):
        """Edit the focused column of the next subtitle."""
        page = self.get_current_page()
        path, column = page.view.get_cursor()
        row = gaupol.util.tree_path_to_row(path)
        path = gaupol.util.tree_row_to_path(row+1)
        page.view.set_cursor(path, column, True)

    @aeidon.deco.export
    def _on_edit_preferences_activate(self, *args):
        """Configure Gaupol."""
        if self._pref_dialog is not None:
            return self._pref_dialog.present()
        self._pref_dialog = gaupol.PreferencesDialog(self.window, self)
        aeidon.util.connect(self, "_pref_dialog", "response")
        self._pref_dialog.show()

    @aeidon.deco.export
    def _on_edit_value_activate(self, *args):
        """Edit the focused cell."""
        page = self.get_current_page()
        path, column = page.view.get_cursor()
        page.view.set_cursor(path, column, True)

    @aeidon.deco.export
    def _on_end_earlier_activate(self, *args):
        """End the selected subtitle earlier."""
        page = self.get_current_page()
        row = page.view.get_selected_rows()[0]
        pos = page.project.subtitles[row].end_seconds
        length = gaupol.conf.editor.stretch_length
        value = ((pos-0.001) // length) * length
        page.project.set_end(row, value)
        register = aeidon.registers.DO
        description = _("Stretching end position")
        page.project.set_action_description(register, description)
        # Group repeated stretces as one action.
        if (len(page.project.undoables) > 1 and
            page.project.undoables[1].description ==
            page.project.undoables[0].description):
            page.project.group_actions(register, 2, description)

    @aeidon.deco.export
    def _on_end_later_activate(self, *args):
        """End the selected subtitle later."""
        page = self.get_current_page()
        row = page.view.get_selected_rows()[0]
        pos = page.project.subtitles[row].end_seconds
        length = gaupol.conf.editor.stretch_length
        value = (((pos+0.001) // length) + 1) * length
        page.project.set_end(row, value)
        register = aeidon.registers.DO
        description = _("Stretching end position")
        page.project.set_action_description(register, description)
        # Group repeated stretces as one action.
        if (len(page.project.undoables) > 1 and
            page.project.undoables[1].description ==
            page.project.undoables[0].description):
            page.project.group_actions(register, 2, description)

    @aeidon.deco.export
    def _on_extend_selection_to_beginning_activate(self, *args):
        """Extend the selection up to the first subtitle."""
        page = self.get_current_page()
        row = page.view.get_selected_rows()[-1]
        rows = list(range(0, row+1))
        page.view.select_rows(rows)

    @aeidon.deco.export
    def _on_extend_selection_to_end_activate(self, *args):
        """Extend the selection up to the last subtitle."""
        page = self.get_current_page()
        row = page.view.get_selected_rows()[0]
        rows = list(range(row, len(page.project.subtitles)))
        page.view.select_rows(rows)

    @aeidon.deco.export
    def _on_insert_subtitle_at_video_position_activate(self, *args):
        """Insert a new subtitle at video position."""
        mode = aeidon.modes.SECONDS
        pos = self.player.get_position(mode)
        page = self.get_current_page()
        starts = [x.start_seconds for x in page.project.subtitles]
        index = bisect.bisect_right(starts, pos)
        subtitle = page.project.new_subtitle()
        subtitle.start_seconds = pos
        subtitle.end_seconds = pos + 3.0
        subtitle.main_text = "[{:d}]".format(index+1)
        page.project.insert_subtitles((index,), (subtitle,))

    @aeidon.deco.export
    def _on_insert_subtitles_activate(self, *args):
        """Insert subtitles."""
        dialog = gaupol.InsertDialog(self.window, self)
        gaupol.util.flash_dialog(dialog)

    @aeidon.deco.export
    def _on_invert_selection_activate(self, *args):
        """Invert the current selection."""
        page = self.get_current_page()
        rows = set(range(0, len(page.project.subtitles)))
        rows -= set(page.view.get_selected_rows())
        page.view.select_rows(rows)

    @aeidon.deco.export
    def _on_merge_subtitles_activate(self, *args):
        """Merge the selected subtitles."""
        page = self.get_current_page()
        rows = page.view.get_selected_rows()
        page.project.merge_subtitles(rows)

    @aeidon.deco.export
    def _on_paste_texts_activate(self, *args):
        """Paste texts from the clipboard."""
        page = self.get_current_page()
        rows = page.view.get_selected_rows()
        row, col = page.view.get_focus()
        doc = page.text_column_to_document(col)
        length = len(page.project.subtitles)
        # Ensure that even if new subtitles need to be inserted,
        # focus and scroll position are not moved to the end.
        rect = page.view.get_visible_rect()
        window = page.view.get_bin_window()
        window.freeze_updates()
        rows = page.project.paste_texts(rows[0], doc)
        rows = page.view.get_selected_rows()
        page.view.set_focus(row, col)
        page.view.select_rows(rows)
        page.view.scroll_to_point(rect.x, rect.y)
        window.thaw_updates()
        count = len(page.project.subtitles) - length
        if count > 0:
            self.flash_message(aeidon.i18n.ngettext(
                    "Inserted {:d} subtitle to fit clipboard contents",
                    "Inserted {:d} subtitles to fit clipboard contents",
                    count).format(count))

    @aeidon.deco.export
    def _on_project_action_done(self, *args):
        """Update user interface and send a signal."""
        page = self.get_current_page()
        self.update_gui()
        self.emit("page-changed", page)

    @aeidon.deco.export
    def _on_project_action_redone(self, *args):
        """Update user interface and send a signal."""
        page = self.get_current_page()
        row = page.view.get_focus()[0]
        if row is not None:
            page.view.scroll_to_row(row)
        self.update_gui()
        self.emit("page-changed", page)

    @aeidon.deco.export
    def _on_project_action_undone(self, *args):
        """Update user interface and send a signal."""
        page = self.get_current_page()
        row = page.view.get_focus()[0]
        if row is not None:
            page.view.scroll_to_row(row)
        self.update_gui()
        self.emit("page-changed", page)

    @aeidon.deco.export
    def _on_redo_action_activate(self, *args):
        """Redo the last undone action."""
        self.redo()

    @aeidon.deco.export
    def _on_remove_subtitles_activate(self, *args):
        """Remove the selected subtitles."""
        page = self.get_current_page()
        rows = page.view.get_selected_rows()
        page.project.remove_subtitles(rows)

    @aeidon.deco.export
    def _on_select_all_activate(self, *args):
        """Select all subtitles."""
        page = self.get_current_page()
        selection = page.view.get_selection()
        selection.select_all()

    @aeidon.deco.export
    def _on_set_end_from_video_position_activate(self, *args):
        """Set subtitle end from video position."""
        page = self.get_current_page()
        mode = aeidon.modes.SECONDS
        row = page.view.get_selected_rows()[0]
        pos = self.player.get_position(mode)
        page.project.set_end(row, pos)

    @aeidon.deco.export
    def _on_split_subtitle_activate(self, *args):
        """Split the selected subtitle."""
        page = self.get_current_page()
        row = page.view.get_selected_rows()[0]
        page.project.split_subtitle(row)

    @aeidon.deco.export
    def _on_start_earlier_activate(self, *args):
        """Start the selected subtitle earlier."""
        page = self.get_current_page()
        row = page.view.get_selected_rows()[0]
        pos = page.project.subtitles[row].start_seconds
        length = gaupol.conf.editor.stretch_length
        value = ((pos-0.001) // length) * length
        page.project.set_start(row, value)
        register = aeidon.registers.DO
        description = _("Stretching start position")
        page.project.set_action_description(register, description)
        # Group repeated stretces as one action.
        if (len(page.project.undoables) > 1 and
            page.project.undoables[1].description ==
            page.project.undoables[0].description):
            page.project.group_actions(register, 2, description)

    @aeidon.deco.export
    def _on_start_later_activate(self, *args):
        """Start the selected subtitle later."""
        page = self.get_current_page()
        row = page.view.get_selected_rows()[0]
        pos = page.project.subtitles[row].start_seconds
        length = gaupol.conf.editor.stretch_length
        value = (((pos+0.001) // length) + 1) * length
        page.project.set_start(row, value)
        register = aeidon.registers.DO
        description = _("Stretching start position")
        page.project.set_action_description(register, description)
        # Group repeated stretces as one action.
        if (len(page.project.undoables) > 1 and
            page.project.undoables[1].description ==
            page.project.undoables[0].description):
            page.project.group_actions(register, 2, description)

    @aeidon.deco.export
    def _on_undo_action_activate(self, *args):
        """Undo the last action."""
        self.undo()

    @aeidon.deco.export
    def _on_view_renderer_edited(self, renderer, path, value, column):
        """Save changes made while editing cell."""
        self._set_unsafe_sensitivities(True)
        self.show_message(None)
        page = self.get_current_page()
        row = gaupol.util.tree_path_to_row(path)
        col = page.view.get_columns().index(column)
        if page.view.is_position_column(col):
            if not value: return
            if page.edit_mode == aeidon.modes.FRAME:
                try:
                    value = aeidon.as_frame(value)
                except ValueError:
                    return
        if col == page.view.columns.START:
            return page.project.set_start(row, value)
        if col == page.view.columns.END:
            return page.project.set_end(row, value)
        if col ==  page.view.columns.DURATION:
            if page.edit_mode == aeidon.modes.TIME:
                value = value.replace(",", ".")
                try:
                    value = aeidon.as_seconds(value)
                except ValueError:
                    return
            return page.project.set_duration(row, value)
        doc = page.text_column_to_document(col)
        page.project.set_text(row, doc, value)

    @aeidon.deco.export
    def _on_view_renderer_editing_canceled(self, *args):
        """Unset state set for editing cell."""
        self._set_unsafe_sensitivities(True)
        self.show_message(None)

    @aeidon.deco.export
    def _on_view_renderer_editing_started(self, renderer, editor, path, column):

        """Set proper state for editing cell."""
        self._set_unsafe_sensitivities(False)
        page = self.get_current_page()
        col = page.view.get_columns().index(column)
        if not page.view.is_text_column(col): return
        self.show_message(_("Use Shift+Return for line-break"))

    @aeidon.deco.export
    def redo(self, count=1):
        """Redo `count` amount of actions."""
        gaupol.util.set_cursor_busy(self.window)
        page = self.get_current_page()
        page.project.redo(count)
        gaupol.util.set_cursor_normal(self.window)

    @aeidon.deco.export
    def undo(self, count=1):
        """Undo `count` amount of actions."""
        gaupol.util.set_cursor_busy(self.window)
        page = self.get_current_page()
        page.project.undo(count)
        gaupol.util.set_cursor_normal(self.window)
