# Copyright (C) 2005 Osmo Salomaa
#
# This file is part of Gaupol.
#
# Gaupol is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Gaupol is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Gaupol; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA


"""Model for subtitle data."""


try:
    from psyco.classes import *
except ImportError:
    pass

import types

from gaupol.base.clipboard   import Clipboard
from gaupol.base.delegates   import Delegates
from gaupol.base.model       import Model
from gaupol.base.timing.calc import TimeFrameCalculator


class Project(Model):

    """Model for subtitle data."""

    _signals = [
        'action_done',
        'action_redone',
        'action_undone',
    ]

    def __init__(self, framerate, undo_limit=None):

        Model.__init__(self)

        self.times      = []
        self.frames     = []
        self.main_texts = []
        self.tran_texts = []

        self.framerate = framerate
        self.calc      = TimeFrameCalculator(framerate)

        self.main_file = None
        self.tran_file = None

        # True if translation file exists or any action affecting translation
        # only has been performed.
        self.tran_active = False

        # Doing and redoing will increase changed value by one. Undoing will
        # decrease changed value by one. At zero the document is at its
        # unchanged (saved) state.
        self.main_changed = 0
        self.tran_changed = 0

        # Stacks of revertable actions.
        self.undoables = []
        self.redoables = []

        # Maximum size for the above stacks. None for no size limit.
        self.undo_limit = undo_limit

        # Clipboard for Gaupol internal use.
        self.clipboard = Clipboard()

        # Video file path and video player output.
        self.video_path = None
        self.output     = None

        self._delegations = {}
        self._init_delegations()

    def _init_delegations(self):
        """Initialize delegate mappings."""

        # Loop through all delegates creating an instance of the delegate and
        # mapping all its methods that don't start with an underscore to that
        # instance.
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


if __name__ == '__main__':

    from gaupol.test import Test

    class TestProject(Test):

        def test_init(self):

            Project(0, 10)
            Project(0)

    TestProject().run()

