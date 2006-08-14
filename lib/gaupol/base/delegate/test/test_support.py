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


import copy

from gaupol.base                  import cons
from gaupol.base.icons            import *
from gaupol.base.delegate.support import SupportDelegate
from gaupol.test                  import Test


class TestSupportDelegate(Test):

    def setup_method(self, method):

        self.project = self.get_project()
        self.delegate = SupportDelegate(self.project)

        for i in range(len(self.project.main_texts)):
            self.project.main_texts[i] = 'test'
            self.project.tran_texts[i] = 'test'

    def test_expand_frames(self):

        calc = self.project.calc
        times, frames = self.project.expand_frames(10, 100)
        assert frames == [10, 100, 90]
        assert times  == list(calc.frame_to_time(x) for x in frames)

    def test_expand_positions(self):

        calc = self.project.calc
        times, frames = self.project.expand_positions(10, 100)
        assert frames == [10, 100, 90]
        assert times  == list(calc.frame_to_time(x) for x in frames)

        show = '00:00:01.000'
        hide = '00:01:00.000'
        times, frames = self.project.expand_positions(show, hide)
        assert times  == [show, hide, '00:00:59.000']
        assert frames == list(calc.time_to_frame(x) for x in times)

    def test_expand_times(self):

        calc = self.project.calc
        show = '00:00:01.000'
        hide = '00:01:00.000'
        times, frames = self.project.expand_times(show, hide)
        assert times  == [show, hide, '00:00:59.000']
        assert frames == list(calc.time_to_frame(x) for x in times)

    def test_get_format_class_name(self):

        name = self.project.get_format_class_name(MAIN)
        assert name in cons.Format.class_names

    def test_get_mode(self):

        mode =  self.project.get_mode()
        assert mode in (cons.Mode.TIME, cons.Mode.FRAME)

    def test_get_positions(self):

        positions = self.project.get_positions()
        assert positions in (self.project.times, self.project.frames)

    def test_get_tag_regex(self):

        re_tag = self.project.get_tag_regex(MAIN)
        if re_tag is not None:
            assert hasattr(re_tag, 'match')

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

    def test_replace_both_texts(self):

        self.project.replace_both_texts([[1], [1]], [['r'], ['r']])
        assert self.project.main_texts[1] == 'r'
        assert self.project.tran_texts[1] == 'r'

        self.project.undo()
        assert self.project.main_texts[1] == 'test'
        assert self.project.tran_texts[1] == 'test'

        self.project.redo()
        assert self.project.main_texts[1] == 'r'
        assert self.project.tran_texts[1] == 'r'

    def test_replace_positions(self):

        orig_time  = self.project.times[0]
        orig_frame = self.project.frames[0]
        self.project.replace_positions([0], ['00:00:00.000'], [0])
        assert self.project.times[0]  == '00:00:00.000'
        assert self.project.frames[0] == 0

        self.project.undo()
        assert self.project.times[0]  == orig_time
        assert self.project.frames[0] == orig_frame

        self.project.redo()
        assert self.project.times[0]  == '00:00:00.000'
        assert self.project.frames[0] == 0

    def test_replace_texts(self):

        self.project.replace_texts([1, 2], TRAN, ['r', 'r'])
        assert self.project.tran_texts[1] == 'r'
        assert self.project.tran_texts[2] == 'r'

        self.project.undo()
        assert self.project.tran_texts[1] == 'test'
        assert self.project.tran_texts[2] == 'test'

        self.project.redo()
        assert self.project.tran_texts[1] == 'r'
        assert self.project.tran_texts[2] == 'r'
