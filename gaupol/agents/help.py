# Copyright (C) 2005-2007,2010 Osmo Salomaa
#
# This file is part of Gaupol.
#
# Gaupol is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# Gaupol is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# Gaupol. If not, see <http://www.gnu.org/licenses/>.

"""Help and information."""

import aeidon
import gaupol


class HelpAgent(aeidon.Delegate):

    """Help and information."""

    def on_browse_wiki_documentation_activate(self, *args):
        """Open web browser to view wiki documentation."""
        gaupol.util.show_uri(gaupol.WIKI_URL)

    def on_report_a_bug_activate(self, *args):
        """Open web browser to submit a bug report."""
        gaupol.util.show_uri(gaupol.BUG_REPORT_URL)

    def on_view_about_dialog_activate(self, *args):
        """Show information about Gaupol."""
        gaupol.util.flash_dialog(gaupol.AboutDialog(self.window))
