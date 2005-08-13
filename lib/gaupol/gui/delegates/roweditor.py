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


"""Performer of actions on entire rows (subtitles)."""


try:
    from psyco.classes import *
except ImportError:
    pass

import gtk

from gaupol.gui.constants import NO, SHOW, HIDE, DURN, TEXT, TRAN
from gaupol.gui.delegates.delegate import Delegate
from gaupol.gui.delegates.durmanager import DURAction
from gaupol.gui.dialogs.insertsub import InsertSubtitleDialog


class RowInsertAction(DURAction):

    """Action to insert subtitles."""
    
    def __init__(self, project, position, amount):

        self.project = project
        self.position = position
        self.amount = amount

        self.document    = 'both'
        self.description = _('Inserting rows')

        self.store_rows = self.project.get_selected_store_rows()
        self.data_rows = []

    def do(self):
        """Insert rows."""

        ABOVE, BELOW = 0, 1
        
        store_rows = self.store_rows
        if self.position == ABOVE:
            start_row = self.project.get_data_row(store_rows[0])
        elif self.position == BELOW:
            start_row = self.project.get_data_row(store_rows[-1]) + 1

        self.project.data.insert_subtitles(start_row, self.amount)

        self.project.reload_all_data()
        
        selection = self.project.tree_view.get_selection()
        selection.unselect_all()
        
        self.data_rows = []
        for row in range(start_row, start_row + self.amount):
            store_row = self.project.get_store_row(row)
            selection.select_path(store_row)
            self.data_rows.append(row)

    def undo(self):
    
        store    = self.project.tree_view.get_model()
        data     = self.project.data

        data.remove_subtitles(self.data_rows)
        
        for data_row in self.data_rows:
            store_row = self.project.get_store_row(data_row)
            store.remove(store.get_iter(store_row))

        self.project.reload_data_in_columns([NO])



class RowRemoveAction(DURAction):

    """Action to remove selected subtitles."""
    
    def __init__(self, project):

        self.project = project
        self.data_rows = project.get_selected_data_rows()

        texts  = project.data.texts
        times  = project.data.times
        frames = project.data.frames

        # Save data.
        self.removed_texts  = [texts[row]  for row in self.data_rows]
        self.removed_times  = [times[row]  for row in self.data_rows]
        self.removed_frames = [frames[row] for row in self.data_rows]

        self.document    = 'both'
        self.description = _('Removing rows')

        self.top_store_row = self.project.get_selected_store_rows()[0]

    def do(self):
        """Remove rows."""

        top_store_row = self.top_store_row

        tree_col = self.project.tree_view.get_cursor()[1]
        store    = self.project.tree_view.get_model()
        data     = self.project.data

        data.remove_subtitles(self.data_rows)
        
        for data_row in self.data_rows:
            store_row = self.project.get_store_row(data_row)
            store.remove(store.get_iter(store_row))

        self.project.reload_data_in_columns([NO])

        selection = self.project.tree_view.get_selection()
        selection.unselect_all()
        selection.select_path(top_store_row)

        self.project.tree_view.set_cursor(top_store_row, tree_col)

    def undo(self):
        """Restore rows."""
        
        store = self.project.tree_view.get_model()
        data  = self.project.data

        data_rows = self.data_rows[:]
        data_rows.sort()
        
        for data_row in data_rows:

            i = self.data_rows.index(data_row)
            data.texts.insert(data_row, self.removed_texts[i])
            data.times.insert(data_row, self.removed_times[i])
            data.frames.insert(data_row, self.removed_frames[i])
            
            store_row = self.project.get_store_row(data_row)

            store.append()

        self.project.reload_all_data()


class RowEditor(Delegate):

    """Performer of actions on entire rows (subtitles)."""

    def on_insert_subtitles_activated(self, *args):
        """Insert blank subtitles at selection."""
        
        positions = ['above', 'below']
        position = self.config.get('insert_subtitles', 'position')
        amount   = self.config.getint('insert_subtitles', 'amount')
        
        dialog = InsertSubtitleDialog(self.window)
        
        dialog.set_amount(amount)
        dialog.set_position(positions.index(position))
        
        response = dialog.run()
        position = dialog.get_position()
        amount   = dialog.get_amount()

        dialog.destroy()

        if response != gtk.RESPONSE_OK:
            return

        self.config.set('insert_subtitles', 'position', positions[position])
        self.config.setint('insert_subtitles', 'amount', amount)

        project = self.get_current_project()
        action = RowInsertAction(project, position, amount)
        self.do_action(project, action)

    def on_invert_selection_activated(self, *args):
        """Invert current selection."""

        project = self.get_current_project()
        store = project.tree_view.get_model()
        selection = project.tree_view.get_selection()
        
        rows = selection.get_selected_rows()[1]
        selection.select_all()
        
        for row in rows:
            selection.unselect_path(row)

        project.tree_view.grab_focus()
        
    def on_remove_subtitles_activated(self, *args):
        """Remove selected subtitles."""

        project = self.get_current_project()
        action = RowRemoveAction(project)
        self.do_action(project, action)

    def on_select_all_activated(self, *args):
        """Select all subtitles."""

        project = self.get_current_project()
        selection = project.tree_view.get_selection()
        selection.select_all()
        project.tree_view.grab_focus()

    def on_unselect_all_activated(self, *args):
        """Unselect all subtitles."""

        project = self.get_current_project()
        selection = project.tree_view.get_selection()
        selection.unselect_all()
        project.tree_view.grab_focus()
