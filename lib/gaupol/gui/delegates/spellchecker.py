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


"""Spell-checking documents."""


try:
    from psyco.classes import *
except ImportError:
    pass

from gaupol.gui.delegates.delegate import Delegate


class SpellChecker(Delegate):

    """Spell-checking documents."""
    
    def on_check_spelling_activated(self, *args):
        """Start spell-checking document(s)."""
        
        pass
        
    def on_set_language_and_target_activated(self, *args):
        """Select language and target for spell-checking."""
        
        pass
