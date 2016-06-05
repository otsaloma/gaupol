# -*- coding: utf-8 -*-

# Copyright (C) 2005 Osmo Salomaa
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""Help and information."""

import aeidon
import gaupol


class HelpAgent(aeidon.Delegate):

    """Help and information."""

    @aeidon.deco.export
    def _on_browse_documentation_activate(self, *args):
        """Open web browser to view documentation."""
        gaupol.util.show_uri(gaupol.DOCUMENTATION_URL)

    @aeidon.deco.export
    def _on_report_a_bug_activate(self, *args):
        """Open web browser to submit a bug report."""
        gaupol.util.show_uri(gaupol.BUG_REPORT_URL)

    @aeidon.deco.export
    def _on_view_about_dialog_activate(self, *args):
        """Show information about Gaupol."""
        gaupol.util.flash_dialog(gaupol.AboutDialog(self.window))
