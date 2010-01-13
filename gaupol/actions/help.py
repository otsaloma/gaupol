# Copyright (C) 2005-2008 Osmo Salomaa
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

"""Help actions."""

import aeidon
import gtk
_ = aeidon.i18n._


class ReportABugAction(gaupol.Action):

    """Submit a bug report."""

    def __init__(self):
        """Initialize a ReportABugAction object."""

        gaupol.Action.__init__(self, "report_a_bug")
        self.props.label = _("_Report A Bug")
        self.props.tooltip = _("Submit a bug report")
        self.action_group = "main-safe"


class ViewAboutDialogAction(gaupol.Action):

    """Show information about Gaupol."""

    def __init__(self):
        """Initialize a ViewAboutDialogAction object."""

        gaupol.Action.__init__(self, "view_about_dialog")
        self.props.label = _("_About")
        self.props.stock_id = gtk.STOCK_ABOUT
        self.props.tooltip = _("Show information about Gaupol")
        self.action_group = "main-safe"


__all__ = aeidon.util.get_all(dir(), r"Action$")
