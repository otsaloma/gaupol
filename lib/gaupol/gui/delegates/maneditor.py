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


"""Manual editing of subtitle data."""


try:
    from psyco.classes import *
except ImportError:
    pass

from gaupol.gui.constants import NO, SHOW, HIDE, DURN, ORIG, TRAN
from gaupol.gui.delegates.delegate import Delegate


class ManualEditAction(object):

    """Manual edit action for subtitle data."""
    
    def __init__(self, project, old_value, new_value, row, col):
        
        self.project   = project
        self.old_value = old_value
        self.new_value = new_value
        self.row       = row
        self.col       = col

        if col == TRAN:
            self.document = 'translation'
        else:
            self.document = 'main'

        edit_mode = project.edit_mode
        subtitle  = row + 1

        DESCRIPTIONS = [
            None,
            _('editing show %s of subtitle %d')     % (edit_mode, subtitle),
            _('editing hide %s of subtitle %d')     % (edit_mode, subtitle),
            _('editing duration of subtitle %d')    % subtitle,
            _('editing text of subtitle %d')        % subtitle,
            _('editing translation of subtitle %d') % subtitle,
        ]
        
        self.description = DESCRIPTIONS[col]
        
    def do(self):
        """Do action."""

        self._set_value(self.new_value)

    def redo(self):
        """Redo action."""
        
        self.do()

    def _set_value(self, value):
        """Set value to data."""

        store = self.project.tree_view.get_model()
        
        if self.col in [SHOW, HIDE, DURN]:
            section = self.project.edit_mode + 's'
            col = self.col - 1
        else:
            section = 'texts'
            col = self.col - 4

        row = store[self.row][NO] - 1
            
        self.project.data.set_single_value(section, col, row, value)
        self.project.reload_tree_view_data_in_row(self.row)
        
    def undo(self):
        """Undo action."""

        self._set_value(self.old_value)


class ManualEditor(Delegate):

    """Manual editor for subtitle data."""

    def on_tree_view_cell_edited(self, project, new_value, row, col):
        """Edit value in tree view cell."""

        self._set_action_sensitivities(True)
        self.set_status_message(None)
    
        store = project.tree_view.get_model()

        # new_value is by default a string.
        if project.edit_mode == 'frame' and col in [SHOW, HIDE, DURN]:
            new_value = int(new_value)

        old_value = store[row][col]

        if old_value == new_value:
            return

        action = ManualEditAction(project, old_value, new_value, row, col)
        self.do_action(project, action)

    def on_tree_view_cell_editing_started(self, project, col):
        """Set menubar and toolbar action insensitive while editing."""

        self._set_action_sensitivities(False)

        if col in [ORIG, TRAN]:
            message = _('Use Ctrl+Return for line-break')
            self.set_status_message(message, False)

    def _set_action_sensitivities(self, sensitive):
        """Set  sensitivity of menubar and toolbar actions."""

        action_groups = self.uim.get_action_groups()
        for group in action_groups:
            group.set_sensitive(sensitive)

        self.uim.get_widget('/ui/toolbar').set_sensitive(sensitive)
        self.uim.get_widget('/ui/menubar').set_sensitive(sensitive)
