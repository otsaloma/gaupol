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

"""Dictionaries mapping enumeration items to UI manager action names."""

import gaupol.gtk

__all__ = ("field_actions", "framerate_actions", "mode_actions")


field_actions = {
    gaupol.gtk.fields.NUMBER:    "toggle_number_column",
    gaupol.gtk.fields.START:     "toggle_start_column",
    gaupol.gtk.fields.END:       "toggle_end_column",
    gaupol.gtk.fields.DURATION:  "toggle_duration_column",
    gaupol.gtk.fields.MAIN_TEXT: "toggle_main_text_column",
    gaupol.gtk.fields.TRAN_TEXT: "toggle_translation_text_column",}

framerate_actions = {
    gaupol.framerates.FPS_24: "show_framerate_24",
    gaupol.framerates.FPS_25: "show_framerate_25",
    gaupol.framerates.FPS_30: "show_framerate_30",}

mode_actions = {
    gaupol.modes.TIME:  "show_times",
    gaupol.modes.FRAME: "show_frames",}
