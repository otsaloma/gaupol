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


"""Managing actions."""


try:
    from psyco.classes import *
except ImportError:
    pass

import gtk

from gaupol.base.util        import listlib
from gaupol.gtk.colconstants import *
from gaupol.gtk.delegates    import Action, Delegate
from gaupol.gtk.util         import gui


class RedoAction(Action):

    """Redoing actions."""

    uim_action_item = (
        'redo_action',
        gtk.STOCK_REDO,
        _('_Redo'),
        '<shift><control>Z',
        _('Redo the last undone action'),
        'on_redo_action_activated'
    )

    uim_paths = ['/ui/menubar/edit/redo']
    widgets   = ['redo_button']

    @classmethod
    def is_doable(cls, application, page):
        """Return whether action can or cannot be done."""

        if page is None:
            return False

        return page.project.can_redo()


class UndoAction(Action):

    """Undoing actions."""

    uim_action_item = (
        'undo_action',
        gtk.STOCK_UNDO,
        _('_Undo'),
        '<control>Z',
        _('Undo the last done action'),
        'on_undo_action_activated'
    )

    uim_paths = ['/ui/menubar/edit/undo']
    widgets   = ['undo_button']

    @classmethod
    def is_doable(cls, application, page):
        """Return whether action can or cannot be done."""

        if page is None:
            return False

        return page.project.can_undo()


class ActionDelegate(Delegate):

    """Managing actions."""

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

    def on_redo_action_activated(self, *args):
        """Redo the last undone action."""

        self.redo(1)

    def on_undo_action_activated(self, *args):
        """Undo the last redone action."""

        self.undo(1)

    def redo(self, amount):
        """Redo actions."""

        gui.set_cursor_busy(self.window)

        page = self.get_current_page()
        page.project.redo(amount)

        self.set_sensitivities()
        page.view.grab_focus()
        gui.set_cursor_normal(self.window)

    def _reload_updated_data(self, action):
        """Reload data updated by action."""

        page = self.get_current_page()

        # Updating is done in an incremental manner. First all rows starting
        # with the first row added or removed are updated. After that data by
        # data rows that need updating, but were not already updated are
        # updated.

        if action.rows_inserted or action.rows_removed:

            first_row = min(action.rows_inserted + action.rows_removed)
            page.reload_between_rows(first_row, -1)

            lists = [
                action.rows_updated,
                action.timing_rows_updated,
                action.main_text_rows_updated,
                action.tran_text_rows_updated,
            ]

            for data in lists:
                for i in reversed(range(len(data))):
                    if data[i] >= first_row:
                        data.pop(i)

        if action.rows_updated:

            page.reload_rows(action.rows_updated)

            lists = [
                action.timing_rows_updated,
                action.main_text_rows_updated,
                action.tran_text_rows_updated,
            ]

            for data in lists:
                for i in reversed(range(len(data))):
                    if data[i] in action.rows_updated:
                        data.pop(i)

        if action.timing_rows_updated:
            page.reload_rows(action.timing_rows_updated)

        if action.main_text_rows_updated:
            page.reload_columns([MTXT], action.main_text_rows_updated)

        if action.tran_text_rows_updated:
            page.reload_columns([TTXT], action.tran_text_rows_updated)

    def _show_updated_data(self, action):
        """Focus, select and scroll to data updated by action."""

        page = self.get_current_page()

        # List all rows that have changed.
        changed_rows  = action.rows_inserted
        changed_rows += action.rows_removed
        changed_rows += action.rows_updated
        changed_rows += action.timing_rows_updated
        changed_rows += action.main_text_rows_updated
        changed_rows += action.tran_text_rows_updated

        changed_rows = listlib.sort_and_remove_duplicates(changed_rows)

        # Locate focus.
        focus_row = min(changed_rows)
        if action.timing_rows_updated:
            focus_col = SHOW
        elif action.main_text_rows_updated:
            focus_col = MTXT
        elif action.tran_text_rows_updated:
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

    def undo(self, amount):
        """Undo actions."""

        gui.set_cursor_busy(self.window)

        page = self.get_current_page()
        page.project.undo(amount)

        self.set_sensitivities()
        page.view.grab_focus()
        gui.set_cursor_normal(self.window)
