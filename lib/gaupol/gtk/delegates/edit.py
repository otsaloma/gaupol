# Copyright (C) 2005 Osmo Salomaa
#
# This file is part of Gaupol.
#
# Gaupol is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Gaupol is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Gaupol; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA


"""Editing subtitle data."""


try:
    from psyco.classes import *
except ImportError:
    pass

import gtk

from gaupol.base.error            import FitError
from gaupol.constants             import Mode, Position
from gaupol.gtk.colconstants      import *
from gaupol.gtk.delegates         import Delegate, UIMAction
from gaupol.gtk.dialogs.insertsub import InsertSubtitleDialog
from gaupol.gtk.dialogs.message   import ErrorDialog
from gaupol.gtk.util              import config, gtklib


class ClipboardAction(UIMAction):

    """Base class for clipboard actions."""

    @classmethod
    def is_doable(cls, application, page):
        """Return whether action can or cannot be done."""

        if page is None:
            return False

        selection = bool(page.view.get_selected_rows())
        focus = page.view.get_focus()[1] in (MTXT, TTXT)
        return bool(selection and focus)


class SelectionAction(UIMAction):

    """Base class for selection actions."""

    @classmethod
    def is_doable(cls, application, page):
        """Return whether action can or cannot be done."""

        if page is None:
            return False

        return bool(page.project.times)


class ClearTextsAction(ClipboardAction):

    """Clearing texts."""

    uim_action_item = (
        'clear_texts',
        gtk.STOCK_CLEAR,
        _('C_lear'),
        'Delete',
        _('Clear the selected texts'),
        'on_clear_texts_activated'
    )

    uim_paths = ['/ui/menubar/edit/clear', '/ui/view/clear']


class CopyTextsAction(ClipboardAction):

    """Copying texts to the clipboard."""

    uim_action_item = (
        'copy_texts',
        gtk.STOCK_COPY,
        _('_Copy'),
        '<control>C',
        _('Copy the selected texts to the clipboard'),
        'on_copy_texts_activated'
    )

    uim_paths = ['/ui/menubar/edit/copy', '/ui/view/copy']


class CutTextsAction(ClipboardAction):

    """Cutting texts to the clipboard."""

    uim_action_item = (
        'cut_texts',
        gtk.STOCK_CUT,
        _('Cu_t'),
        '<control>X',
        _('Cut the selected texts to the clipboard'),
        'on_cut_texts_activated'
    )

    uim_paths = ['/ui/menubar/edit/cut', '/ui/view/cut']


class EditValueAction(UIMAction):

    """Editing the value of a single cell."""

    uim_action_item = (
        'edit_value',
        gtk.STOCK_EDIT,
        _('_Edit'),
        'Return',
        _('Edit the focused cell'),
        'on_edit_value_activated'
    )

    uim_paths = ['/ui/menubar/edit/value', '/ui/view/value']

    @classmethod
    def is_doable(cls, application, page):
        """Return whether action can or cannot be done."""

        if page is None:
            return False

        row, col = page.view.get_focus()

        if None in (row, col):
            return False
        elif col == NO:
            return False
        else:
            return True


class InsertSubtitlesAction(UIMAction):

    """Inserting subtitles."""

    uim_action_item = (
        'insert_subtitles',
        gtk.STOCK_ADD,
        _('_Insert Subtitles'),
        '<control>Insert',
        _('Insert blank subtitles'),
        'on_insert_subtitles_activated'
    )

    uim_paths = ['/ui/menubar/edit/insert', '/ui/view/insert']

    @classmethod
    def is_doable(cls, application, page):
        """Return whether action can or cannot be done."""

        if page is None:
            return False

        if page.view.get_selected_rows():
            return True
        if not page.project.times:
            return True

        return False


class InvertSelectionAction(SelectionAction):

    """Inverting selection."""

    uim_action_item = (
        'invert_selection',
        None,
        _('In_vert Selection'),
        None,
        _('Invert the current selection'),
        'on_invert_selection_activated'
    )

    uim_paths = ['/ui/menubar/edit/invert_selection']


class PasteTextsAction(ClipboardAction):

    """Pasting texts from the clipboard."""

    uim_action_item = (
        'paste_texts',
        gtk.STOCK_PASTE,
        _('_Paste'),
        '<control>V',
        _('Paste texts from the clipboard'),
        'on_paste_texts_activated'
    )

    uim_paths = ['/ui/menubar/edit/paste', '/ui/view/paste']


