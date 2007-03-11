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


"""Projects menu UI manager actions."""


import gtk
from gettext import gettext as _

from ._action import UIMAction


class ActivateNextProjectAction(UIMAction):

    """Activate the project in the next tab."""

    action_item = (
        "activate_next_project",
        None,
        _("_Next"),
        "<control>Page_Down",
        _("Activate the project in the next tab"),)

    paths = ["/ui/menubar/projects/next"]

    @classmethod
    def is_doable(cls, application, page):
        """Return True if action can be done."""

        if page is not None:
            index = application.pages.index(page) + 1
            return (index in range(len(application.pages)))
        return False


class ActivatePreviousProjectAction(UIMAction):

    """Activate the project in the previous tab."""

    action_item = (
        "activate_previous_project",
        None,
        _("_Previous"),
        "<control>Page_Up",
        _("Activate the project in the previous tab"),)

    paths = ["/ui/menubar/projects/previous"]

    @classmethod
    def is_doable(cls, application, page):
        """Return True if action can be done."""

        if page is not None:
            return (application.pages.index(page) > 0)
        return False


class CloseAllProjectsAction(UIMAction):

    """Close all open projects."""

    action_item = (
        "close_all_projects",
        gtk.STOCK_CLOSE,
        _("_Close All"),
        "<shift><control>W",
        _("Close all open projects"),)

    paths = ["/ui/menubar/projects/close_all"]

    @classmethod
    def is_doable(cls, application, page):
        """Return True if action can be done."""

        return (page is not None)


class MoveTabLeftAction(UIMAction):

    """Move the current tab to the left."""

    action_item = (
        "move_tab_left",
        None,
        _("Move Tab _Left"),
        None,
        _("Move the current tab to the left"),)

    paths = ["/ui/menubar/projects/move_tab_left"]

    @classmethod
    def is_doable(cls, application, page):
        """Return True if action can be done."""

        if page is not None:
            return (application.pages.index(page) > 0)
        return False


class MoveTabRightAction(UIMAction):

    """Move the current tab to the right."""

    action_item = (
        "move_tab_right",
        None,
        _("Move Tab _Right"),
        None,
        _("Move the current tab to the right"),)

    paths = ["/ui/menubar/projects/move_tab_right"]

    @classmethod
    def is_doable(cls, application, page):
        """Return True if action can be done."""

        if page is not None:
            index = application.pages.index(page) + 1
            return (index in range(len(application.pages)))
        return False


class SaveAllDocumentsAction(UIMAction):

    """Save all open documents."""

    action_item = (
        "save_all_documents",
        gtk.STOCK_SAVE,
        _("_Save All"),
        "<shift><control>L",
        _("Save all open documents"),)

    paths = ["/ui/menubar/projects/save_all"]

    @classmethod
    def is_doable(cls, application, page):
        """Return True if action can be done."""

        return (page is not None)
