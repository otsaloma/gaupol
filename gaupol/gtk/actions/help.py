# Copyright (C) 2005-2007 Osmo Salomaa
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
# A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# Gaupol.  If not, see <http://www.gnu.org/licenses/>.


"""Help actions."""


import gaupol
import gtk
_ = gaupol.i18n._

from .action import Action


class ReportABugAction(Action):

    """Submit a bug report."""

    def __init__(self):

        Action.__init__(self, "report_a_bug")
        self.props.label = _("_Report A Bug")
        self.props.tooltip = _("Submit a bug report")


class ViewAboutDialogAction(Action):

    """Show information about Gaupol."""

    def __init__(self):

        Action.__init__(self, "view_about_dialog")
        self.props.label = _("_About")
        self.props.stock_id = gtk.STOCK_ABOUT
        self.props.tooltip = _("Show information about Gaupol")
