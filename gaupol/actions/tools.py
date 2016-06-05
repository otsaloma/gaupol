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

"""Time and frame editing actions for :class:`gaupol.Application`."""

import aeidon
import gaupol

from aeidon.i18n import _


class AdjustDurationsAction(gaupol.Action):

    """Lengthen or shorten durations."""

    def __init__(self):
        """Initialize an :class:`AdjustDurationsAction` instance."""
        gaupol.Action.__init__(self, "adjust_durations")
        self.set_label(_("Adjust _Durations…"))
        self.set_tooltip(_("Lengthen or shorten durations"))
        self.action_group = "main-unsafe"

    def _affirm_doable(self, application, page, selected_rows):
        """Raise :exc:`aeidon.AffirmationError` if action cannot be done."""
        aeidon.util.affirm(page is not None)


class CheckSpellingAction(gaupol.Action):

    """Check for incorrect spelling."""

    def __init__(self):
        """Initialize a :class:`CheckSpellingAction` instance."""
        gaupol.Action.__init__(self, "check_spelling")
        self.set_icon_name("tools-check-spelling")
        self.set_label(_("_Check Spelling"))
        self.set_short_label(_("Spelling"))
        self.set_tooltip(_("Check for incorrect spelling"))
        self.accelerator = "F7"
        self.action_group = "main-unsafe"

    def _affirm_doable(self, application, page, selected_rows):
        """Raise :exc:`aeidon.AffirmationError` if action cannot be done."""
        aeidon.util.affirm(page is not None)
        aeidon.util.affirm(aeidon.util.enchant_available())
        aeidon.util.affirm(gaupol.conf.spell_check.language)


class ConfigureSpellCheckAction(gaupol.Action):

    """Set languages and spell-check targets."""

    def __init__(self):
        """Initialize a :class:`ConfigureSpellCheckAction` instance."""
        gaupol.Action.__init__(self, "configure_spell_check")
        self.set_label(_("Co_nfigure Spell-check…"))
        self.set_tooltip(_("Set language and spell-check target"))
        self.action_group = "main-unsafe"

    def _affirm_doable(self, application, page, selected_rows):
        """Raise :exc:`aeidon.AffirmationError` if action cannot be done."""
        aeidon.util.affirm(aeidon.util.enchant_available())


class ConvertFramerateAction(gaupol.Action):

    """Change positions for a different framerate."""

    def __init__(self):
        """Initialize a :class:`ConvertFramerateAction` instance."""
        gaupol.Action.__init__(self, "convert_framerate")
        self.set_label(_("Convert _Framerate…"))
        self.set_tooltip(_("Change positions for a different framerate"))
        self.action_group = "main-unsafe"

    def _affirm_doable(self, application, page, selected_rows):
        """Raise :exc:`aeidon.AffirmationError` if action cannot be done."""
        aeidon.util.affirm(page is not None)
        aeidon.util.affirm(page.project.main_file is not None)


class CorrectTextsAction(gaupol.Action):

    """Find and correct errors in texts."""

    def __init__(self):
        """Initialize a :class:`CorrectTextsAction` instance."""
        gaupol.Action.__init__(self, "correct_texts")
        self.set_label(_("C_orrect Texts…"))
        self.set_tooltip(_("Find and correct errors in texts"))
        self.accelerator = "F8"
        self.action_group = "main-unsafe"

    def _affirm_doable(self, application, page, selected_rows):
        """Raise :exc:`aeidon.AffirmationError` if action cannot be done."""
        aeidon.util.affirm(page is not None)


class PreviewAction(gaupol.Action):

    """Preview from selected position with a video player."""

    def __init__(self):
        """Initialize a :class:`PreviewAction` instance."""
        gaupol.Action.__init__(self, "preview")
        self.set_icon_name("media-playback-start")
        self.set_label(_("_Preview"))
        self.set_tooltip(_("Preview from selected position with a video player"))
        self.accelerator = "F5"
        self.action_group = "main-unsafe"

    def _affirm_doable(self, application, page, selected_rows):
        """Raise :exc:`aeidon.AffirmationError` if action cannot be done."""
        aeidon.util.affirm(page is not None)
        aeidon.util.affirm(page.project.video_path is not None)
        if gaupol.conf.preview.use_custom_command:
            aeidon.util.affirm(gaupol.conf.preview.custom_command)


class ShiftPositionsAction(gaupol.Action):

    """Make subtitles appear earlier or later."""

    def __init__(self):
        """Initialize a :class:`ShiftPositionsAction` instance."""
        gaupol.Action.__init__(self, "shift_positions")
        self.set_label(_("_Shift Positions…"))
        self.set_tooltip(_("Make subtitles appear earlier or later"))
        self.accelerator = "H"
        self.action_group = "main-unsafe"

    def _affirm_doable(self, application, page, selected_rows):
        """Raise :exc:`aeidon.AffirmationError` if action cannot be done."""
        aeidon.util.affirm(page is not None)


class TransformPositionsAction(gaupol.Action):

    """Change positions by linear two-point correction."""

    def __init__(self):
        """Initialize a :class:`TransformPositionsAction` instance."""
        gaupol.Action.__init__(self, "transform_positions")
        self.set_label(_("_Transform Positions…"))
        self.set_tooltip(_("Change positions by linear two-point correction"))
        self.action_group = "main-unsafe"

    def _affirm_doable(self, application, page, selected_rows):
        """Raise :exc:`aeidon.AffirmationError` if action cannot be done."""
        aeidon.util.affirm(page is not None)
        aeidon.util.affirm(len(page.project.subtitles) > 1)


__all__ = tuple(x for x in dir() if x.endswith("Action"))
