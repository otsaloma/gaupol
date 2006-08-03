# Copyright (C) 2006 Osmo Salomaa
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


from gettext import gettext as _
import copy

from gaupol.test       import Test
from gaupol.base.icons import *
from gaupol.base.util  import scriptlib


class TestTextDelegate(Test):

    def setup_method(self, method):

        self.project = self.get_project()

    def test_capitalize(self):

        texts = self.project.main_texts
        texts[0] = \
            '- which paper?\n' \
            '- figaro-pravda.'
        texts[1] = \
            'room 344. have you registered\n' \
            'at residents control...'
        texts[2] = \
            'you must, even if you\'re\n' \
            'a festival visitor a.k.a. a visitor'

        pattern, flags = scriptlib.get_capitalize_after(_('Latin'))
        rows = self.project.capitalize([0, 1, 2], [MAIN], pattern, flags)
        assert rows == [0, 1]

        assert texts[0] == \
            '- Which paper?\n' \
            '- Figaro-pravda.'
        assert texts[1] == \
            'Room 344. Have you registered\n' \
            'at residents control...'
        assert texts[2] == \
            'you must, even if you\'re\n' \
            'a festival visitor a.k.a. a visitor'

        self.project.undo()
        self.project.redo()

    def test_not_really_do(self):

        orig_times = copy.deepcopy(self.project.times)
        orig_frames = copy.deepcopy(self.project.frames)
        orig_main_texts = copy.deepcopy(self.project.main_texts)
        orig_tran_texts = copy.deepcopy(self.project.tran_texts)

        method = self.project.remove_subtitles
        args = [[0, 1, 2]]
        data = self.project.not_really_do(method, args)
        assert len(self.project.undoables) == 0

        assert data[0] != self.project.times
        assert data[1] != self.project.frames
        assert data[2] != self.project.main_texts
        assert data[3] != self.project.tran_texts

        assert self.project.times == orig_times
        assert self.project.frames == orig_frames
        assert self.project.main_texts == orig_main_texts
        assert self.project.tran_texts == orig_tran_texts
