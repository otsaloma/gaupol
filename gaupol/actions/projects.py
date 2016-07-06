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

class ActivateNextProjectAction(gaupol.Action):
    def __init__(self):
        gaupol.Action.__init__(self, "activate-next-project")
        self.accelerators = ["<Control>Page_Down"]
        self.action_group = "safe"
    def _affirm_doable(self, application, page, selected_rows):
        aeidon.util.affirm(page is not None)
        index = application.pages.index(page) + 1
        aeidon.util.affirm(index in range(len(application.pages)))

class ActivatePreviousProjectAction(gaupol.Action):
    def __init__(self):
        gaupol.Action.__init__(self, "activate-previous-project")
        self.accelerators = ["<Control>Page_Up"]
        self.action_group = "safe"
    def _affirm_doable(self, application, page, selected_rows):
        aeidon.util.affirm(page is not None)
        aeidon.util.affirm(application.pages.index(page) > 0)

class ActivateProjectAction(gaupol.RadioAction):
    def __new__(cls):
        action = gaupol.RadioAction.new("activate-project")
        action.__class__ = cls
        return action
    def __init__(self):
        gaupol.RadioAction.__init__(self, "activate-project")
        self.set_state(str(0))
    def _affirm_doable(self, application, page, selected_rows):
        aeidon.util.affirm(application.pages)

class CloseAllProjectsAction(gaupol.Action):
    def __init__(self):
        gaupol.Action.__init__(self, "close-all-projects")
        self.accelerators = ["<Shift><Control>W"]
        self.action_group = "safe"
    def _affirm_doable(self, application, page, selected_rows):
        aeidon.util.affirm(application.pages)

class MoveTabLeftAction(gaupol.Action):
    def __init__(self):
        gaupol.Action.__init__(self, "move-tab-left")
        self.action_group = "safe"
    def _affirm_doable(self, application, page, selected_rows):
        aeidon.util.affirm(page is not None)
        aeidon.util.affirm(application.pages.index(page) > 0)

class MoveTabRightAction(gaupol.Action):
    def __init__(self):
        gaupol.Action.__init__(self, "move-tab-right")
        self.action_group = "safe"
    def _affirm_doable(self, application, page, selected_rows):
        aeidon.util.affirm(page is not None)
        index = application.pages.index(page) + 1
        aeidon.util.affirm(index in range(len(application.pages)))

class SaveAllDocumentsAction(gaupol.Action):
    def __init__(self):
        gaupol.Action.__init__(self, "save-all-documents")
        self.accelerators = ["<Shift><Control>L"]
        self.action_group = "safe"
    def _affirm_doable(self, application, page, selected_rows):
        aeidon.util.affirm(application.pages)

class SaveAllDocumentsAsAction(gaupol.Action):
    def __init__(self):
        gaupol.Action.__init__(self, "save-all-documents-as")
        self.action_group = "safe"
    def _affirm_doable(self, application, page, selected_rows):
        aeidon.util.affirm([x for x in application.pages
                            if x.project.main_file is not None])

__all__ = tuple(x for x in dir() if x.endswith("Action"))
