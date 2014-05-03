# -*- coding: utf-8 -*-

# Copyright (C) 2005-2008,2010 Osmo Salomaa
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

"""Text searching actions for :class:`gaupol.Application`."""

import aeidon
import gaupol
_ = aeidon.i18n._

from gi.repository import Gtk


class FindAndReplaceAction(gaupol.Action):

    """Search for and replace text."""

    def __init__(self):
        """Initialize a :class:`FindAndReplaceAction` instance."""
        gaupol.Action.__init__(self, "find_and_replace")
        self.props.label = _("_Find And Replace…")
        self.props.short_label = _("Find")
        self.props.stock_id = Gtk.STOCK_FIND_AND_REPLACE
        self.props.tooltip = _("Search for and replace text")
        self.accelerator = "<Control>F"
        self.action_group = "main-unsafe"

    def _affirm_doable(self, application, page, selected_rows):
        """Raise :exc:`aeidon.AffirmationError` if action cannot be done."""
        aeidon.util.affirm(page is not None)


class FindNextAction(gaupol.Action):

    """Search forwards for same text."""

    def __init__(self):
        """Initialize a :class:`FindNextAction` instance."""
        gaupol.Action.__init__(self, "find_next")
        self.props.label = _("Find _Next")
        self.props.tooltip = _("Search forwards for same text")
        self.accelerator = "<Control>G"
        self.action_group = "main-unsafe"

    def _affirm_doable(self, application, page, selected_rows):
        """Raise :exc:`aeidon.AffirmationError` if action cannot be done."""
        aeidon.util.affirm(page is not None)
        aeidon.util.affirm(application.pattern)


class FindPreviousAction(gaupol.Action):

    """Search backwards for same text."""

    def __init__(self):
        """Initialize a :class:`FindPreviousAction` instance."""
        gaupol.Action.__init__(self, "find_previous")
        self.props.label = _("Find Pre_vious")
        self.props.tooltip = _("Search backwards for same text")
        self.accelerator = "<Shift><Control>G"
        self.action_group = "main-unsafe"

    def _affirm_doable(self, application, page, selected_rows):
        """Raise :exc:`aeidon.AffirmationError` if action cannot be done."""
        aeidon.util.affirm(page is not None)
        aeidon.util.affirm(application.pattern)


__all__ = tuple(x for x in dir() if x.endswith("Action"))
