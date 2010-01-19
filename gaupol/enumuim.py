# Copyright (C) 2009 Osmo Salomaa
#
# This file is part of Gaupol.
#
# Gaupol is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# Gaupol is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# Gaupol.  If not, see <http://www.gnu.org/licenses/>.

"""Dictionaries mapping enumeration items to UI manager action names.

:var field_actions: Dictionary mapping :attr:`gaupol.formats` to actions
:var framerate_actions: Dictionary mapping :attr:`aeidon.framerates` to actions
:var mode_actions: Dictionary mapping :attr:`aeidon.modes` to actions
"""

import aeidon
import gaupol

__all__ = ("field_actions", "framerate_actions", "mode_actions")


field_actions = {gaupol.fields.NUMBER:    "toggle_number_column",
                 gaupol.fields.START:     "toggle_start_column",
                 gaupol.fields.END:       "toggle_end_column",
                 gaupol.fields.DURATION:  "toggle_duration_column",
                 gaupol.fields.MAIN_TEXT: "toggle_main_text_column",
                 gaupol.fields.TRAN_TEXT: "toggle_translation_text_column",}

framerate_actions = {aeidon.framerates.FPS_24: "show_framerate_24",
                     aeidon.framerates.FPS_25: "show_framerate_25",
                     aeidon.framerates.FPS_30: "show_framerate_30",}

mode_actions = {aeidon.modes.TIME:  "show_times",
                aeidon.modes.FRAME: "show_frames",}
