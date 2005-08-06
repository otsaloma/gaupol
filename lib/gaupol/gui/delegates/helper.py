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


"""Offerer of support and information."""


try:
    from psyco.classes import *
except ImportError:
    pass

from gaupol.gui.delegates.delegate import Delegate
from gaupol.gui.dialogs.about import AboutDialog


class Helper(Delegate):
    
    """Offerer of support and information."""

    def on_about_activated(self, *args):
        """Display the about dialog."""
        
        dialog = AboutDialog(self.window)
        dialog.run()
        dialog.destroy()

    def on_check_latest_version_activated(self, *args):
        """Check latest version of Gaupol from the project page."""
        
        pass
        
    def on_report_a_bug_activated(self, *args):
        """Report a bug at the project page."""

        pass
        
    def on_support_activated(self, *args):
        """Request support at the project page."""

        pass
