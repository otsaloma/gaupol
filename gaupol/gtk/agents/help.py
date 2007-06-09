# Copyright (C) 2005-2007 Osmo Salomaa
#
# This file is part of Gaupol.
#
# Gaupol is free software; you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.
#
# Gaupol is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# Gaupol; if not, write to the Free Software Foundation, Inc., 51 Franklin
# Street, Fifth Floor, Boston, MA 02110-1301, USA.


"""Help and information."""


import gaupol.gtk


class HelpAgent(gaupol.Delegate):

    """Help and information."""

    # pylint: disable-msg=E0203,W0201

    def on_report_a_bug_activate(self, *args):
        """Submit a bug report."""

        gaupol.gtk.util.browse_url(gaupol.BUG_REPORT_URL)

    def on_view_about_dialog_activate(self, *args):
        """Show information about Gaupol."""

        self.flash_dialog(gaupol.gtk.AboutDialog(self.window))
