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


"""Text searching actions."""


import gaupol.gtk
import gtk
_ = gaupol.i18n._

from .action import Action


class FindAndReplaceAction(Action):

    """Search for and replace text."""

    def __init__(self):

        Action.__init__(self, "find_and_replace")
        self.props.label = _("_Find And Replace\342\200\246")
        self.props.short_label = _("Find")
        self.props.stock_id = gtk.STOCK_FIND_AND_REPLACE
        self.props.tooltip = _("Search for and replace text")
        self.accelerator = "<Control>F"

    def _assert_doable(self, application, page):
        """Raise AssertionError if action cannot be done."""

        assert page is not None


class FindNextAction(Action):

    """Search forwards for same text."""

    def __init__(self):

        Action.__init__(self, "find_next")
        self.props.label = _("Find _Next")
        self.props.tooltip = _("Search forwards for same text")
        self.accelerator = "<Control>G"

    def _assert_doable(self, application, page):
        """Raise AssertionError if action cannot be done."""

        assert page is not None
        assert application.pattern


class FindPreviousAction(Action):

    """Search backwards for same text."""

    def __init__(self):

        Action.__init__(self, "find_previous")
        self.props.label = _("Find Pre_vious")
        self.props.tooltip = _("Search backwards for same text")
        self.accelerator = "<Shift><Control>G"

    def _assert_doable(self, application, page):
        """Raise AssertionError if action cannot be done."""

        assert page is not None
        assert application.pattern
