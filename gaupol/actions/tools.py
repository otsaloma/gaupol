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

"""Tool actions for :class:`gaupol.Application`."""

import aeidon
import gaupol

class AdjustDurationsAction(gaupol.Action):
    def __init__(self):
        gaupol.Action.__init__(self, "adjust-durations")
        self.action_group = "unsafe"
    def _affirm_doable(self, application, page, selected_rows):
        aeidon.util.affirm(page is not None)

class AppendFileAction(gaupol.Action):
    def __init__(self):
        gaupol.Action.__init__(self, "append-file")
        self.action_group = "unsafe"
    def _affirm_doable(self, application, page, selected_rows):
        aeidon.util.affirm(page is not None)
        aeidon.util.affirm(len(page.project.subtitles) > 0)

class CheckSpellingAction(gaupol.Action):
    def __init__(self):
        gaupol.Action.__init__(self, "check-spelling")
        self.accelerators = ["F7"]
        self.action_group = "unsafe"
    def _affirm_doable(self, application, page, selected_rows):
        aeidon.util.affirm(page is not None)
        aeidon.util.affirm(aeidon.SpellChecker.available())
        aeidon.util.affirm(gaupol.conf.spell_check.language)

class ConfigureSpellCheckAction(gaupol.Action):
    def __init__(self):
        gaupol.Action.__init__(self, "configure-spell-check")
        self.action_group = "unsafe"
    def _affirm_doable(self, application, page, selected_rows):
        aeidon.util.affirm(aeidon.SpellChecker.available())

class ConvertFramerateAction(gaupol.Action):
    def __init__(self):
        gaupol.Action.__init__(self, "convert-framerate")
        self.action_group = "unsafe"
    def _affirm_doable(self, application, page, selected_rows):
        aeidon.util.affirm(page is not None)
        aeidon.util.affirm(page.project.main_file is not None)

class CorrectTextsAction(gaupol.Action):
    def __init__(self):
        gaupol.Action.__init__(self, "correct-texts")
        self.accelerators = ["F8"]
        self.action_group = "unsafe"
    def _affirm_doable(self, application, page, selected_rows):
        aeidon.util.affirm(page is not None)

class PreviewAction(gaupol.Action):
    def __init__(self):
        gaupol.Action.__init__(self, "preview")
        self.accelerators = ["F5"]
        self.action_group = "unsafe"
    def _affirm_doable(self, application, page, selected_rows):
        aeidon.util.affirm(page is not None)
        aeidon.util.affirm(page.project.video_path is not None)
        if gaupol.conf.preview.use_custom_command:
            aeidon.util.affirm(gaupol.conf.preview.custom_command)

class SelectVideoFileAction(gaupol.Action):
    def __init__(self):
        gaupol.Action.__init__(self, "select-video-file")
        self.action_group = "safe"
    def _affirm_doable(self, application, page, selected_rows):
        aeidon.util.affirm(page is not None)
        aeidon.util.affirm(page.project.main_file is not None)

class ShiftPositionsAction(gaupol.Action):
    def __init__(self):
        gaupol.Action.__init__(self, "shift-positions")
        self.accelerators = ["H"]
        self.action_group = "unsafe"
    def _affirm_doable(self, application, page, selected_rows):
        aeidon.util.affirm(page is not None)

class SplitProjectAction(gaupol.Action):
    def __init__(self):
        gaupol.Action.__init__(self, "split-project")
        self.action_group = "unsafe"
    def _affirm_doable(self, application, page, selected_rows):
        aeidon.util.affirm(page is not None)
        aeidon.util.affirm(len(page.project.subtitles) > 1)

class TransformPositionsAction(gaupol.Action):
    def __init__(self):
        gaupol.Action.__init__(self, "transform-positions")
        self.action_group = "unsafe"
    def _affirm_doable(self, application, page, selected_rows):
        aeidon.util.affirm(page is not None)
        aeidon.util.affirm(len(page.project.subtitles) > 1)

__all__ = tuple(x for x in dir() if x.endswith("Action"))
