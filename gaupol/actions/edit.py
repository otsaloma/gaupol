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

"""Simple subtitle data editing actions for :class:`gaupol.Application`."""

import aeidon
import gaupol

from gi.repository import Gtk

class EditPreferencesAction(gaupol.Action):
    def __init__(self):
        gaupol.Action.__init__(self, "edit-preferences")
        self.action_group = "safe"

class EditNextValueAction(gaupol.Action):
    def __init__(self):
        gaupol.Action.__init__(self, "edit-next-value")
        self.accelerators = ["space"]
        self.action_group = "unsafe"
    def _affirm_doable(self, application, page, selected_rows):
        aeidon.util.affirm(page is not None)
        row, col = page.view.get_focus()
        aeidon.util.affirm(not None in (row, col))
        aeidon.util.affirm(row < len(page.project.subtitles) - 1)
        column = page.view.get_column(col)
        renderer = column.get_cells()[0]
        aeidon.util.affirm(renderer.props.mode ==
                           Gtk.CellRendererMode.EDITABLE)

class EditValueAction(gaupol.Action):
    def __init__(self):
        gaupol.Action.__init__(self, "edit-value")
        self.accelerators = ["Return"]
        self.action_group = "unsafe"
    def _affirm_doable(self, application, page, selected_rows):
        aeidon.util.affirm(page is not None)
        row, col = page.view.get_focus()
        aeidon.util.affirm(not None in (row, col))
        column = page.view.get_column(col)
        renderer = column.get_cells()[0]
        aeidon.util.affirm(renderer.props.mode ==
                           Gtk.CellRendererMode.EDITABLE)

class EndEarlierAction(gaupol.Action):
    def __init__(self):
        gaupol.Action.__init__(self, "end-earlier")
        self.accelerators = ["E"]
        self.action_group = "unsafe"
    def _affirm_doable(self, application, page, selected_rows):
        aeidon.util.affirm(page is not None)
        aeidon.util.affirm(page.project.subtitles)
        aeidon.util.affirm(len(selected_rows) == 1)

class EndLaterAction(gaupol.Action):
    def __init__(self):
        gaupol.Action.__init__(self, "end-later")
        self.accelerators = ["R"]
        self.action_group = "unsafe"
    def _affirm_doable(self, application, page, selected_rows):
        aeidon.util.affirm(page is not None)
        aeidon.util.affirm(page.project.subtitles)
        aeidon.util.affirm(len(selected_rows) == 1)

class ExtendSelectionToBeginningAction(gaupol.Action):
    def __init__(self):
        gaupol.Action.__init__(self, "extend-selection-to-beginning")
        self.accelerators = ["<Shift><Control>Home"]
        self.action_group = "unsafe"
    def _affirm_doable(self, application, page, selected_rows):
        aeidon.util.affirm(page is not None)
        aeidon.util.affirm(page.project.subtitles)
        aeidon.util.affirm(selected_rows)

class ExtendSelectionToEndAction(gaupol.Action):
    def __init__(self):
        gaupol.Action.__init__(self, "extend-selection-to-end")
        self.accelerators = ["<Shift><Control>End"]
        self.action_group = "unsafe"
    def _affirm_doable(self, application, page, selected_rows):
        aeidon.util.affirm(page is not None)
        aeidon.util.affirm(page.project.subtitles)
        aeidon.util.affirm(selected_rows)

class InsertSubtitleAtVideoPositionAction(gaupol.Action):
    def __init__(self):
        gaupol.Action.__init__(self, "insert-subtitle-at-video-position")
        self.accelerators = ["J"]
        self.action_group = "unsafe"
    def _affirm_doable(self, application, page, selected_rows):
        aeidon.util.affirm(page is not None)
        aeidon.util.affirm(application.player is not None)
        aeidon.util.affirm(application.player.ready)

class InsertSubtitlesAction(gaupol.Action):
    def __init__(self):
        gaupol.Action.__init__(self, "insert-subtitles")
        self.accelerators = ["I"]
        self.action_group = "unsafe"
    def _affirm_doable(self, application, page, selected_rows):
        aeidon.util.affirm(page is not None)
        if page.project.subtitles:
            aeidon.util.affirm(selected_rows)

class InvertSelectionAction(gaupol.Action):
    def __init__(self):
        gaupol.Action.__init__(self, "invert-selection")
        self.accelerators = ["<Control>J"]
        self.action_group = "unsafe"
    def _affirm_doable(self, application, page, selected_rows):
        aeidon.util.affirm(page is not None)
        aeidon.util.affirm(page.project.subtitles)

class MergeSubtitlesAction(gaupol.Action):
    def __init__(self):
        gaupol.Action.__init__(self, "merge-subtitles")
        self.accelerators = ["M"]
        self.action_group = "unsafe"
    def _affirm_doable(self, application, page, selected_rows):
        aeidon.util.affirm(page is not None)
        aeidon.util.affirm(len(selected_rows) > 1)
        block = list(range(selected_rows[0], selected_rows[-1] + 1))
        aeidon.util.affirm(list(selected_rows) == block)

