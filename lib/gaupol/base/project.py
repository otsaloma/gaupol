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

from gaupol.base.clipboard     import Clipboard
from gaupol.base.delegate      import Delegates
from gaupol.base.model         import Model
from gaupol.base.position.calc import Calculator


class Project(Model):

    """
    Model for subtitle data.

    Class variables:

        _signals: List of signals

    Instance variables:

        _delegations: Dictionary mapping method names to Delegates
        calc:         Calculator
        clipboard:    Clipboard
        framerate:    Framerate constant
        frames:       List of lists of frames
        main_changed: Integer, status of main document
        main_file:    SubtitleFile
        main_texts:   List of main document texts
        redoables:    Stack of RevertableActions
        times:        List of lists of times
        tran_active:  True if translation document is active
        tran_changed: Integer, status of translation document
        tran_file:    SubtitleFile
        tran_texts:   List of translation document texts
        undo_limit:   Max size of undo/redo stacks, None for no limit
        undoables:    Stack of RevertableActions
        video_path:   Path to video file

    """

    _signals = [
        'action_done',
        'action_redone',
        'action_undone',
    ]

    def __getattr__(self, name):

        return self._delegations[name].__getattribute__(name)

    def __init__(self, framerate=None, undo_limit=None):

        Model.__init__(self)

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
        """Initialize delegate mappings."""

        for cls in Delegates.classes:
            delegate = cls(self)
            for name in dir(delegate):
                if name.startswith('_'):
                    continue
                value = getattr(delegate, name)
                if type(value) is types.MethodType:
                    self._delegations[name] = delegate
