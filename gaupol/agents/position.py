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

"""Editing times and frames."""

import aeidon
import gaupol


class PositionAgent(aeidon.Delegate):

    """Editing times and frames."""

    @aeidon.deco.export
    def _on_adjust_durations_activate(self, *args):
        """Lengthen or shorten durations."""
        dialog = gaupol.DurationAdjustDialog(self.window, self)
        gaupol.util.flash_dialog(dialog)

    @aeidon.deco.export
    def _on_convert_framerate_activate(self, *args):
        """Convert framerate."""
        dialog = gaupol.FramerateConvertDialog(self.window, self)
        gaupol.util.flash_dialog(dialog)

    @aeidon.deco.export
    def _on_shift_positions_activate(self, *args):
        """Make subtitles appear earlier or later."""
        page = self.get_current_page()
        if page.edit_mode == aeidon.modes.TIME:
            dialog = gaupol.TimeShiftDialog(self.window, self)
        if page.edit_mode == aeidon.modes.FRAME:
            dialog = gaupol.FrameShiftDialog(self.window, self)
        gaupol.util.flash_dialog(dialog)

    @aeidon.deco.export
    def _on_speech_recognition_activate(self, *args):
        """Generate subtitles by voice and speech recognition."""
        dialog = gaupol.SpeechRecognitionDialog(self.window, self)
        gaupol.util.flash_dialog(dialog)

    @aeidon.deco.export
    def _on_transform_positions_activate(self, *args):
        """Change positions by linear two-point correction."""
        page = self.get_current_page()
        if page.edit_mode == aeidon.modes.TIME:
            dialog = gaupol.TimeTransformDialog(self.window, self)
        if page.edit_mode == aeidon.modes.FRAME:
            dialog = gaupol.FrameTransformDialog(self.window, self)
        gaupol.util.flash_dialog(dialog)
