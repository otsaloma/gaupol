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


"""Searcher to move around in the document."""


try:
    from psyco.classes import *
except ImportError:
    pass

import gtk

from gaupol.gui.delegates.delegate import Delegate
from gaupol.gui.dialogs.goto import GoToDialog


class Searcher(Delegate):

    """Searcher to move around in the document."""

    def on_go_to_subtitle_activated(self, *args):
        """Go to a specific subtitle."""
        
        project = self.get_current_project()
        maximum = len(project.data.times)
        tree_col = project.tree_view.get_cursor()[1]
        
        dialog = GoToDialog(self.window, maximum)
        response = dialog.run()
        subtitle = dialog.get_subtitle()
        dialog.destroy()

        if response != gtk.RESPONSE_OK:
            return
            
        store = project.tree_view.get_model()
        data_row = subtitle - 1
        store_row = project.get_store_row(data_row)
                
        selection = project.tree_view.get_selection()
        selection.unselect_all()
        selection.select_path(store_row)
        
        project.tree_view.set_cursor(store_row, tree_col)
        project.tree_view.scroll_to_cell(store_row, tree_col, True, 0.5, 0)
        
