# Copyright (C) 2005 Osmo Salomaa
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
from gaupol.base.delegates     import Delegates
from gaupol.base.model         import Model
from gaupol.base.position.calc import Calculator
from gaupol.base.text.finder   import Finder


class Project(Model):

    """Model for subtitle data."""

    _signals = [
        'action_done',
        'action_redone',
        'action_undone',
    ]

    def __init__(self, framerate=None, undo_limit=None):

        Model.__init__(self)

        self.times      = []
        self.frames     = []
        self.main_texts = []
        self.tran_texts = []
        self.main_file  = None
        self.tran_file  = None
        self.framerate  = framerate

        self.tran_active  = False
        self.main_changed = 0
        self.tran_changed = 0
        self.undoables    = []
        self.redoables    = []
        self.undo_limit   = undo_limit

        self.video_path = None
        self.output     = None

        self.calc = Calculator(framerate)
        self.clipboard = Clipboard()
        self.finder = Finder()

        self._delegations = {}
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

    def __getattr__(self, name):
        """Delegate method calls to delegate objects."""

        return self._delegations[name].__getattribute__(name)
