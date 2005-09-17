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


"""Base class for actions."""


try:
    from psyco.classes import *
except ImportError:
    pass

from gaupol.gtk.delegates.delegate import Delegate


class Action(Delegate):

    """Base class for actions."""

    undoable = False

    # UI Manager entries
    uim_actions        = []
    uim_radio_actions  = []
    uim_toggle_actions = []
    uim_paths          = []

    def is_doable(project):
        """Return whether action can or cannot be done."""
        return True

    is_doable = staticmethod(is_doable)

    def __init__(self, master, *args):

        Delegate.__init__(self, master)

        self.project     = None
        self.description = None
        self.documents   = None

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
