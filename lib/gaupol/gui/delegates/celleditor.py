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


"""Editing a single value of subtitle data."""


try:
    from psyco.classes import *
except ImportError:
    pass

from gaupol.constants import MODE
from gaupol.gui.colcons import *
from gaupol.gui.delegates.delegate import Delegate
from gaupol.gui.delegates.durmanager import DURAction


class CellEditAction(DURAction):

    """Action for editing a single value of subtitle data."""
    
    def __init__(self, project, old_value, new_value, row, col):
        
        self.project = project

        self._row = row
        self._col = col
        
        self._old_value = old_value
        self._new_value = new_value

        subtitle = row + 1

        descriptions = [
            None,
            _('Editing show'),
            _('Editing hide'),
            _('Editing duration'),
            _('Editing text'),
            _('Editing translation'),
        ]
        
        self.description = descriptions[col]
        self.documents = [project.get_document_type(col)]
        
    def do(self):
        """Do editing."""

        self._set_value(self._new_value)

    def _set_value(self, value):
        """Set value to data."""

        project = self.project
        model = project.tree_view.get_model()
        data = project.data
        data_col = project.get_data_column(self._col)
        
        if self._col in [SHOW, HIDE, DURN]:
            
            if project.edit_mode == MODE.TIME:
                new_row = data.set_time(self._row, data_col, value)
            if project.edit_mode == MODE.FRAME:
                new_row = data.set_frame(self._row, data_col, value)
                
        elif self._col in [TEXT, TRAN]:
        
            data.set_text(self._row, data_col, value)
            new_row = self._row

        # Reload changed data.
        if new_row == self._row:
            project.reload_data_in_row(self._row)
        else:
            project.reload_data_between_rows(self._row, new_row)

            # Set focus to new location of row.
            tree_view_column = project.tree_view.get_column(self._col)
            project.tree_view.set_cursor(new_row, tree_view_column)

            # Instance variable pointing to row needs to be updated to be
            # able to undo at the correct row.
            self._row = new_row
        
    def undo(self):
        """Undo editing."""

        self._set_value(self._old_value)


class CellEditor(Delegate):

    """Editing a single value of subtitle data."""

    def on_edit_cell_activated(self, *args):
        """Edit focused cell."""
        
        tree_view = self.get_current_project().tree_view
        row, tree_view_column = tree_view.get_cursor()
        tree_view.set_cursor_on_cell(row, tree_view_column, None, True)

    def on_tree_view_cell_edited(self, project, new_value, row, col):
        """Finish editing of a TreeView cell."""

        self._set_sensitivities(True)
        self.set_status_message(None)

        model = project.tree_view.get_model()

        # new_value is by default a string.
        if project.edit_mode == MODE.FRAME and col in [SHOW, HIDE, DURN]:
            new_value = int(new_value)

        old_value = model[row][col]

        if old_value == new_value:
            return

        action = CellEditAction(project, old_value, new_value, row, col)
        self.do_action(project, action)

    def on_tree_view_cell_editing_started(self, project, col):
        """Set GUI properties for editing."""

        self._set_sensitivities(False)

        if col in [TEXT, TRAN]:
            message = _('Use Ctrl+Enter for line-break')
            self.set_status_message(message, False)

    def _set_sensitivities(self, sensitive):
        """Set  sensitivity of menubar and toolbar actions."""

        action_groups = self.uim.get_action_groups()
        for action_group in action_groups:
            action_group.set_sensitive(sensitive)

        self.uim.get_widget('/ui/toolbar').set_sensitive(sensitive)
        self.uim.get_widget('/ui/menubar').set_sensitive(sensitive)
