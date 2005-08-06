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

from gaupol.gui.constants import NO, SHOW, HIDE, DURN, ORIG, TRAN
from gaupol.gui.delegates.delegate import Delegate
from gaupol.gui.delegates.durmanager import DURAction


class CellEditAction(DURAction):

    """Action for editing a single value of subtitle data."""
    
    def __init__(self, project, old_value, new_value, store_row, store_col):
        
        self.project = project
        
        self.old_value = old_value
        self.new_value = new_value
        
        self.focus_data_row  = project.get_data_row(store_row)
        self.focus_store_col = store_col

        documents = ['main'] * 5 + ['translation']
        self.document = documents[store_col]

        edit_mode = project.edit_mode
        subtitle  = store_row + 1

        descriptions = [
            None,
            _('Editing show %s of subtitle %d')     % (edit_mode, subtitle),
            _('Editing hide %s of subtitle %d')     % (edit_mode, subtitle),
            _('Editing duration of subtitle %d')    % subtitle,
            _('Editing text of subtitle %d')        % subtitle,
            _('Editing translation of subtitle %d') % subtitle,
        ]
        
        self.description = descriptions[store_col]
        
    def do(self):
        """Do editing."""

        self._set_value(self.new_value)

    def _set_value(self, value):
        """Set value to data."""

        store    = self.project.tree_view.get_model()
        data     = self.project.data
        data_row = self.focus_data_row
        
        if self.focus_store_col in [SHOW, HIDE, DURN]:
        
            data_col = self.focus_store_col - 1
            
            if self.project.edit_mode == 'time':
                new_data_row = data.set_time(data_row, data_col, value)
            if self.project.edit_mode == 'frame':
                new_data_row = data.set_frame(data_row, data_col, value)
                
        elif self.focus_store_col in [ORIG, TRAN]:
        
            data_col = self.focus_store_col - 4
            data.set_text(data_row, data_col, value)
            new_data_row = data_row

        if new_data_row == data_row:
            self.project.reload_data_in_row(data_row)
        else:
            self.project.reload_data_in_rows(data_row, new_data_row)

            store_col = self.focus_store_col
            store_row = self.project.get_store_row(new_data_row)
            tree_col  = self.project.tree_view.get_column(store_col)
            self.project.tree_view.set_cursor(store_row, tree_col)

        # Instance variable pointing to data row needs to be updated to
        # be able to undo at the correct row.
        self.focus_data_row = new_data_row
        
    def undo(self):
        """Undo editing."""

        self._set_value(self.old_value)


class CellEditor(Delegate):

    """Editor for editing a single value of subtitle data."""

    def on_edit_value_activated(self, *args):
        """Edit value of focused cell."""
        
        pass

    def on_tree_view_cell_edited(self, project, new_value, row, col):
        """Edit value in TreeView cell."""

        self._set_sensitivities(True)
        self.set_status_message(None)
        store = project.tree_view.get_model()

        # new_value is by default a string.
        if project.edit_mode == 'frame' and col in [SHOW, HIDE, DURN]:
            new_value = int(new_value)

        old_value = store[row][col]

        if old_value == new_value:
            return

        action = CellEditAction(project, old_value, new_value, row, col)
        self.do_action(project, action)

    def on_tree_view_cell_editing_started(self, project, col):
        """Set GUI properties for editing."""

        self._set_sensitivities(False)

        if col in [ORIG, TRAN]:
            message = _('Use Ctrl+Enter for line-break')
            self.set_status_message(message, False)

    def _set_sensitivities(self, sensitive):
        """Set  sensitivity of menubar and toolbar actions."""

        action_groups = self.uim.get_action_groups()
        for group in action_groups:
            group.set_sensitive(sensitive)

        self.uim.get_widget('/ui/toolbar').set_sensitive(sensitive)
        self.uim.get_widget('/ui/menubar').set_sensitive(sensitive)
