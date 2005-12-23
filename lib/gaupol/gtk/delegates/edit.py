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

from gaupol.constants        import Mode
from gaupol.gtk.colconstants import *
from gaupol.gtk.delegates    import Action, Delegate
from gaupol.gtk.util         import gui


class ClipboardAction(Action):

    """Base class for clipboard actions."""

    @classmethod
    def is_doable(cls, application, page):
        """Return whether action can or cannot be done."""

        if page is None:
            return False

        selection = bool(page.view.get_selected_rows())
        focus = page.view.get_focus()[1] in (MTXT, TTXT)
        return bool(selection and focus)


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

    uim_paths = ['/ui/menubar/edit/clear']


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

    uim_paths = ['/ui/menubar/edit/copy']


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

    uim_paths = ['/ui/menubar/edit/cut']


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

    uim_paths = ['/ui/menubar/edit/paste']


class EditValueAction(Action):

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


class EditDelegate(Delegate):

    """Editing subtitle data."""

    def on_clear_texts_activated(self, *args):
        """Paste texts from the clipboard."""

        page = self.get_current_page()
        rows = page.view.get_selected_rows()
        col  = page.view.get_focus()[1]
        doc  = col - 4

        page.project.clear_texts(rows, doc)
        self.set_sensitivities(page)

    def on_copy_texts_activated(self, *args):
        """Cut the selected texts to the clipboard."""

        page = self.get_current_page()
        rows = page.view.get_selected_rows()
        col  = page.view.get_focus()[1]
        doc  = col - 4

        page.project.copy_texts(rows, doc)

        # Additionally, put a string representation of the Gaupol internal
        # clipboard to the X clipboard.
        text = page.project.clipboard.get_data_as_string()
        self.clipboard.set_text(text)

        self.set_sensitivities(page)

    def on_cut_texts_activated(self, *args):
        """Cut the selected texts to the clipboard."""

        page = self.get_current_page()
        rows = page.view.get_selected_rows()
        col  = page.view.get_focus()[1]
        doc  = col - 4

        page.project.cut_texts(rows, doc)

        # Additionally, put a string representation of the Gaupol internal
        # clipboard to the X clipboard.
        text = page.project.clipboard.get_data_as_string()
        self.clipboard.set_text(text)

        self.set_sensitivities(page)

    def on_edit_value_activated(self, *args):
        """Edit the focused cell."""

        view = self.get_current_page().view
        row, tree_view_column = view.get_cursor()
        view.set_cursor(row, tree_view_column, True)

    def on_paste_texts_activated(self, *args):
        """Paste texts from the clipboard."""

        page = self.get_current_page()
        rows = page.view.get_selected_rows()
        col  = page.view.get_focus()[1]
        doc  = col - 4

        # FIX: Added subs?

        page.project.paste_texts(rows[0], doc)
        self.set_sensitivities(page)

    def on_view_cell_edited(self, cell_renderer, value, row, col):
        """Finish editing of a cell."""

        gui.set_cursor_busy(self.window)
        self._set_sensitivities(True)
        self.set_status_message(None)
        page = self.get_current_page()

        # value is by default a string.
        if page.edit_mode == Mode.FRAME and col in (SHOW, HIDE, DURN):
            value = int(value)

        if col in (SHOW, HIDE, DURN):
            gui.set_cursor_busy(self.window)
            if page.edit_mode == Mode.TIME:
                page.project.set_time(row, col - 1, value)
            if page.edit_mode == Mode.FRAME:
                page.project.set_frame(row, col - 1, value)
            gui.set_cursor_normal(self.window)
        elif col in (MTXT, TTXT):
            page.project.set_text(row, col - 4, value)

        self.set_sensitivities(page)
        gui.set_cursor_normal(self.window)

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

        # Determine the visible edge columns that the user cannot move beyond.
        min_col = SHOW
        max_col = TTXT
        for i in range(1, 6):
            if view.get_column(i).get_visible():
                min_col = i
                break
        for i in reversed(range(1, 6)):
            if view.get_column(i).get_visible():
                max_col = i
                break

        def on_key_press_event(editor, event):
            """Move to edit an adjacent cell on Alt+Arrow key press."""

            accel_masks = gtk.gdk.MOD1_MASK
            keymap = gtk.gdk.keymap_get_default()
            keyval, egroup, level, consumed = keymap.translate_keyboard_state(
                event.hardware_keycode, event.state, event.group
            )

            if not event.state & ~consumed & accel_masks:
                return
            if keyval not in (65361, 65362, 65363, 65364):
                return

            editor.emit('editing-done')
            next_col = col
            next_row = row

            if keyval == 65361: # Left
                next_col = max(min_col, col - 1)
            elif keyval == 65362: # Up
                next_row = max(min_row, row - 1)
            elif keyval == 65363: # Right
                next_col = min(max_col, col + 1)
            elif keyval == 65364: # Down
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

        self.uim.get_widget('/ui/toolbar').set_sensitive(sensitive)
        self.uim.get_widget('/ui/menubar').set_sensitive(sensitive)
