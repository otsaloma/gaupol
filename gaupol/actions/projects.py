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


class CloseAllProjectsAction(gaupol.Action):

    """Close all open projects."""

    def __init__(self):
        """Initialize a :class:`CloseAllProjectsAction` instance."""
        gaupol.Action.__init__(self, "close_all_projects")
        self.set_icon_name("window-close")
        self.set_label(_("_Close All"))
        self.set_tooltip( _("Close all open projects"))
        self.accelerator = "<Shift><Control>W"
        self.action_group = "main-safe"

    def _affirm_doable(self, application, page, selected_rows):
        """Raise :exc:`aeidon.AffirmationError` if action cannot be done."""
        aeidon.util.affirm(application.pages)


class SaveAllDocumentsAction(gaupol.Action):

    """Save all open documents."""

    def __init__(self):
        """Initialize a :class:`SaveAllDocumentsAction` instance."""
        gaupol.Action.__init__(self, "save_all_documents")
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
        gaupol.Action.__init__(self, "save_all_documents_as")
        self.set_icon_name("document-save")
        self.set_label(_("Save _All As…"))
        self.set_tooltip(_("Save all open documents with different properties"))
        self.action_group = "main-safe"

    def _affirm_doable(self, application, page, selected_rows):
        """Raise :exc:`aeidon.AffirmationError` if action cannot be done."""
        aeidon.util.affirm([x for x in application.pages
                            if x.project.main_file is not None])


__all__ = tuple(x for x in dir() if x.endswith("Action"))
