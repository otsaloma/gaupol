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

class SetEditModeAction(gaupol.RadioAction):
    def __new__(cls):
        action = gaupol.RadioAction.new("set-edit-mode")
        action.__class__ = cls
        return action
    def __init__(self):
        gaupol.RadioAction.__init__(self, "set-edit-mode")
        self.accelerators = ["<Shift>T"]
        self.set_state(str(gaupol.conf.editor.mode))
    def _affirm_doable(self, application, page, selected_rows):
        aeidon.util.affirm(page is not None)

class SetFramerateAction(gaupol.RadioAction):
    def __new__(cls):
        action = gaupol.RadioAction.new("set-framerate")
        action.__class__ = cls
        return action
    def __init__(self):
        gaupol.RadioAction.__init__(self, "set-framerate")
        self.action_group = "unsafe"
        self.set_state(str(gaupol.conf.editor.framerate))
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
        self.action_group = "unsafe"
        self.set_state(str(gaupol.conf.application_window.layout))
    def _affirm_doable(self, application, page, selected_rows):
        aeidon.util.affirm(application.player is not None)

class ToggleDurationColumnAction(gaupol.ToggleAction):
    def __new__(cls):
        action = gaupol.ToggleAction.new("toggle-duration-column")
        action.__class__ = cls
        return action
    def __init__(self):
        gaupol.ToggleAction.__init__(self, "toggle-duration-column")
        self.action_group = "unsafe"
        self.set_state(gaupol.fields.DURATION in gaupol.conf.editor.visible_fields)
    def _affirm_doable(self, application, page, selected_rows):
        aeidon.util.affirm(page is not None)

class ToggleEndColumnAction(gaupol.ToggleAction):
    def __new__(cls):
        action = gaupol.ToggleAction.new("toggle-end-column")
        action.__class__ = cls
        return action
    def __init__(self):
        gaupol.ToggleAction.__init__(self, "toggle-end-column")
        self.action_group = "unsafe"
        self.set_state(gaupol.fields.END in gaupol.conf.editor.visible_fields)
    def _affirm_doable(self, application, page, selected_rows):
        aeidon.util.affirm(page is not None)

class ToggleMainTextColumnAction(gaupol.ToggleAction):
    def __new__(cls):
        action = gaupol.ToggleAction.new("toggle-main-text-column")
        action.__class__ = cls
        return action
    def __init__(self):
        gaupol.ToggleAction.__init__(self, "toggle-main-text-column")
        self.action_group = "unsafe"
        self.set_state(gaupol.fields.MAIN_TEXT in gaupol.conf.editor.visible_fields)
    def _affirm_doable(self, application, page, selected_rows):
        aeidon.util.affirm(page is not None)

class ToggleMainToolbarAction(gaupol.ToggleAction):
    def __new__(cls):
        action = gaupol.ToggleAction.new("toggle-main-toolbar")
        action.__class__ = cls
        return action
    def __init__(self):
        gaupol.ToggleAction.__init__(self, "toggle-main-toolbar")
        self.action_group = "safe"
        self.set_state(gaupol.conf.application_window.show_main_toolbar)

class ToggleNumberColumnAction(gaupol.ToggleAction):
    def __new__(cls):
        action = gaupol.ToggleAction.new("toggle-number-column")
        action.__class__ = cls
        return action
    def __init__(self):
        gaupol.ToggleAction.__init__(self, "toggle-number-column")
        self.action_group = "unsafe"
        self.set_state(gaupol.fields.NUMBER in gaupol.conf.editor.visible_fields)
    def _affirm_doable(self, application, page, selected_rows):
        aeidon.util.affirm(page is not None)

class TogglePlayerAction(gaupol.ToggleAction):
    def __new__(cls):
        action = gaupol.ToggleAction.new("toggle-player")
        action.__class__ = cls
        return action
    def __init__(self):
        gaupol.ToggleAction.__init__(self, "toggle-player")
        self.action_group = "safe"
        self.set_state(False)
    def _affirm_doable(self, application, page, selected_rows):
        aeidon.util.affirm(application.player is not None)

class ToggleStartColumnAction(gaupol.ToggleAction):
    def __new__(cls):
        action = gaupol.ToggleAction.new("toggle-start-column")
        action.__class__ = cls
        return action
    def __init__(self):
        gaupol.ToggleAction.__init__(self, "toggle-start-column")
        self.action_group = "unsafe"
        self.set_state(gaupol.fields.START in gaupol.conf.editor.visible_fields)
    def _affirm_doable(self, application, page, selected_rows):
        aeidon.util.affirm(page is not None)

class ToggleTranslationTextColumnAction(gaupol.ToggleAction):
    def __new__(cls):
        action = gaupol.ToggleAction.new("toggle-translation-text-column")
        action.__class__ = cls
        return action
    def __init__(self):
        gaupol.ToggleAction.__init__(self, "toggle-translation-text-column")
        self.action_group = "unsafe"
        self.set_state(gaupol.fields.TRAN_TEXT in gaupol.conf.editor.visible_fields)
    def _affirm_doable(self, application, page, selected_rows):
        aeidon.util.affirm(page is not None)

__all__ = tuple(x for x in dir() if x.endswith("Action"))
