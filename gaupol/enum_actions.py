# -*- coding: utf-8 -*-

# Copyright (C) 2009 Osmo Salomaa
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

"""
Dictionaries mapping enumeration items to action names.

:var field_actions: Dictionary mapping :attr:`aeidon.fields` to actions
:var framerate_actions: Dictionary mapping :attr:`aeidon.framerates` to actions
:var mode_actions: Dictionary mapping :attr:`aeidon.modes` to actions
"""

import aeidon
import gaupol

__all__ = ("field_actions", "framerate_actions", "mode_actions")


field_actions = {
    gaupol.fields.NUMBER:    "toggle-number-column",
    gaupol.fields.START:     "toggle-start-column",
    gaupol.fields.END:       "toggle-end-column",
    gaupol.fields.DURATION:  "toggle-duration-column",
    gaupol.fields.MAIN_TEXT: "toggle-main-text-column",
    gaupol.fields.TRAN_TEXT: "toggle-translation-text-column",
}

framerate_actions = {
    aeidon.framerates.FPS_23_976: "show-framerate-23-976",
    aeidon.framerates.FPS_24_000: "show-framerate-24-000",
    aeidon.framerates.FPS_25_000: "show-framerate-25-000",
    aeidon.framerates.FPS_29_970: "show-framerate-29-970",
}

mode_actions = {
    aeidon.modes.TIME:  "show-times",
    aeidon.modes.FRAME: "show-frames",
}
