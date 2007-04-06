# Copyright (C) 2005-2006 Osmo Salomaa
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


import types

from gaupol import const
from gaupol._agents import *
from gaupol._agents import AGENTS
from gaupol.base import Observable
from gaupol.calculator import Calculator
from gaupol.clipboard import Clipboard


class Project(Observable):

    """Model for subtitle data.

    Instance variables:

        _delegations: Dictionary mapping method names to agents
        calc:         Position calculator
        clipboard:    Internal clipboard
        framerate:    FRAMERATE constant
        frames:       List of lists of show, hide, duration frames
        main_changed: Integer, status of main document
        main_file:    The main SubtitleFile
        main_texts:   List of the main document's texts
        redoables:    Stack of redoable Actions
        times:        List of lists of show, hide, duration times
        tran_active:  True if the translation document is active
        tran_changed: Integer, status of the translation document
        tran_file:    The translation SubtitleFile
        tran_texts:   List of the translation document's texts
        undoables:    Stack of undoable Actions
        undo_limit:   Maximum size of the undo/redo stacks or None for no limit
        video_path:   Path to the video file

    Signals:

        action-done (project, action)
        action-redone (project, action)
        action-undone (project, action)
        main-file-opened (project, main_file)
        main-file-saved (project, main_file)
        main-texts-changed (project, rows)
        positions-changed (project, rows)
        subtitles-changed (project, rows)
        subtitles-inserted (project, rows)
        subtitles-removed (project, rows)
        translation-file-opened (project, tran_file)
        translation-file-saved (project, tran_file)
        translation-texts-changed (project, rows)

    See gaupol._agents for project methods provided by agents.
    """

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

        return self._delegations[name].__getattribute__(name)

    def __init__(self, framerate=const.FRAMERATE.P24, undo_limit=None):

        Observable.__init__(self)

        self._delegations = {}
        self.calc         = Calculator(framerate)
        self.clipboard    = Clipboard()
        self.framerate    = framerate
        self.frames       = []
        self.main_changed = 0
        self.main_file    = None
        self.main_texts   = []
        self.redoables    = []
        self.times        = []
        self.tran_active  = False
        self.tran_changed = 0
        self.tran_file    = None
        self.tran_texts   = []
        self.undo_limit   = undo_limit
        self.undoables    = []
        self.video_path   = None

        self._init_delegations()

    def _init_delegations(self):
        """Initialize the delegation mappings."""

        for agent in (eval(x)(self) for x in AGENTS):
            for attr_name in (x for x in dir(agent) if not x.startswith("_")):
                attr = getattr(agent, attr_name)
                if type(attr) is types.MethodType:
                    if attr_name in self._delegations:
                        raise ValueError
                    self._delegations[attr_name] = agent
