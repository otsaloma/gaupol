# Copyright (C) 2005-2007 Osmo Salomaa
#
# This file is part of Gaupol.
#
# Gaupol is free software; you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.
#
# Gaupol is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# Gaupol; if not, write to the Free Software Foundation, Inc., 51 Franklin
# Street, Fifth Floor, Boston, MA 02110-1301, USA.


"""Model for subtitle data."""


from gaupol import agents, const
from gaupol.base import Contractual, Observable
from gaupol.calculator import Calculator
from gaupol.clipboard import Clipboard


class Project(Observable):

    """Model for subtitle data.

    Instance variables:
     * _delegations: Dictionary mapping method names to agent methods
     * calc: Position calculator
     * clipboard: Internal subtitle clipboard
     * framerate: FRAMERATE constant
     * main_changed: Integer, status of main document
     * main_file: Main SubtitleFile
     * redoables: Stack of redoable Actions
     * subtitles: List of Subtitles
     * tran_changed: Status of the translation document or None if not active
     * tran_file: Translation SubtitleFile
     * undoables: Stack of undoable Actions
     * undo_limit: Maximum size of undo/redo stacks or None for no limit
     * video_path: Path to the video file

    Signals:
     * action-done (project, action)
     * action-redone (project, action)
     * action-undone (project, action)
     * main-file-opened (project, main_file)
     * main-file-saved (project, main_file)
     * main-texts-changed (project, indexes)
     * positions-changed (project, indexes)
     * subtitles-changed (project, indexes)
     * subtitles-inserted (project, indexes)
     * subtitles-removed (project, indexes)
     * translation-file-opened (project, tran_file)
     * translation-file-saved (project, tran_file)
     * translation-texts-changed (project, indexes)

    See gaupol._agents for project methods provided by agents.
    """

    __metaclass__ = Contractual

    _signals = [
        "action-done",
        "action-redone",
        "action-undone",
        "main-file-opened",
        "main-file-saved",
        "main-texts-changed",
        "positions-changed",
        "subtitles-inserted",
        "subtitles-removed",
        "subtitles-changed",
        "translation-file-opened",
        "translation-file-saved",
        "translation-texts-changed",]

    def __getattr__(self, name):

        return self._delegations[name]

    def __init__(self, framerate=const.FRAMERATE.P24, undo_limit=None):

        Observable.__init__(self)
        self._delegations = {}
        self.calc = Calculator(framerate)
        self.clipboard = Clipboard()
        self.framerate = framerate
        self.main_changed = 0
        self.main_file = None
        self.redoables = []
        self.subtitles = []
        self.tran_changed = None
        self.tran_file = None
        self.undo_limit = undo_limit
        self.undoables = []
        self.video_path = None

        self._init_delegations()

    def _invariant(self):
        assert self.calc.framerate == self.framerate.value
        if self.undo_limit is not None:
            assert len(self.undoables) <= self.undo_limit
            assert len(self.redoables) <= self.undo_limit

    def _init_delegations(self):
        """Initialize the delegation mappings."""

        for agent_class_name in agents.__all__:
            agent = getattr(agents, agent_class_name)(self)
            attrs = [x for x in dir(agent) if not x.startswith("_")]
            attrs = [(x, getattr(agent, x)) for x in attrs]
            attrs = [(x, y) for (x, y) in attrs if callable(y)]
            for attr_name, attr in attrs:
                if attr_name in self._delegations:
                    raise ValueError("Agents overlap")
                self._delegations[attr_name] = attr
