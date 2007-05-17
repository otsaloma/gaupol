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


"""Text searching actions."""


import gtk

from gaupol.gtk.i18n import _
from .action import UIMAction


class FindAndReplaceAction(UIMAction):

    """Search for and replace text."""

    action_item = (
        "find_and_replace",
        gtk.STOCK_FIND_AND_REPLACE,
        _("_Find And Replace\342\200\246"),
        "<control>F",
        _("Search for and replace text"),)

    paths = [
        "/ui/menubar/text/find_and_replace",
        "/ui/main_toolbar/find_and_replace"]

    @classmethod
    def is_doable(cls, application, page):
        """Return True if action can be done."""

        return (page is not None)


class FindNextAction(UIMAction):

    """Search forwards for same text."""

    action_item = (
        "find_next",
        None,
        _("Find _Next"),
        "<control>G",
        _("Search forwards for same text"),)

    paths = ["/ui/menubar/text/find_next"]

    @classmethod
    def is_doable(cls, application, page):
        """Return True if action can be done."""

        return bool(application.pattern)


class FindPreviousAction(UIMAction):

    """Search backwards for same text."""

    action_item = (
        "find_previous",
        None,
        _("Find _Previous"),
        "<shift><control>G",
        _("Search backwards for same text"),)

    paths = ["/ui/menubar/text/find_previous"]

    @classmethod
    def is_doable(cls, application, page):
        """Return True if action can be done."""

        return bool(application.pattern)
