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

class CloseProjectAction(gaupol.Action):
    def __init__(self):
        gaupol.Action.__init__(self, "close-project")
        self.accelerators = ["<Control>W"]
        self.action_group = "safe"
    def _affirm_doable(self, application, page, selected_rows):
        aeidon.util.affirm(page is not None)

class NewProjectAction(gaupol.Action):
    def __init__(self):
        gaupol.Action.__init__(self, "new-project")
        self.accelerators = ["<Control>N"]
        self.action_group = "safe"

class OpenMainFilesAction(gaupol.Action):
    def __init__(self):
        gaupol.Action.__init__(self, "open-main-files")
        self.accelerators = ["<Control>O"]
        self.action_group = "safe"

class OpenTranslationFileAction(gaupol.Action):
    def __init__(self):
        gaupol.Action.__init__(self, "open-translation-file")
        self.action_group = "safe"
    def _affirm_doable(self, application, page, selected_rows):
        aeidon.util.affirm(page is not None)
        aeidon.util.affirm(page.project.main_file is not None)

class QuitAction(gaupol.Action):
    def __init__(self):
        gaupol.Action.__init__(self, "quit")
        self.accelerators = ["<Control>Q"]
        self.action_group = "safe"

class SaveMainDocumentAction(gaupol.Action):
    def __init__(self):
        gaupol.Action.__init__(self, "save-main-document")
        self.accelerators = ["<Control>S"]
        self.action_group = "safe"
    def _affirm_doable(self, application, page, selected_rows):
        aeidon.util.affirm(page is not None)

class SaveMainDocumentAsAction(gaupol.Action):
    def __init__(self):
        gaupol.Action.__init__(self, "save-main-document-as")
        self.accelerators = ["<Shift><Control>S"]
        self.action_group = "safe"
    def _affirm_doable(self, application, page, selected_rows):
        aeidon.util.affirm(page is not None)

class SaveTranslationDocumentAction(gaupol.Action):
    def __init__(self):
        gaupol.Action.__init__(self, "save-translation-document")
        self.accelerators = ["<Control>T"]
        self.action_group = "safe"
    def _affirm_doable(self, application, page, selected_rows):
        aeidon.util.affirm(page is not None)

class SaveTranslationDocumentAsAction(gaupol.Action):
    def __init__(self):
        gaupol.Action.__init__(self, "save-translation-document-as")
        self.accelerators = ["<Shift><Control>T"]
        self.action_group = "safe"
    def _affirm_doable(self, application, page, selected_rows):
        aeidon.util.affirm(page is not None)

__all__ = tuple(x for x in dir() if x.endswith("Action"))
