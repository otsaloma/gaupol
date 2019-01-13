# -*- coding: utf-8 -*-

# Copyright (C) 2013 Osmo Salomaa
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

"""Audio actions for :class:`gaupol.Application`."""

import aeidon
import gaupol

class SetAudioLanguageAction(gaupol.RadioAction):
    def __new__(cls):
        action = gaupol.RadioAction.new("set-audio-language")
        action.__class__ = cls
        return action
    def __init__(self):
        gaupol.RadioAction.__init__(self, "set-audio-language")
        self.set_state(str(0))
    def _affirm_doable(self, application, page, selected_rows):
        aeidon.util.affirm(application.player is not None)
        aeidon.util.affirm(application.player.ready)

class VolumeDownAction(gaupol.Action):
    def __init__(self):
        gaupol.Action.__init__(self, "volume-down")
        self.accelerators = ["<Control>minus", "<Control>KP_Subtract"]
        self.action_group = "unsafe"
    def _affirm_doable(self, application, page, selected_rows):
        aeidon.util.affirm(application.player is not None)
        aeidon.util.affirm(application.player.ready)

class VolumeUpAction(gaupol.Action):
    def __init__(self):
        gaupol.Action.__init__(self, "volume-up")
        self.accelerators = ["<Control>plus", "<Control>KP_Add"]
        self.action_group = "unsafe"
    def _affirm_doable(self, application, page, selected_rows):
        aeidon.util.affirm(application.player is not None)
        aeidon.util.affirm(application.player.ready)

__all__ = tuple(x for x in dir() if x.endswith("Action"))