class RedoActionAction(gaupol.Action):
    def __init__(self):
        gaupol.Action.__init__(self, "redo-action")
        self.accelerators = ["<Shift><Control>Z"]
        self.action_group = "unsafe"
    def _affirm_doable(self, application, page, selected_rows):
        aeidon.util.affirm(page is not None)
        aeidon.util.affirm(page.project.can_redo())

class RemoveSubtitlesAction(gaupol.Action):
    def __init__(self):
        gaupol.Action.__init__(self, "remove-subtitles")
        self.accelerators = ["Delete"]
        self.action_group = "unsafe"
    def _affirm_doable(self, application, page, selected_rows):
        aeidon.util.affirm(page is not None)
        aeidon.util.affirm(selected_rows)

class SelectAllAction(gaupol.Action):
    def __init__(self):
        gaupol.Action.__init__(self, "select-all")
        self.accelerators = ["<Control>A"]
        self.action_group = "unsafe"
    def _affirm_doable(self, application, page, selected_rows):
        aeidon.util.affirm(page is not None)
        aeidon.util.affirm(page.project.subtitles)

class SelectNextFromVideoPositionAction(gaupol.Action):
    def __init__(self):
        gaupol.Action.__init__(self, "select-next-from-video-position")
        self.accelerators = ["<Control>U"]
        self.action_group = "unsafe"
    def _affirm_doable(self, application, page, selected_rows):
        aeidon.util.affirm(page is not None)
        aeidon.util.affirm(page.project.subtitles)
        aeidon.util.affirm(application.player is not None)
        aeidon.util.affirm(application.player.ready)

class SelectPreviousFromVideoPositionAction(gaupol.Action):
    def __init__(self):
        gaupol.Action.__init__(self, "select-previous-from-video-position")
        self.accelerators = ["<Control>Y"]
        self.action_group = "unsafe"
    def _affirm_doable(self, application, page, selected_rows):
        aeidon.util.affirm(page is not None)
        aeidon.util.affirm(page.project.subtitles)
        aeidon.util.affirm(application.player is not None)
        aeidon.util.affirm(application.player.ready)

class SetEndFromVideoPositionAction(gaupol.Action):
    def __init__(self):
        gaupol.Action.__init__(self, "set-end-from-video-position")
        self.accelerators = ["K"]
        self.action_group = "unsafe"
    def _affirm_doable(self, application, page, selected_rows):
        aeidon.util.affirm(page is not None)
        aeidon.util.affirm(application.player is not None)
        aeidon.util.affirm(application.player.ready)
        aeidon.util.affirm(len(selected_rows) == 1)

class SetStartFromVideoPositionAction(gaupol.Action):
    def __init__(self):
        gaupol.Action.__init__(self, "set-start-from-video-position")
        self.accelerators = ["U"]
        self.action_group = "unsafe"
    def _affirm_doable(self, application, page, selected_rows):
        aeidon.util.affirm(page is not None)
        aeidon.util.affirm(application.player is not None)
        aeidon.util.affirm(application.player.ready)
        aeidon.util.affirm(len(selected_rows) == 1)

class SplitSubtitleAction(gaupol.Action):
    def __init__(self):
        gaupol.Action.__init__(self, "split-subtitle")
        self.accelerators = ["S"]
        self.action_group = "unsafe"
    def _affirm_doable(self, application, page, selected_rows):
        aeidon.util.affirm(page is not None)
        aeidon.util.affirm(len(selected_rows) == 1)

class StartEarlierAction(gaupol.Action):
    def __init__(self):
        gaupol.Action.__init__(self, "start-earlier")
        self.accelerators = ["Q"]
        self.action_group = "unsafe"
    def _affirm_doable(self, application, page, selected_rows):
        aeidon.util.affirm(page is not None)
        aeidon.util.affirm(page.project.subtitles)
        aeidon.util.affirm(len(selected_rows) == 1)

class StartLaterAction(gaupol.Action):
    def __init__(self):
        gaupol.Action.__init__(self, "start-later")
        self.accelerators = ["W"]
        self.action_group = "unsafe"
    def _affirm_doable(self, application, page, selected_rows):
        aeidon.util.affirm(page is not None)
        aeidon.util.affirm(page.project.subtitles)
        aeidon.util.affirm(len(selected_rows) == 1)

class UndoActionAction(gaupol.Action):
    def __init__(self):
        gaupol.Action.__init__(self, "undo-action")
        self.accelerators = ["<Control>Z"]
        self.action_group = "unsafe"
    def _affirm_doable(self, application, page, selected_rows):
        aeidon.util.affirm(page is not None)
        aeidon.util.affirm(page.project.can_undo())

__all__ = tuple(x for x in dir() if x.endswith("Action"))
