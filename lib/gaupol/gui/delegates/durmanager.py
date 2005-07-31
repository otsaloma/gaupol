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


"""Handling of do, undo and redo actions."""


try:
    from psyco.classes import *
except ImportError:
    pass

from gaupol.gui.constants import NO, SHOW, HIDE, DURN, ORIG, TRAN
from gaupol.gui.delegates.delegate import Delegate
from gaupol.gui.util import gui


class DURAction(object):

    """Base class for actions, that can be done, undone and redone."""
    
    def __init__(self, *args):
        
        self.description = None
        self.document    = None

        # Tree view properties that can be restored.
        self.focus_data_row  = None
        self.focus_store_col = None
        self.sel_data_rows   = None
        self.sort_col        = None
        self.sort_order      = None
        
    def do(self):
        """Do action."""
        pass

    def redo(self):
        """Redo action."""
        
        self.do()
        
    def undo(self):
        """Undo action."""
        pass


class DURManager(Delegate):

    """Manager for actions, that can be done, undone and redone."""

    def do_action(self, project, action):
        """Do action and update things affected."""

        self._save_tree_view_properties(project, action)
        
        action.do()

        project.undoables.insert(0, action)

        if self.config.getboolean('editor', 'limit_undo'):
            undo_levels = self.config.getint('editor', 'undo_levels')
            while len(project.undoables) > undo_levels:
                project.undoables.pop()

        project.redoables = []

        if action.document == 'main':
            project.main_changed += 1
        elif action.document == 'translation':
            project.tran_changed += 1

        self.set_sensitivities(project)

    def on_redo_activated(self, *args):
        """Redo most recently undone action."""

        self.uim.get_action('/ui/redo_popup/redo-0').activate()

    def on_redo_button_clicked(self, *args):
        """Redo most recently undone action."""

        self.uim.get_action('/ui/redo_popup/redo-0').activate()

    def on_redo_item_activated(self, action):
        """Redo action and all newer actions."""

        gui.set_cursor_busy(self.window)

        name  = action.get_name()
        index = int(name.split('-')[-1])

        project = self.get_current_project()
        project.tree_view.freeze_child_notify()

        for i in range(index + 1):
            self.redo_action(project, project.redoables[0])

        project.tree_view.thaw_child_notify()
        gui.set_cursor_normal(self.window)
        
    def on_undo_activated(self, *args):
        """Undo most recently done action."""
        
        self.uim.get_action('/ui/undo_popup/undo-0').activate()

    def on_undo_button_clicked(self, *args):
        """Undo most recently done action."""
        
        self.uim.get_action('/ui/undo_popup/undo-0').activate()

    def on_undo_item_activated(self, action):
        """Undo action and all newer actions."""

        gui.set_cursor_busy(self.window)

        name  = action.get_name()
        index = int(name.split('-')[-1])

        project = self.get_current_project()
        project.tree_view.freeze_child_notify()

        for i in range(index + 1):
            self.undo_action(project, project.undoables[0])

        project.tree_view.thaw_child_notify()
        gui.set_cursor_normal(self.window)

    def redo_action(self, project, action):
        """Redo action and update things affected."""

        action.redo()

        self._restore_tree_view_properties(project, action)

        project.undoables.insert(0, action)

        if self.config.getboolean('editor', 'limit_undo'):
            undo_levels = self.config.getint('editor', 'undo_levels')
            while len(project.undoables) > undo_levels:
                project.undoables.pop()

        project.redoables.pop(0)
        
        if action.document == 'main':
            project.main_changed += 1
        elif action.document == 'translation':
            project.tran_changed += 1

        self.set_sensitivities(project)

    def _restore_tree_view_properties(self, project, action):
        """Restore tree view properties."""

        # Focus
        store_row = project.get_store_row(action.focus_data_row)
        tree_col  = project.tree_view.get_column(action.focus_store_col)
        project.tree_view.set_cursor(store_row, tree_col)

        # Selection
        selection = project.tree_view.get_selection()
        selection.unselect_all()
        for row in action.sel_data_rows:
            store_row = project.get_store_row(row)
            selection.select_path(store_row)

        # Sort order and column
        store = project.tree_view.get_model()
        store.set_sort_column_id(action.sort_col, action.sort_order)

    def _save_tree_view_properties(self, project, action):
        """Save tree view properties."""

        # Focus
        action.focus_data_row  = project.get_data_focus()[1]
        action.focus_store_col = project.get_store_focus()[1]

        # Selection
        action.sel_data_rows = project.get_selected_data_rows()
        
        # Sort order and column
        store = project.tree_view.get_model()
        action.sort_col, action.sort_order = store.get_sort_column_id()

    def undo_action(self, project, action):
        """Undo action and update things affected."""

        action.undo()

        self._restore_tree_view_properties(project, action)

        project.redoables.insert(0, action)

        if self.config.getboolean('editor', 'limit_undo'):
            undo_levels = self.config.getint('editor', 'undo_levels')
            while len(project.redoables) > undo_levels:
                project.redoables.pop()

        project.undoables.pop(0)

        if action.document == 'main':
            project.main_changed -= 1
        elif action.document == 'translation':
            project.tran_changed -= 1

        self.set_sensitivities(project)
