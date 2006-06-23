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


"""Managing revertable actions."""


from gettext import gettext as _

import gtk

from gaupol.base.util    import listlib
from gaupol.gtk.icons    import *
from gaupol.gtk.delegate import Delegate, UIMAction
from gaupol.gtk.util     import gtklib


class RedoActionAction(UIMAction):

    """Redoing revertable actions."""

    action_item = (
        'redo_action',
        gtk.STOCK_REDO,
        _('_Redo'),
        '<shift><control>Z',
        _('Redo the last undone action'),
        'on_redo_action_activate'
    )

    paths = ['/ui/menubar/edit/redo']
    widgets = ['_redo_button']

    @classmethod
    def is_doable(cls, app, page):
        """Return action doability."""

        if page is None:
            return False
        return page.project.can_redo()


class UndoActionAction(UIMAction):

    """Undoing revertable actions."""

    action_item = (
        'undo_action',
        gtk.STOCK_UNDO,
        _('_Undo'),
        '<control>Z',
        _('Undo the last done action'),
        'on_undo_action_activate'
    )

    paths = ['/ui/menubar/edit/undo']
    widgets = ['_undo_button']

    @classmethod
    def is_doable(cls, app, page):
        """Return action doability."""

        if page is None:
            return False
        return page.project.can_undo()


class ActionDelegate(Delegate):

    """Managing revertable actions."""

    def _reload_updated_data(self, action):
        """Reload data updated by action."""

        page = self.get_current_page()
        inserted_rows = action.inserted_rows[:]
        removed_rows  = action.removed_rows[:]
        updated_rows  = action.updated_rows[:]
        updated_positions  = action.updated_positions[:]
        updated_main_texts = action.updated_main_texts[:]
        updated_tran_texts = action.updated_tran_texts[:]

        if inserted_rows or removed_rows:
            first_row = min(inserted_rows + removed_rows)
            page.reload_after(first_row)
            for data in (
                updated_rows,
                updated_positions,
                updated_main_texts,
                updated_tran_texts,
            ):
                for i in reversed(range(len(data))):
                    if data[i] >= first_row:
                        data.pop(i)

        if updated_rows:
            page.reload_rows(updated_rows)
            for data in (
                updated_positions,
                updated_main_texts,
                updated_tran_texts,
            ):
                for i in reversed(range(len(data))):
                    if data[i] in updated_rows:
                        data.pop(i)

        if updated_positions:
            page.reload_columns([SHOW, HIDE, DURN], updated_positions)
        if updated_main_texts:
            page.reload_columns([MTXT], updated_main_texts)
        if updated_tran_texts:
            page.reload_columns([TTXT], updated_tran_texts)

    def _show_updated_data(self, action):
        """Focus, select and scroll to data updated by action."""

        page = self.get_current_page()
        if not page.project.times:
            return

        changed_rows = []
        if action.inserted_rows or action.removed_rows:
            first_row = min(action.inserted_rows + action.removed_rows)
            changed_rows += range(first_row, len(page.project.times))
        changed_rows += action.updated_rows
        changed_rows += action.updated_positions
        changed_rows += action.updated_main_texts
        changed_rows += action.updated_tran_texts
        changed_rows = listlib.sorted_unique(changed_rows)
        if not changed_rows:
            return

        focus_row = min(changed_rows)
        if action.updated_positions:
            focus_col = SHOW
        elif action.updated_main_texts:
            focus_col = MTXT
        elif action.updated_tran_texts:
            focus_col = TTXT
        else:
            focus_col = MTXT

        try:
            page.view.set_focus(focus_row, focus_col)
        except (TypeError, ValueError):
            pass
        page.view.select_rows(changed_rows)
        try:
            page.view.scroll_to_row(focus_row)
        except TypeError:
            pass

    def on_project_action_done(self, action):
        """Update view after doing action."""

        self._reload_updated_data(action)

    def on_project_action_redone(self, action):
        """Update view after redoing action."""

        self._reload_updated_data(action)
        self._show_updated_data(action)

    def on_project_action_undone(self, action):
        """Update view after undoing action."""

        self._reload_updated_data(action)
        self._show_updated_data(action)

    def on_redo_action_activate(self, *args):
        """Redo the last undone action."""

        self.redo()

    def on_redo_button_clicked(self, *args):
        """Redo the last undone action."""

        self.redo()

    def on_undo_action_activate(self, *args):
        """Undo the last redone action."""

        self.undo()

    def on_undo_button_clicked(self, *args):
        """Undo the last redone action."""

        self.undo()

    def redo(self, count=1):
        """Redo actions."""

        gtklib.set_cursor_busy(self._window)
        page = self.get_current_page()
        page.project.redo(count)
        page.view.grab_focus()
        self.set_sensitivities(page)
        gtklib.set_cursor_normal(self._window)

    def undo(self, count=1):
        """Undo actions."""

        gtklib.set_cursor_busy(self._window)
        page = self.get_current_page()
        page.project.undo(count)
        page.view.grab_focus()
        self.set_sensitivities(page)
        gtklib.set_cursor_normal(self._window)
