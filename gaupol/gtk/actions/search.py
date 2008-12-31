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

"""Text searching actions."""

import gaupol.gtk
import gtk
_ = gaupol.i18n._


class FindAndReplaceAction(gaupol.gtk.Action):

    """Search for and replace text."""

    def __init__(self):

        gaupol.gtk.Action.__init__(self, "find_and_replace")
        self.props.label = _("_Find And Replace\342\200\246")
        self.props.short_label = _("Find")
        self.props.stock_id = gtk.STOCK_FIND_AND_REPLACE
        self.props.tooltip = _("Search for and replace text")
        self.accelerator = "<Control>F"
        self.action_group = "main-unsafe"

    def _affirm_doable(self, application, page):
        """Raise AssertionError if action cannot be done."""

        gaupol.util.affirm(page is not None)


class FindNextAction(gaupol.gtk.Action):

    """Search forwards for same text."""

    def __init__(self):

        gaupol.gtk.Action.__init__(self, "find_next")
        self.props.label = _("Find _Next")
        self.props.tooltip = _("Search forwards for same text")
        self.accelerator = "<Control>G"
        self.action_group = "main-unsafe"

    def _affirm_doable(self, application, page):
        """Raise AssertionError if action cannot be done."""

        gaupol.util.affirm(page is not None)
        gaupol.util.affirm(application.pattern)


class FindPreviousAction(gaupol.gtk.Action):

    """Search backwards for same text."""

    def __init__(self):

        gaupol.gtk.Action.__init__(self, "find_previous")
        self.props.label = _("Find Pre_vious")
        self.props.tooltip = _("Search backwards for same text")
        self.accelerator = "<Shift><Control>G"
        self.action_group = "main-unsafe"

    def _affirm_doable(self, application, page):
        """Raise AssertionError if action cannot be done."""

        gaupol.util.affirm(page is not None)
        gaupol.util.affirm(application.pattern)


__all__ = gaupol.util.get_all(dir(), r"Action$")
