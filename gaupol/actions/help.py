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

"""Help actions for :class:`gaupol.Application`."""

import aeidon
import gaupol

from aeidon.i18n import _


class BrowseWikiDocumentationAction(gaupol.Action):

    """Browse wiki documentation."""

    def __init__(self):
        """Initialize a :class:`BrowseWikiDocumentationAction` instance."""
        gaupol.Action.__init__(self, "browse_wiki_documentation")
        self.set_icon_name("help-contents")
        self.set_label(_("_Wiki Documentation"))
        self.set_tooltip(_("Browse wiki documentation"))
        self.action_group = "main-safe"


class ReportABugAction(gaupol.Action):

    """Submit a bug report."""

    def __init__(self):
        """Initialize a :class:`ReportABugAction` instance."""
        gaupol.Action.__init__(self, "report_a_bug")
        self.set_label(_("_Report A Bug"))
        self.set_tooltip(_("Submit a bug report"))
        self.action_group = "main-safe"


class ViewAboutDialogAction(gaupol.Action):

    """Show information about Gaupol."""

    def __init__(self):
        """Initialize a :class:`ViewAboutDialogAction` instance."""
        gaupol.Action.__init__(self, "view_about_dialog")
        self.set_icon_name("help-about")
        self.set_label(_("_About"))
        self.set_tooltip(_("Show information about Gaupol"))
        self.action_group = "main-safe"


__all__ = tuple(x for x in dir() if x.endswith("Action"))
