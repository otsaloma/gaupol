# Copyright (C) 2005-2006 Osmo Salomaa
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


"""Basic subtitle data editing."""


from gettext import gettext as _
from gettext import ngettext

import gtk

from gaupol.gtk                  import cons
from gaupol.gtk.icons            import *
from gaupol.gtk.delegate         import Delegate, UIMAction
from gaupol.gtk.dialog.subinsert import SubtitleInsertDialog
from gaupol.gtk.util             import gtklib


class _ClipboardAction(UIMAction):

    """Base class for clipboard actions."""

    @classmethod
    def is_doable(cls, app, page):
        """Return action doability."""

        if page is None:
            return False
        selection = bool(page.view.get_selected_rows())
        focus = page.view.get_focus()[1] in (MTXT, TTXT)
        return bool(selection and focus)


class _SelectionAction(UIMAction):

    """Base class for selection actions."""

    @classmethod
    def is_doable(cls, app, page):
        """Return action doability."""

        if page is None:
            return False
        return bool(page.project.times)


class ClearTextsAction(_ClipboardAction):

    """Clearing texts."""

    action_item = (
        'clear_texts',
        gtk.STOCK_CLEAR,
        _('C_lear'),
        'Delete',
        _('Clear the selected texts'),
        'on_clear_texts_activate'
    )

    paths = ['/ui/menubar/edit/clear', '/ui/view/clear']


class CopyTextsAction(_ClipboardAction):

    """Copying texts to clipboard."""

    action_item = (
        'copy_texts',
        gtk.STOCK_COPY,
        _('_Copy'),
        '<control>C',
        _('Copy the selected texts to the clipboard'),
        'on_copy_texts_activate'
    )

    paths = ['/ui/menubar/edit/copy', '/ui/view/copy']


class CutTextsAction(_ClipboardAction):

    """Cutting texts to clipboard."""

    action_item = (
        'cut_texts',
        gtk.STOCK_CUT,
        _('Cu_t'),
        '<control>X',
        _('Cut the selected texts to the clipboard'),
        'on_cut_texts_activate'
    )

    paths = ['/ui/menubar/edit/cut', '/ui/view/cut']


class EditValueAction(UIMAction):

    """Editing value of a single cell."""

    action_item = (
        'edit_value',
        gtk.STOCK_EDIT,
        _('_Edit'),
        'Return',
        _('Edit the focused cell'),
        'on_edit_value_activate'
    )

    paths = ['/ui/menubar/edit/edit', '/ui/view/edit']

    @classmethod
    def is_doable(cls, app, page):
        """Return action doability."""

        if page is None:
            return False

        row, col = page.view.get_focus()
        if None in (row, col):
            return False
        elif col == NUMB:
            return False
        else:
            return True


class InsertSubtitlesAction(UIMAction):

    """Inserting subtitles."""

    action_item = (
        'insert_subtitles',
        gtk.STOCK_ADD,
        _('_Insert Subtitles...'),
        '<control>Insert',
        _('Insert blank subtitles'),
        'on_insert_subtitles_activate'
    )

    paths = ['/ui/menubar/edit/insert', '/ui/view/insert']

    @classmethod
    def is_doable(cls, app, page):
        """Return action doability."""

        if page is None:
            return False
        if page.view.get_selected_rows():
            return True
        if not page.project.times:
            return True
        return False


class InvertSelectionAction(_SelectionAction):

    """Inverting selection."""

    action_item = (
        'invert_selection',
        None,
        _('In_vert Selection'),
        '<shift><control>A',
        _('Invert the current selection'),
        'on_invert_selection_activate'
    )

    paths = ['/ui/menubar/edit/invert_selection']


class PasteTextsAction(_ClipboardAction):

    """Pasting texts from clipboard."""

    action_item = (
        'paste_texts',
        gtk.STOCK_PASTE,
        _('_Paste'),
        '<control>V',
        _('Paste texts from the clipboard'),
        'on_paste_texts_activate'
    )

    paths = ['/ui/menubar/edit/paste', '/ui/view/paste']