class RemoveSubtitlesAction(UIMAction):

    """Removing subtitles."""

    uim_action_item = (
        'remove_subtitles',
        gtk.STOCK_REMOVE,
        _('Re_move Subtitles'),
        '<control>Delete',
        _('Remove the selected subtitles'),
        'on_remove_subtitles_activated'
    )

    uim_paths = ['/ui/menubar/edit/remove', '/ui/view/remove']

    @classmethod
    def is_doable(cls, application, page):
        """Return whether action can or cannot be done."""

        if page is None:
            return False

        return bool(page.view.get_selected_rows())


class SelectAllAction(SelectionAction):

    """Selecting all subtitles."""

    uim_action_item = (
        'select_all',
        None,
        _('_Select All'),
        '<control>A',
        _('Select all subtitles'),
        'on_select_all_activated'
    )

    uim_paths = ['/ui/menubar/edit/select_all']


class UnSelectAllAction(SelectionAction):

    """Unselecting all subtitles."""

    uim_action_item = (
        'unselect_all',
        None,
        _('U_nselect All'),
        '<shift><control>A',
        _('Unselect all subtitles'),
        'on_unselect_all_activated'
    )

    uim_paths = ['/ui/menubar/edit/unselect_all']


class PasteFitErrorDialog(ErrorDialog):

    """Dialog to inform that clipboard contents did not fit."""

    def __init__(self, parent):

        title   = _('Not enough space available to fit clipboard contents')
        message = _('Please first insert new subtitles if you wish to paste '
                    'at the current location')

        ErrorDialog.__init__(self, parent, title, message)


