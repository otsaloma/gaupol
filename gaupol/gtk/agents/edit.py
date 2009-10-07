# Copyright (C) 2005-2009 Osmo Salomaa
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

"""Editing subtitle data."""

import gaupol.gtk
_ = gaupol.i18n._


class EditAgent(gaupol.Delegate):

    """Editing subtitle data."""

    __metaclass__ = gaupol.Contractual

    def __init__(self, master):
        """Initialize an EditAgent object."""

        gaupol.Delegate.__init__(self, master)
        self._pref_dialog = None

    def _on_pref_dialog_response(self, *args):
        """Destroy the preferences dialog."""

        self._pref_dialog.destroy()
        self._pref_dialog = None

    def _set_sensitivities(self, sensitive):
        """Set sensitivities of unsafe UI manager actions."""

        action_group = self.get_action_group("main-unsafe")
        action_group.set_sensitive(sensitive)

    def _sync_clipboards(self, page):
        """Synchronize all clipboards to match that of page."""

        texts = page.project.clipboard.get_texts()
        self.clipboard.set_texts(texts)
        for item in self.pages:
            item.project.clipboard.set_texts(texts)
        text = page.project.clipboard.get_string()
        self.x_clipboard.set_text(text)
        self.update_gui()

    def on_clear_texts_activate(self, *args):
        """Clear the selected texts."""

        page = self.get_current_page()
        rows = page.view.get_selected_rows()
        col = page.view.get_focus()[1]
        doc = page.text_column_to_document(col)
        page.project.clear_texts(rows, doc)

    def on_copy_texts_activate(self, *args):
        """Copy the selected texts to the clipboard."""

        page = self.get_current_page()
        rows = page.view.get_selected_rows()
        col = page.view.get_focus()[1]
        doc = page.text_column_to_document(col)
        page.project.copy_texts(rows, doc)
        self._sync_clipboards(page)

    def on_cut_texts_activate(self, *args):
        """Cut the selected texts to the clipboard."""

        page = self.get_current_page()
        rows = page.view.get_selected_rows()
        col = page.view.get_focus()[1]
        doc = page.text_column_to_document(col)
        page.project.cut_texts(rows, doc)
        self._sync_clipboards(page)

    def on_edit_headers_activate(self, *args):
        """Edit file headers."""

        dialog = gaupol.gtk.HeaderDialog(self.window, self)
        self.flash_dialog(dialog)

    def on_edit_next_value_activate(self, *args):
        """Edit the focused column of the next subtitle."""

        view = self.get_current_page().view
        path, column = view.get_cursor()
        view.set_cursor((path[0] + 1,), column, True)

    def on_edit_preferences_activate(self, *args):
        """Configure Gaupol."""

        if self._pref_dialog is not None:
            return self._pref_dialog.present()
        self._pref_dialog = gaupol.gtk.PreferencesDialog(self.window, self)
        gaupol.util.connect(self, "_pref_dialog", "response")
        self._pref_dialog.show()

    def on_edit_value_activate(self, *args):
        """Edit the focused cell."""

        view = self.get_current_page().view
        row, column = view.get_cursor()
        view.set_cursor(row, column, True)

    def on_extend_selection_to_beginning_activate(self, *args):
        """Extend the selection up to the first subtitle."""

        page = self.get_current_page()
        row = page.view.get_selected_rows()[-1]
        rows = range(0, row + 1)
        page.view.select_rows(rows)

    def on_extend_selection_to_end_activate(self, *args):
        """Extend the selection up to the last subtitle."""

        page = self.get_current_page()
        row = page.view.get_selected_rows()[0]
        rows = range(row, len(page.project.subtitles))
        page.view.select_rows(rows)

    def on_insert_subtitles_activate(self, *args):
        """Insert subtitles."""

        dialog = gaupol.gtk.InsertDialog(self.window, self)
        self.flash_dialog(dialog)

    def on_invert_selection_activate(self, *args):
        """Invert the current selection."""

        page = self.get_current_page()
        rows = set(range(0, len(page.project.subtitles)))
        rows -= set(page.view.get_selected_rows())
        page.view.select_rows(rows)

    def on_merge_subtitles_activate(self, *args):
        """Merge the selected subtitles."""

        page = self.get_current_page()
        rows = page.view.get_selected_rows()
        page.project.merge_subtitles(rows)

    def on_paste_texts_activate(self, *args):
        """Paste texts from the clipboard."""

        page = self.get_current_page()
        rows = page.view.get_selected_rows()
        col = page.view.get_focus()[1]
        doc = page.text_column_to_document(col)
        length = len(page.project.subtitles)
        rows = page.project.paste_texts(rows[0], doc)
        count = len(page.project.subtitles) - length
        if count <= 0: return
        message = gaupol.i18n.ngettext(
            "Inserted %d subtitle to fit clipboard contents",
            "Inserted %d subtitles to fit clipboard contents",
            count) % count
        self.flash_message(message)

    def on_project_action_done(self, *args):
        """Update GUI after doing action."""

        page = self.get_current_page()
        self.update_gui()
        self.emit("page-changed", page)

    def on_project_action_redone(self, *args):
        """Update GUI after redoing action."""

        page = self.get_current_page()
        row = page.view.get_focus()[0]
        if row is not None:
            page.view.scroll_to_row(row)
        self.update_gui()
        self.emit("page-changed", page)

    def on_project_action_undone(self, *args):
        """Update GUI after undoing action."""

        page = self.get_current_page()
        row = page.view.get_focus()[0]
        if row is not None:
            page.view.scroll_to_row(row)
        self.update_gui()
        self.emit("page-changed", page)

    def on_redo_action_activate(self, *args):
        """Redo the last undone action."""

        self.redo()

    def on_remove_subtitles_activate(self, *args):
        """Remove the selected subtitles."""

        page = self.get_current_page()
        rows = page.view.get_selected_rows()
        page.project.remove_subtitles(rows)

    def on_select_all_activate(self, *args):
        """Select all subtitles."""

        page = self.get_current_page()
        selection = page.view.get_selection()
        selection.select_all()

    def on_split_subtitle_activate(self, *args):
        """Split the selected subtitle."""

        page = self.get_current_page()
        row = page.view.get_selected_rows()[0]
        page.project.split_subtitle(row)

    def on_undo_action_activate(self, *args):
        """Undo the last action."""

        self.undo()

    def on_view_renderer_edited(self, renderer, path, value, column):
        """Save changes made while editing cell."""

        self._set_sensitivities(True)
        self.push_message(None)
        page = self.get_current_page()
        row = int(path)
        col = page.view.get_columns().index(column)
        if page.view.is_position_column(col):
            if not value: return
            if page.edit_mode == gaupol.modes.FRAME:
                try: value = int(value)
                except ValueError: return
        if col == page.view.columns.START:
            return page.project.set_start(row, value)
        if col == page.view.columns.END:
            return page.project.set_end(row, value)
        if col ==  page.view.columns.DURATION:
            if page.edit_mode == gaupol.modes.TIME:
                value = value.replace(",", ".")
                try: value = float(value)
                except ValueError: return
            return page.project.set_duration(row, value)
        doc = page.text_column_to_document(col)
        page.project.set_text(row, doc, value)

    def on_view_renderer_editing_canceled(self, *args):
        """Unset state set for editing cell."""

        self._set_sensitivities(True)
        self.push_message(None)

    def on_view_renderer_editing_started(self, renderer, editor, path, column):
        """Set proper state for editing cell."""

        self._set_sensitivities(False)
        page = self.get_current_page()
        col = page.view.get_columns().index(column)
        if not page.view.is_text_column(col): return
        message = _("Use Shift+Return for line-break")
        self.push_message(message)

    def redo_require(self, count=1):
        page = self.get_current_page()
        assert page.project.can_redo()

    def redo(self, count=1):
        """Redo actions."""

        gaupol.gtk.util.set_cursor_busy(self.window)
        page = self.get_current_page()
        page.project.redo(count)
        gaupol.gtk.util.set_cursor_normal(self.window)

    def undo_require(self, count=1):
        page = self.get_current_page()
        assert page.project.can_undo()

    def undo(self, count=1):
        """Undo actions."""

        gaupol.gtk.util.set_cursor_busy(self.window)
        page = self.get_current_page()
        page.project.undo(count)
        gaupol.gtk.util.set_cursor_normal(self.window)
