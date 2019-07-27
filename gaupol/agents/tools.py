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

"""Tools to edit positions and texts."""

import aeidon
import gaupol

from aeidon.i18n import _
from gi.repository import Gtk


class ToolsAgent(aeidon.Delegate):

    """Tools to edit positions and texts."""

    @aeidon.deco.export
    def _on_adjust_durations_activate(self, *args):
        """Lengthen or shorten durations."""
        dialog = gaupol.DurationAdjustDialog(self.window, self)
        gaupol.util.flash_dialog(dialog)

    @aeidon.deco.export
    def _on_check_spelling_activate(self, *args):
        """Check for incorrect spelling."""
        gaupol.util.set_cursor_busy(self.window)
        try:
            dialog = gaupol.SpellCheckDialog(self.window, self)
        except Exception as error:
            gaupol.util.set_cursor_normal(self.window)
            title = _('Failed to load dictionary for language "{}"')
            title = title.format(gaupol.conf.spell_check.language)
            dialog = gaupol.ErrorDialog(self.window, title, str(error))
            dialog.add_button(_("_OK"), Gtk.ResponseType.OK)
            dialog.set_default_response(Gtk.ResponseType.OK)
            return gaupol.util.flash_dialog(dialog)
        gaupol.util.set_cursor_normal(self.window)
        gaupol.util.flash_dialog(dialog)

    @aeidon.deco.export
    def _on_configure_spell_check_activate(self, *args):
        """Set language and spell-check targets."""
        gaupol.util.set_cursor_busy(self.window)
        dialog = gaupol.LanguageDialog(self.window)
        gaupol.util.set_cursor_normal(self.window)
        gaupol.util.flash_dialog(dialog)
        self.update_gui()

    @aeidon.deco.export
    def _on_convert_framerate_activate(self, *args):
        """Convert framerate."""
        dialog = gaupol.FramerateConvertDialog(self.window, self)
        gaupol.util.flash_dialog(dialog)

    @aeidon.deco.export
    def _on_correct_texts_activate(self, *args):
        """Find and correct errors in texts."""
        gaupol.util.set_cursor_busy(self.window)
        assistant = gaupol.TextAssistant(self.window, self)
        gaupol.util.set_cursor_normal(self.window)
        assistant.show()

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
    def _on_transform_positions_activate(self, *args):
        """Change positions by linear two-point correction."""
        page = self.get_current_page()
        if page.edit_mode == aeidon.modes.TIME:
            dialog = gaupol.TimeTransformDialog(self.window, self)
        if page.edit_mode == aeidon.modes.FRAME:
            dialog = gaupol.FrameTransformDialog(self.window, self)
        gaupol.util.flash_dialog(dialog)
