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

from gaupol.gui.delegates.delegate import Delegate


class RowEditor(Delegate):

    """Performer of actions on entire rows (subtitles)."""

    def on_insert_subtitles_activated(self, *args):
        """Insert blank subtitles at selection."""
        
        pass

    def on_invert_selection_activated(self, *args):
        """Invert current selection."""

        project = self.get_current_project()
        store = project.tree_view.get_model()
        selection = project.tree_view.get_selection()
        
        rows = selection.get_selected_rows()[1]
        selection.select_all()
        
        for row in rows:
            selection.unselect_path(row)
        
    def on_remove_subtitles_activated(self, *args):
        """Remove selected subtitles."""

        pass

    def on_select_all_activated(self, *args):
        """Select all subtitles."""

        project = self.get_current_project()
        selection = project.tree_view.get_selection()
        selection.select_all()

    def on_unselect_all_activated(self, *args):
        """Unselect all subtitles."""

        project = self.get_current_project()
        selection = project.tree_view.get_selection()
        selection.unselect_all()
