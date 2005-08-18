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

from gaupol.constants import TYPE
from gaupol.gui.colcons import *
from gaupol.gui.delegates.delegate import Delegate
from gaupol.gui.util import gui


class DURAction(object):

    """Base class for actions, that can be done, undone and redone."""
    
    def __init__(self, *args):

        self.project = None
        
        # One line description.
        self.description = None

        # List of documents affected.
        self.document = []

        # TreeView properties that can be restored.
        self.focus_row     = None
        self.focus_col     = None
        self.selected_rows = None
        
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

    """Handling of do, undo and redo actions."""

    def do_action(self, project, action):
        """Do action and update things affected."""

        self._save_tree_view_properties(project, action)
        
        action.do()

        project.undoables.insert(0, action)

        # Remove oldest undo action if level limit is exceeded.
        if self.config.getboolean('editor', 'limit_undo'):
            undo_levels = self.config.getint('editor', 'undo_levels')
            while len(project.undoables) > undo_levels:
                project.undoables.pop()

        project.redoables = []
        self._shift_changed_value(project, action, 1)

        self.set_sensitivities(project)

    def on_redo_activated(self, *args):
        """Redo most recently undone action."""

        self.uim.get_action('/ui/redo_popup/redo-0').activate()

    def on_redo_item_activated(self, action):
        """Redo action and all newer actions."""

        gui.set_cursor_busy(self.window)

        name  = action.get_name()
        index = int(name.split('-')[-1])

        project = self.get_current_project()

        for i in range(index + 1):
            self.redo_action(project, project.redoables[0])

        gui.set_cursor_normal(self.window)
        
    def on_undo_activated(self, *args):
        """Undo most recently done action."""
        
        self.uim.get_action('/ui/undo_popup/undo-0').activate()

    def on_undo_item_activated(self, action):
        """Undo action and all newer actions."""

        gui.set_cursor_busy(self.window)

        name  = action.get_name()
        index = int(name.split('-')[-1])

        project = self.get_current_project()

        for i in range(index + 1):
            self.undo_action(project, project.undoables[0])

        gui.set_cursor_normal(self.window)

    def redo_action(self, project, action):
        """Redo action and update things affected."""

        action.redo()

        self._restore_tree_view_properties(project, action)

        project.undoables.insert(0, action)

        # Remove oldest undo action if level limit is exceeded.
        if self.config.getboolean('editor', 'limit_undo'):
            undo_levels = self.config.getint('editor', 'undo_levels')
            while len(project.undoables) > undo_levels:
                project.undoables.pop()

        project.redoables.pop(0)
        self._shift_changed_value(project, action, 1)

        self.set_sensitivities(project)

    def _restore_tree_view_properties(self, project, action):
        """Restore TreeView properties."""

        tree_view = project.tree_view
        row = action.focus_row
        tree_view_column = tree_view.get_column(action.focus_col)

        # Focus
        try:
            project.tree_view.set_cursor(row, tree_view_column)
        except TypeError:
            pass

        # Scroll position
        try:
            tree_view.scroll_to_cell(row, tree_view_column, True, 0.5, 0)
        except TypeError:
            pass
        
        # Selection
        selection = tree_view.get_selection()
        selection.unselect_all()
        for row in action.selected_rows:
            try:
                selection.select_path(row)
            except TypeError:
                pass

    def _save_tree_view_properties(self, project, action):
        """Save TreeView properties."""

        # Focus
        action.focus_row, action.focus_col = project.get_focus()[:2]

        # Selection
        action.selected_rows = project.get_selected_rows()

    def _shift_changed_value(self, project, action, shift):
        """
        Shift value(s) of document(s) changed variables.
        
        Raise ValueError if action.documents has an invalid value.
        """
        
        if TYPE.MAIN in action.documents and \
           TYPE.TRAN in action.documents:
            project.main_changed += shift
            project.tran_changed += shift
            
        elif TYPE.MAIN in action.documents:
            project.main_changed += shift
            
        elif TYPE.TRAN in action.documents:
            project.tran_active = True
            project.tran_changed += shift
            
        else:
            raise ValueError('What document was changed?')

    def undo_action(self, project, action):
        """Undo action and update things affected."""

        action.undo()

        self._restore_tree_view_properties(project, action)

        project.redoables.insert(0, action)

        # Remove oldest redo action if level limit is exceeded.
        if self.config.getboolean('editor', 'limit_undo'):
            undo_levels = self.config.getint('editor', 'undo_levels')
            while len(project.redoables) > undo_levels:
                project.redoables.pop()

        project.undoables.pop(0)
        self._shift_changed_value(project, action, -1)

        self.set_sensitivities(project)
