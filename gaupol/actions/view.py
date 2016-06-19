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

"""View actions for :class:`gaupol.Application`."""

import aeidon
import gaupol

class SetFramerateAction(gaupol.RadioAction):
    def __new__(cls):
        action = gaupol.RadioAction.new("set-framerate")
        action.__class__ = cls
        return action
    def __init__(self):
        gaupol.RadioAction.__init__(self, "set-framerate")
        self.action_group = "main-unsafe"
    def _affirm_doable(self, application, page, selected_rows):
        aeidon.util.affirm(page is not None)
        aeidon.util.affirm(page.project.main_file is not None)

class SetLayoutAction(gaupol.RadioAction):
    def __new__(cls):
        action = gaupol.RadioAction.new("set-layout")
        action.__class__ = cls
        return action
    def __init__(self):
        gaupol.RadioAction.__init__(self, "set-layout")
        self.action_group = "main-unsafe"
    def _affirm_doable(self, application, page, selected_rows):
        aeidon.util.affirm(application.player is not None)

class SetPositionUnitsAction(gaupol.RadioAction):
    def __new__(cls):
        action = gaupol.RadioAction.new("set-position-units")
        action.__class__ = cls
        return action
    def __init__(self):
        gaupol.RadioAction.__init__(self, "set-position-units")
        self.accelerators = ["<Shift>T"]
    def _affirm_doable(self, application, page, selected_rows):
        aeidon.util.affirm(page is not None)

class ShowColumnsMenuAction(gaupol.Action):
    def __init__(self):
        gaupol.Action.__init__(self, "show-columns-menu")
        self.action_group = "main-unsafe"
    def _affirm_doable(self, application, page, selected_rows):
        aeidon.util.affirm(page is not None)

class ShowFramerateMenuAction(gaupol.Action):
    def __init__(self):
        gaupol.Action.__init__(self, "show-framerate-menu")
        self.action_group = "main-unsafe"
    def _affirm_doable(self, application, page, selected_rows):
        aeidon.util.affirm(page is not None)
        aeidon.util.affirm(page.project.main_file is not None)

class ShowLayoutMenuAction(gaupol.Action):
    def __init__(self):
        gaupol.Action.__init__(self, "show-layout-menu")
        self.action_group = "main-unsafe"
    def _affirm_doable(self, application, page, selected_rows):
        aeidon.util.affirm(application.player is not None)

class ToggleDurationColumnAction(gaupol.ToggleAction):
    def __new__(cls):
        action = gaupol.ToggleAction.new("toggle-duration-column")
        action.__class__ = cls
        return action
    def __init__(self):
        gaupol.ToggleAction.__init__(self, "toggle-duration-column")
        self.action_group = "main-unsafe"
    def _affirm_doable(self, application, page, selected_rows):
        aeidon.util.affirm(page is not None)

class ToggleEndColumnAction(gaupol.ToggleAction):
    def __new__(cls):
        action = gaupol.ToggleAction.new("toggle-end-column")
        action.__class__ = cls
        return action
    def __init__(self):
        gaupol.ToggleAction.__init__(self, "toggle-end-column")
        self.action_group = "main-unsafe"
    def _affirm_doable(self, application, page, selected_rows):
        aeidon.util.affirm(page is not None)

class ToggleMainTextColumnAction(gaupol.ToggleAction):
    def __new__(cls):
        action = gaupol.ToggleAction.new("toggle-main-text-column")
        action.__class__ = cls
        return action
    def __init__(self):
        gaupol.ToggleAction.__init__(self, "toggle-main-text-column")
        self.action_group = "main-unsafe"
    def _affirm_doable(self, application, page, selected_rows):
        aeidon.util.affirm(page is not None)

class ToggleMainToolbarAction(gaupol.ToggleAction):
    def __new__(cls):
        action = gaupol.ToggleAction.new("toggle-main-toolbar")
        action.__class__ = cls
        return action
    def __init__(self):
        gaupol.ToggleAction.__init__(self, "toggle-main-toolbar")
        self.action_group = "main-safe"

class ToggleNumberColumnAction(gaupol.ToggleAction):
    def __new__(cls):
        action = gaupol.ToggleAction.new("toggle-number-column")
        action.__class__ = cls
        return action
    def __init__(self):
        gaupol.ToggleAction.__init__(self, "toggle-number-column")
        self.action_group = "main-unsafe"
    def _affirm_doable(self, application, page, selected_rows):
        aeidon.util.affirm(page is not None)

class TogglePlayerAction(gaupol.ToggleAction):
    def __new__(cls):
        action = gaupol.ToggleAction.new("toggle-player")
        action.__class__ = cls
        return action
    def __init__(self):
        gaupol.ToggleAction.__init__(self, "toggle-player")
        self.action_group = "main-safe"
    def _affirm_doable(self, application, page, selected_rows):
        aeidon.util.affirm(application.player is not None)

class ToggleStartColumnAction(gaupol.ToggleAction):
    def __new__(cls):
        action = gaupol.ToggleAction.new("toggle-start-column")
        action.__class__ = cls
        return action
    def __init__(self):
        gaupol.ToggleAction.__init__(self, "toggle-start-column")
        self.action_group = "main-unsafe"
    def _affirm_doable(self, application, page, selected_rows):
        aeidon.util.affirm(page is not None)

class ToggleTranslationTextColumnAction(gaupol.ToggleAction):
    def __new__(cls):
        action = gaupol.ToggleAction.new("toggle-translation-text-column")
        action.__class__ = cls
        return action
    def __init__(self):
        gaupol.ToggleAction.__init__(self, "toggle-translation-text-column")
        self.action_group = "main-unsafe"
    def _affirm_doable(self, application, page, selected_rows):
        aeidon.util.affirm(page is not None)

__all__ = tuple(x for x in dir() if x.endswith("Action"))
