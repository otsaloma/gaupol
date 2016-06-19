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

"""File and project actions for :class:`gaupol.Application`."""

import aeidon
import gaupol

from aeidon.i18n import _


class ActivateNextProjectAction(gaupol.Action):
    def __init__(self):
        gaupol.Action.__init__(self, "activate-next-project")
        self.set_label(_("_Next"))
        self.set_tooltip(_("Activate the project in the next tab"))
        self.accelerator = "<Control>Page_Down"
        self.action_group = "main-safe"
    def _affirm_doable(self, application, page, selected_rows):
        aeidon.util.affirm(page is not None)
        index = application.pages.index(page) + 1
        aeidon.util.affirm(index in range(len(application.pages)))

class ActivatePreviousProjectAction(gaupol.Action):
    def __init__(self):
        gaupol.Action.__init__(self, "activate-previous-project")
        self.set_label(_("_Previous"))
        self.set_tooltip(_("Activate the project in the previous tab"))
        self.accelerator = "<Control>Page_Up"
        self.action_group = "main-safe"
    def _affirm_doable(self, application, page, selected_rows):
        aeidon.util.affirm(page is not None)
        aeidon.util.affirm(application.pages.index(page) > 0)

class CloseAllProjectsAction(gaupol.Action):

    """Close all open projects."""

    def __init__(self):
        """Initialize a :class:`CloseAllProjectsAction` instance."""
        gaupol.Action.__init__(self, "close-all-projects")
        self.set_icon_name("window-close")
        self.set_label(_("_Close All"))
        self.set_tooltip( _("Close all open projects"))
        self.accelerator = "<Shift><Control>W"
        self.action_group = "main-safe"

    def _affirm_doable(self, application, page, selected_rows):
        """Raise :exc:`aeidon.AffirmationError` if action cannot be done."""
        aeidon.util.affirm(application.pages)


class MoveTabLeftAction(gaupol.Action):
    def __init__(self):
        gaupol.Action.__init__(self, "move-tab-left")
        self.set_label(_("Move Tab _Left"))
        self.set_tooltip(_("Move the current tab to the left"))
        self.action_group = "main-safe"
    def _affirm_doable(self, application, page, selected_rows):
        aeidon.util.affirm(page is not None)
        aeidon.util.affirm(application.pages.index(page) > 0)

class MoveTabRightAction(gaupol.Action):
    def __init__(self):
        gaupol.Action.__init__(self, "move-tab-right")
        self.set_label(_("Move Tab _Right"))
        self.set_tooltip(_("Move the current tab to the right"))
        self.action_group = "main-safe"
    def _affirm_doable(self, application, page, selected_rows):
        aeidon.util.affirm(page is not None)
        index = application.pages.index(page) + 1
        aeidon.util.affirm(index in range(len(application.pages)))

class SaveAllDocumentsAction(gaupol.Action):

    """Save all open documents."""

    def __init__(self):
        """Initialize a :class:`SaveAllDocumentsAction` instance."""
        gaupol.Action.__init__(self, "save-all-documents")
        self.set_icon_name("document-save")
        self.set_label(_("_Save All"))
        self.set_tooltip(_("Save all open documents"))
        self.accelerator = "<Shift><Control>L"
        self.action_group = "main-safe"

    def _affirm_doable(self, application, page, selected_rows):
        """Raise :exc:`aeidon.AffirmationError` if action cannot be done."""
        aeidon.util.affirm(application.pages)


class SaveAllDocumentsAsAction(gaupol.Action):

    """Save all open documents with different properties."""

    def __init__(self):
        """Initialize a :class:`SaveAllDocumentsAsAction` instance."""
        gaupol.Action.__init__(self, "save-all-documents-as")
        self.set_icon_name("document-save")
        self.set_label(_("Save _All As…"))
        self.set_tooltip(_("Save all open documents with different properties"))
        self.action_group = "main-safe"

    def _affirm_doable(self, application, page, selected_rows):
        """Raise :exc:`aeidon.AffirmationError` if action cannot be done."""
        aeidon.util.affirm([x for x in application.pages
                            if x.project.main_file is not None])


__all__ = tuple(x for x in dir() if x.endswith("Action"))