class EditDelegate(Delegate):

    """Editing subtitle data."""

    def on_clear_texts_activated(self, *args):
        """Paste texts from the clipboard."""

        page     = self.get_current_page()
        rows     = page.view.get_selected_rows()
        col      = page.view.get_focus()[1]
        document = page.text_column_to_document(col)

        page.project.clear_texts(rows, document)
        self.set_sensitivities(page)

    def on_copy_texts_activated(self, *args):
        """Cut the selected texts to the clipboard."""

        page     = self.get_current_page()
        rows     = page.view.get_selected_rows()
        col      = page.view.get_focus()[1]
        document = page.text_column_to_document(col)

        page.project.copy_texts(rows, document)

        # Put a string representation of the Gaupol internal clipboard to the
        # X clipboard.
        text = page.project.clipboard.get_data_as_string()
        self.clipboard.set_text(text)

        self.set_sensitivities(page)

    def on_cut_texts_activated(self, *args):
        """Cut the selected texts to the clipboard."""

        page     = self.get_current_page()
        rows     = page.view.get_selected_rows()
        col      = page.view.get_focus()[1]
        document = page.text_column_to_document(col)

        page.project.cut_texts(rows, document)

        # Put a string representation of the Gaupol internal clipboard to the
        # X clipboard.
        text = page.project.clipboard.get_data_as_string()
        self.clipboard.set_text(text)

        self.set_sensitivities(page)

    def on_edit_value_activated(self, *args):
        """Edit the focused cell."""

        view = self.get_current_page().view
        row, tree_view_column = view.get_cursor()
        view.set_cursor(row, tree_view_column, True)

    def on_insert_subtitles_activated(self, *args):
        """Insert blank subtitles."""

        dialog = InsertSubtitleDialog(self.window)
        page = self.get_current_page()
        if not page.project.times:
            dialog.set_position_sensitive(False)

        response = dialog.run()
        position = dialog.get_position()
        amount   = dialog.get_amount()
        dialog.destroy()

        if response != gtk.RESPONSE_OK:
            return

        config.subtitle_insert.position = position
        config.subtitle_insert.amount   = amount

        if page.project.times:
            start_row = page.view.get_selected_rows()[0]
            if position == Position.BELOW:
                start_row += 1
        else:
            start_row = 0
        rows = range(start_row, start_row + amount)

        page.project.insert_subtitles(rows)
        page.view.select_rows(rows)

    def on_invert_selection_activated(self, *args):
        """Invert the current selection."""

        page = self.get_current_page()

        selected_rows = page.view.get_selected_rows()
        rows = range(0, len(page.project.times))
        for row in selected_rows:
            rows.remove(row)

        page.view.select_rows(rows)
        page.view.grab_focus()

    def on_paste_texts_activated(self, *args):
        """Paste texts from the clipboard."""

        page     = self.get_current_page()
        rows     = page.view.get_selected_rows()
        col      = page.view.get_focus()[1]
        document = page.text_column_to_document(col)

        try:
            rows = page.project.paste_texts(rows[0], document)
        except FitError:
            dialog = PasteFitErrorDialog(self.window)
            dialog.run()
            dialog.destroy()
            return

        page.view.select_rows(rows)

    def on_remove_subtitles_activated(self, *args):
        """Remove selected subtitles."""

        page = self.get_current_page()
        col  = page.view.get_focus()[1]
        rows = page.view.get_selected_rows()

        page.project.remove_subtitles(rows)

        if page.project.times:
            row = min(rows[0], len(page.project.times) - 1)
            page.view.set_focus(row, col)

    def on_select_all_activated(self, *args):
        """Select all subtitles."""

        page = self.get_current_page()
        selection = page.view.get_selection()
        selection.select_all()
        page.view.grab_focus()

    def on_unselect_all_activated(self, *args):
        """Unselect all subtitles."""

        page = self.get_current_page()
        selection = page.view.get_selection()
        selection.unselect_all()
        page.view.grab_focus()

    def on_view_cell_edited(self, cell_renderer, value, row, col):
        """Finish editing of a cell."""

        gtklib.set_cursor_busy(self.window)
        self._set_sensitivities(True)
        self.set_status_message(None)
        page = self.get_current_page()

        # value is by default a string, which cannot be empty to be a frame.
        if page.edit_mode == Mode.FRAME and col in (SHOW, HIDE, DURN):
            try:
                value = int(value)
            except ValueError:
                self.set_sensitivities(page)
                gtklib.set_cursor_normal(self.window)
                return

        if col in (SHOW, HIDE, DURN):
            gtklib.set_cursor_busy(self.window)
            if page.edit_mode == Mode.TIME:
                new_row = page.project.set_time(row, col - 1, value)
            elif page.edit_mode == Mode.FRAME:
                new_row = page.project.set_frame(row, col - 1, value)
            if new_row != row:
                page.view.set_focus(new_row, col)
        elif col in (MTXT, TTXT):
            page.project.set_text(row, col - 4, value)
            self.set_sensitivities(page)
            self.set_character_status(page)

        gtklib.set_cursor_normal(self.window)

    def on_view_cell_editing_canceled(self, cell_renderer, editor):
        """Set GUI properties for editing."""

        self._set_sensitivities(True)
        self.set_status_message(None)

    def on_view_cell_editing_started(self, cell_renderer, editor, row, col):
        """Set GUI properties for editing."""

        self._set_sensitivities(False)
        page = self.get_current_page()
        view = page.view
        row = int(row)

        # Put a help message in the statusbar.
        message = _('Use Alt+Arrow for moving to edit an adjacent cell')
        if col in (MTXT, TTXT):
            message = _('Use Ctrl+Return for line-break')
        self.set_status_message(message, False)

        min_row = 0
        max_row = len(page.project.times) - 1

        # Determine the visible columns.
        visible_cols = []
        for i in range(1, 6):
            if view.get_column(i).get_visible():
                visible_cols.append(i)
        min_col = min(visible_cols)
        max_col = max(visible_cols)

        def on_key_press_event(editor, event):
            """Move to edit an adjacent cell on Alt+Arrow key press."""

            accel_masks = gtk.gdk.MOD1_MASK
            keymap = gtk.gdk.keymap_get_default()

            args = event.hardware_keycode, event.state, event.group
            output = keymap.translate_keyboard_state(*args)
            keyval, egroup, level, consumed = output
            keyname = gtk.gdk.keyval_name(keyval)

            if not event.state & ~consumed & accel_masks:
                return
            if keyname not in ('Up', 'Down', 'Left', 'Right'):
                return

            # Do not move if rows will be reordered.
            if col == SHOW:
                value = editor.get_text()
                if page.project.get_needs_resort(row, value):
                    return

            editor.emit('editing-done')
            next_col = col
            next_row = row

            # Determine next row or column.
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

            while gtk.events_pending():
                gtk.main_iteration()
            view.set_cursor(next_row, view.get_column(next_col), True)

        editor.connect('key-press-event', on_key_press_event)

    def _set_sensitivities(self, sensitive):
        """Set sensitivity of menubar and toolbar actions."""

        action_groups = self.uim.get_action_groups()
        for action_group in action_groups:
            action_group.set_sensitive(sensitive)

        self.uim.get_widget('/ui/menubar').set_sensitive(sensitive)
        self.uim.get_widget('/ui/main_toolbar').set_sensitive(sensitive)

        get_toolbar = gtklib.get_parent_widget
        video_toolbar = get_toolbar(self.video_file_button, gtk.Toolbar)
        video_toolbar.set_sensitive(sensitive)
