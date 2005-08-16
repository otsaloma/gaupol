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


"""Searching for specific data in document."""


try:
    from psyco.classes import *
except ImportError:
    pass

import gtk

from gaupol.gui.delegates.delegate import Delegate
from gaupol.gui.dialogs.jumpto import JumpToSubtitleDialog


class Searcher(Delegate):

    """Searching for specific data in document."""

    def _jump_to_subtitle(self, dialog, subtitle):
        """Select subtitle and scroll to it."""

        project = self.get_current_project()
        tree_view_column = project.get_focus()[2]

        # Save keep open value.
        keep_open = dialog.get_keep_open()
        self.config.setboolean('jump_to_dialog', 'keep_open', keep_open)

        # Jump to last subtitle if subtitle number greater than what exists.
        if subtitle > len(project.data.times):
            subtitle = len(project.data.times)
        dialog.set_subtitle_number(subtitle)

        if not keep_open:
            dialog.destroy()

        row = subtitle - 1
        
        # Select subtitle.
        selection = project.tree_view.get_selection()
        selection.unselect_all()
        selection.select_path(row)
        
        # Scroll to subtitle.
        project.tree_view.set_cursor(row, tree_view_column)
        project.tree_view.scroll_to_cell(row, tree_view_column, True, 0.5, 0)

        project.tree_view.grab_focus()

    def on_jump_to_subtitle_activated(self, *args):
        """Jump to a specific subtitle."""

        keep_open = self.config.getboolean('jump_to_dialog', 'keep_open')
        dialog = JumpToSubtitleDialog(self.window, keep_open)
        dialog.connect('jump-button-clicked', self._jump_to_subtitle)
        dialog.show()