class RemoveSubtitlesAction(UIMAction):

    """Removing subtitles."""

    action_item = (
        'remove_subtitles',
        gtk.STOCK_REMOVE,
        _('Re_move Subtitles'),
        '<control>Delete',
        _('Remove the selected subtitles'),
        'on_remove_subtitles_activate'
    )

    paths = ['/ui/menubar/edit/remove', '/ui/view/remove']

    @classmethod
    def is_doable(cls, app, page):
        """Return action doability."""

        if page is None:
            return False
        return bool(page.view.get_selected_rows())


class SelectAllAction(_SelectionAction):

    """Selecting all subtitles."""

    action_item = (
        'select_all',
        None,
        _('_Select All'),
        '<control>A',
        _('Select all subtitles'),
        'on_select_all_activate'
    )

    paths = ['/ui/menubar/edit/select_all']


class EditDelegate(Delegate):

    """Basic subtitle data editing."""

    def _get_next_cell(self, page, row, col, keyname):
        """Get adjacent cell to move to."""

        min_row = 0
        max_row = len(page.project.times) - 1
        visible_cols = []
        for i in range(1, 6):
            if page.view.get_column(i).get_visible():
                visible_cols.append(i)
        min_col = min(visible_cols)
        max_col = max(visible_cols)

        next_col = col
        next_row = row
        if keyname == 'Left':
            for i in reversed(range(min_col, col)):
                if i in visible_cols:
                    next_col = i
                    break
        elif keyname == 'Up':
            next_row = max(min_row, row - 1)
        elif keyname == 'Right':
            for i in range(col + 1, max_col + 1):
                if i in visible_cols:
                    next_col = i
                    break
        elif keyname == 'Down':
            next_row = min(row + 1, max_row)

        return next_row, next_col

    def _set_sensitivities(self, sensitive):
        """Set menubar and toolbar sensitivities."""

        for group in self._uim.get_action_groups():
            group.set_sensitive(sensitive)
        self._uim.get_widget('/ui/menubar').set_sensitive(sensitive)
        self._uim.get_widget('/ui/main_toolbar').set_sensitive(sensitive)
        video_toolbar = gtklib.get_parent_widget(
            self._video_button, gtk.Toolbar)
        video_toolbar.set_sensitive(sensitive)

    def on_clear_texts_activate(self, *args):
        """Clear selected texts"""

        page = self.get_current_page()
        rows = page.view.get_selected_rows()
        col  = page.view.get_focus()[1]
        doc  = page.text_column_to_document(col)

        page.project.clear_texts(rows, doc)

    def on_copy_texts_activate(self, *args):
        """Copy selected texts to clipboard."""

        page = self.get_current_page()
        rows = page.view.get_selected_rows()
        col  = page.view.get_focus()[1]
        doc  = page.text_column_to_document(col)

        page.project.copy_texts(rows, doc)
        text = page.project.clipboard.get_data_as_string()
        self._clipboard.set_text(text)
        self.set_sensitivities(page)

    def on_cut_texts_activate(self, *args):
        """Cut selected texts to clipboard."""

        page = self.get_current_page()
        rows = page.view.get_selected_rows()
        col  = page.view.get_focus()[1]
        doc  = page.text_column_to_document(col)

        page.project.cut_texts(rows, doc)
        text = page.project.clipboard.get_data_as_string()
        self._clipboard.set_text(text)

    def on_edit_value_activate(self, *args):
        """Edit focused cell."""

        view = self.get_current_page().view
        row, column = view.get_cursor()
        view.set_cursor(row, column, True)

    def on_insert_subtitles_activate(self, *args):
        """Insert blank subtitles."""

        page = self.get_current_page()
        dialog = SubtitleInsertDialog(self._window, page.project)
        response = dialog.run()
        above    = dialog.get_above()
        amount   = dialog.get_amount()
        dialog.destroy()
        if response != gtk.RESPONSE_OK:
            return

        start_row = 0
        if page.project.times:
            start_row = page.view.get_selected_rows()[0]
            if not above:
                start_row += 1

        rows = range(start_row, start_row + amount)
        page.project.insert_subtitles(rows)
        page.view.select_rows(rows)

    def on_invert_selection_activate(self, *args):
        """Invert selection."""

        page = self.get_current_page()
        selected_rows = page.view.get_selected_rows()
        rows = range(0, len(page.project.times))
        for row in selected_rows:
            rows.remove(row)
        page.view.select_rows(rows)
        page.view.grab_focus()

    def on_paste_texts_activate(self, *args):
        """Paste texts from the clipboard."""

        page = self.get_current_page()
        rows = page.view.get_selected_rows()
        col  = page.view.get_focus()[1]
        doc  = page.text_column_to_document(col)

        orig_length = len(page.project.times)
        rows = page.project.paste_texts(rows[0], doc)
        page.view.select_rows(rows)
        new_length = len(page.project.times)
        if new_length > orig_length:
            count = new_length - orig_length
            message = ngettext(
                'Inserted %d subtitle to fit clipboard contents',
                'Inserted %d subtitles to fit clipboard contents',
                count
            ) % count
            self.set_status_message(message)

    def on_remove_subtitles_activate(self, *args):
        """Remove selected subtitles."""

        page = self.get_current_page()
        col  = page.view.get_focus()[1]
        rows = page.view.get_selected_rows()

        page.project.remove_subtitles(rows)
        if page.project.times:
            row = min(rows[0], len(page.project.times) - 1)
            page.view.set_focus(row, col)

    def on_select_all_activate(self, *args):
        """Select all subtitles."""

        page = self.get_current_page()
        selection = page.view.get_selection()
        selection.select_all()
        page.view.grab_focus()

    def on_view_cell_edited(self, cell_renderer, value, row, col):
        """Finish editing cell."""

        gtklib.set_cursor_busy(self._window)
        self._set_sensitivities(True)
        self.set_status_message(None)
        page = self.get_current_page()

        if col in (SHOW, HIDE, DURN):
            gtklib.set_cursor_busy(self._window)
            if page.edit_mode == cons.Mode.TIME:
                new_row = page.project.set_time(row, col - 1, value)
            elif page.edit_mode == cons.Mode.FRAME:
                try:
                    value = int(value)
                except ValueError:
                    self.set_sensitivities(page)
                    gtklib.set_cursor_normal(self._window)
                    return
                new_row = page.project.set_frame(row, col - 1, value)
            if new_row != row:
                page.view.set_focus(new_row, col)
        elif col in (MTXT, TTXT):
            page.project.set_text(row, col - 4, value)
            self.set_character_status(page)

        gtklib.set_cursor_normal(self._window)

    def on_view_cell_editing_canceled(self, *args):
        """Cancel editing cell."""

        self._set_sensitivities(True)
        self.set_status_message(None)

    def on_view_cell_editing_started(self, cell_renderer, editor, row, col):
        """Start editing cell."""

        self._set_sensitivities(False)
        page = self.get_current_page()
        row = int(row)
        message = _('Use Alt+Arrow for moving to edit an adjacent cell')
        if col in (MTXT, TTXT):
            message = _('Use Shift+Return for line-break')
        self.set_status_message(message, False)

        def on_key_press_event(editor, event):
            keymap = gtk.gdk.keymap_get_default()
            keyval, egroup, level, consumed = keymap.translate_keyboard_state(
                event.hardware_keycode, event.state, event.group)
            keyname = gtk.gdk.keyval_name(keyval)
            if not event.state & ~consumed & gtk.gdk.MOD1_MASK:
                return
            if keyname not in ('Up', 'Down', 'Left', 'Right'):
                return
            if col == SHOW:
                if page.project.needs_resort(row, editor.get_text()):
                    return
            next_row, next_col = self._get_next_cell(page, row, col, keyname)
            next_column = page.view.get_column(next_col)
            editor.emit('editing-done')
            while gtk.events_pending():
                gtk.main_iteration()
            page.view.set_cursor(next_row, next_column, True)

        editor.connect('key-press-event', on_key_press_event)
