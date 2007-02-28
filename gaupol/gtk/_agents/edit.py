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


"""Editing subtitle data."""


from gettext import gettext as _
from gettext import ngettext

import gtk

from gaupol.base import Delegate
from gaupol.gtk import cons, util
from gaupol.gtk.dialogs import HeaderDialog, InsertDialog, PreferencesDialog
from gaupol.gtk.index import *


class EditAgent(Delegate):

    """Editing subtitle data.

    Instance variables:

        _pref_dialog: PreferencesDialog or None
    """

    # pylint: disable-msg=E0203,W0201

    def __init__(self, master):

        Delegate.__init__(self, master)

        self._pref_dialog = None

    def _get_next_cell(self, page, row, col, keyname):
        """Get adjacent cell to move to with Alt+Arrow."""

        if keyname == "Up":
            return max(0, row - 1), col
        if keyname == "Down":
            max_row = len(page.project.times) - 1
            return min(max_row, row + 1), col

        def get_visible(col):
            return page.view.get_column(col).get_visible()
        visible_cols = list(x for x in range(1, 6) if get_visible(x))
        if keyname == "Left":
            cols = list(x for x in visible_cols if x < col)
            col = (max(cols) if cols else col)
            return row, col
        if keyname == "Right":
            cols = list(x for x in visible_cols if x > col)
            col = (min(cols) if cols else col)
            return row, col

    @util.ignore_exceptions(AssertionError)
    def _on_editor_key_press_event(self, editor, event, page, row, col):
        """End editing cell or move between adjacent cells."""

        # pylint: disable-msg=W0612
        keymap = gtk.gdk.keymap_get_default()
        keyval, egroup, level, consumed = keymap.translate_keyboard_state(
            event.hardware_keycode, event.state, event.group)
        keyname = gtk.gdk.keyval_name(keyval)
        assert event.state & ~consumed & gtk.gdk.MOD1_MASK
        assert keyname in ("Up", "Down", "Left", "Right")
        if col == SHOW:
            # FIX: SEGFAULT.
            assert not page.project.needs_resort(row, editor.get_text())
        row, col = self._get_next_cell(page, row, col, keyname)
        column = page.view.get_column(col)
        editor.emit("editing-done")
        while gtk.events_pending():
            gtk.main_iteration()
        page.view.set_cursor(row, column, True)

    def _on_pref_dialog_response(self, *args):
        """Destroy the preferences dialog."""

        self._pref_dialog.destroy()
        self._pref_dialog = None

    def _set_sensitivities(self, sensitive):
        """Set menubar and toolbar sensitivities."""

        for group in self.uim.get_action_groups():
            group.set_sensitive(sensitive)
        self.uim.get_widget("/ui/menubar").set_sensitive(sensitive)
        self.uim.get_widget("/ui/main_toolbar").set_sensitive(sensitive)
        self.video_toolbar.set_sensitive(sensitive)

    def _sync_clipboards(self, page):
        """Synchronize all clipboards to match that of page."""

        data = page.project.clipboard.data
        self.clipboard.data = data
        for item in self.pages:
            item.project.clipboard.data = data
        text = page.project.clipboard.get_data_as_string()
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

        dialog = HeaderDialog(self.window, self)
        self.flash_dialog(dialog)
        self.update_gui()

    def on_edit_preferences_activate(self, *args):
        """Configure Gaupol."""

        if self._pref_dialog is None:
            self._pref_dialog = PreferencesDialog()
            util.connect(self, "_pref_dialog", "response")
            self._pref_dialog.show()
        self._pref_dialog.present()

    def on_edit_value_activate(self, *args):
        """Edit the focused cell."""

        view = self.get_current_page().view
        row, column = view.get_cursor()
        view.set_cursor(row, column, True)

    def on_insert_subtitles_activate(self, *args):
        """Insert blank subtitles."""

        dialog = InsertDialog(self.window, self)
        self.flash_dialog(dialog)

    def on_invert_selection_activate(self, *args):
        """Invert the current selection."""

        page = self.get_current_page()
        rows = set(range(0, len(page.project.times)))
        rows.difference_update(set(page.view.get_selected_rows()))
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
        length = len(page.project.times)
        rows = page.project.paste_texts(rows[0], doc)
        count = len(page.project.times) - length
        if count > 0:
            message = ngettext(
                "Inserted %d subtitle to fit clipboard contents",
                "Inserted %d subtitles to fit clipboard contents",
                count ) % count
            self.push_message(message)

    def on_project_action_done(self, *args):
        """Update GUI after doing action."""

        self.update_gui()
        self.emit("page-changed", self.get_current_page())

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

    def on_redo_button_clicked(self, *args):
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

    def on_undo_button_clicked(self, *args):
        """Undo the last action."""

        self.undo()

    util.ignore_exceptions(AssertionError)
    def on_view_renderer_edited(self, renderer, path, value, col):
        """Finish editing cell."""

        row = int(path)
        self._set_sensitivities(True)
        self.push_message(None)
        page = self.get_current_page()
        if col in (SHOW, HIDE, DURN):
            assert value
            if page.edit_mode == cons.MODE.FRAME:
                assert value.isdigit()
                value = int(value)
            new_row = page.project.set_position(row, col - 1, value)
            if new_row != row:
                page.view.set_focus(new_row, col)
        elif col in (MTXT, TTXT):
            page.project.set_text(row, col - 4, value)

    def on_view_renderer_editing_canceled(self, *args):
        """Cancel editing cell."""

        self._set_sensitivities(True)
        self.push_message(None)

    def on_view_renderer_editing_started(self, renderer, editor, path, col):
        """Start editing cell."""

        row = int(path)
        self._set_sensitivities(False)
        page = self.get_current_page()
        message = _("Use Alt+Arrow to move to edit an adjacent cell")
        if col in (MTXT, TTXT):
            message = _("Use Shift+Return for line-break")
        self.push_message(message, False)
        method = self._on_editor_key_press_event
        editor.connect("key-press-event", method, page, row, col)

    def redo(self, count=1):
        """Redo actions."""

        util.set_cursor_busy(self.window)
        page = self.get_current_page()
        page.project.redo(count)
        util.set_cursor_normal(self.window)

    def undo(self, count=1):
        """Undo actions."""

        util.set_cursor_busy(self.window)
        page = self.get_current_page()
        page.project.undo(count)
        util.set_cursor_normal(self.window)
