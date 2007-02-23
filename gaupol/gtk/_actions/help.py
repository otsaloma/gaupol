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


"""Help menu UI manager actions."""


from gettext import gettext as _

import gtk

from ._action import UIMAction


class ReportABugAction(UIMAction):

    """Submit a bug report."""

    action_item = (
        "report_a_bug",
        None,
        _("_Report A Bug"),
        None,
        _("Submit a bug report"),)

    paths = ["/ui/menubar/help/report_a_bug"]


class ViewAboutDialogAction(UIMAction):

    """Show information about Gaupol."""

    action_item = (
        "view_about_dialog",
        gtk.STOCK_ABOUT,
        _("_About"),
        None,
        _("Show information about Gaupol"),)

    paths = ["/ui/menubar/help/about"]
