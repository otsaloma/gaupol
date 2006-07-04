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

from gaupol.base               import cons
from gaupol.base.icons         import *
from gaupol.base.delegate.edit import EditDelegate
from gaupol.test               import Test


class TestEditDelegate(Test):

    def setup_method(self, method):

        self.project = self.get_project()
        self.delegate = EditDelegate(self.project)

        for i in range(len(self.project.main_texts)):
            self.project.main_texts[i] = 'test'
            self.project.tran_texts[i] = 'test'

    def test_insert_blank(self):

        self.project.insert_subtitles([1, 2])
        assert self.project.main_texts[1] == ''
        assert self.project.main_texts[2] == ''

        self.project.undo()
        assert self.project.main_texts[1] == 'test'
        assert self.project.main_texts[2] == 'test'

        self.project.redo()
        assert self.project.main_texts[1] == ''
        assert self.project.main_texts[2] == ''

    def test_insert_data(self):

        self.project.insert_subtitles(
            [0, 1],
            ['00:00:00:000', '00:00:00:100'],
            [0, 1],
            ['0', '1'],
            ['0', '1']

        )
        assert self.project.main_texts[0] == '0'
        assert self.project.main_texts[1] == '1'

        self.project.undo()
        assert self.project.main_texts[0] == 'test'
        assert self.project.main_texts[1] == 'test'

        self.project.redo()
        assert self.project.main_texts[0] == '0'
        assert self.project.main_texts[1] == '1'

    def test_sort_data(self):

        last = len(self.project.times) - 1
        orig_times = copy.deepcopy(self.project.times)
        self.project.main_texts[0] = 'first'
        self.project.set_frame(0, SHOW, 999999999999)
        assert self.project.times[:last] == orig_times[1:]
        assert self.project.main_texts[last] == 'first'

        self.project.undo()
        assert self.project.times[1:] == orig_times[1:]
        assert self.project.main_texts[0] == 'first'

        self.project.redo()
        assert self.project.times[:last] == orig_times[1:]
        assert self.project.main_texts[last] == 'first'

    def test_clear_texts(self):

        self.project.clear_texts([0, 1], MAIN)
        assert self.project.main_texts[0] == ''
        assert self.project.main_texts[1] == ''

        self.project.undo()
        assert self.project.main_texts[0] == 'test'
        assert self.project.main_texts[1] == 'test'

        self.project.redo()
        assert self.project.main_texts[0] == ''
        assert self.project.main_texts[1] == ''

    def test_copy_texts(self):

        self.project.copy_texts([0, 2], MAIN)
        data = self.project.clipboard.data
        assert data == ['test', None, 'test']

    def test_cut_texts(self):

        self.project.cut_texts([0, 2], MAIN)
        assert self.project.main_texts[0] == ''
        assert self.project.main_texts[2] == ''
        data = self.project.clipboard.data
        assert data == ['test', None, 'test']

        self.project.undo()
        assert self.project.main_texts[0] == 'test'
        assert self.project.main_texts[2] == 'test'

        self.project.redo()
        assert self.project.main_texts[0] == ''
        assert self.project.main_texts[2] == ''

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

    def test_get_mode(self):

        mode =  self.project.get_mode()
        assert mode in (cons.Mode.TIME, cons.Mode.FRAME)

    def test_get_positions(self):

        positions = self.project.get_positions()
        assert positions in (self.project.times, self.project.frames)

    def test_merge_subtitles(self):

        orig_len = len(self.project.times)
        orig_times_1 = self.project.times[1]
        orig_times_2 = self.project.times[2]
        orig_frames_1 = self.project.frames[1]
        orig_frames_2 = self.project.frames[2]
        orig_main_1 = self.project.main_texts[1]
        orig_main_2 = self.project.main_texts[2]
        orig_tran_1 = self.project.tran_texts[1]
        orig_tran_2 = self.project.tran_texts[2]

        self.project.merge_subtitles([1, 2])
        assert len(self.project.times) == orig_len - 1
        assert self.project.times[1][SHOW] == orig_times_1[SHOW]
        assert self.project.times[1][HIDE] == orig_times_2[HIDE]
        assert self.project.frames[1][SHOW] == orig_frames_1[SHOW]
        assert self.project.frames[1][HIDE] == orig_frames_2[HIDE]
        assert self.project.main_texts[1] == \
               str(orig_main_1 + '\n' + orig_main_2).strip()
        assert self.project.tran_texts[1] == \
               str(orig_tran_1 + '\n' + orig_tran_2).strip()

        self.project.undo()
        assert len(self.project.times) == orig_len
        assert self.project.times[1] == orig_times_1
        assert self.project.times[2] == orig_times_2
        assert self.project.frames[1] == orig_frames_1
        assert self.project.frames[2] == orig_frames_2
        assert self.project.main_texts[1] == orig_main_1
        assert self.project.main_texts[2] == orig_main_2
        assert self.project.tran_texts[1] == orig_tran_1
        assert self.project.tran_texts[2] == orig_tran_2

        self.project.redo()
        assert len(self.project.times) == orig_len - 1
        assert self.project.times[1][SHOW] == orig_times_1[SHOW]
        assert self.project.times[1][HIDE] == orig_times_2[HIDE]
        assert self.project.frames[1][SHOW] == orig_frames_1[SHOW]
        assert self.project.frames[1][HIDE] == orig_frames_2[HIDE]
        assert self.project.main_texts[1] == \
               str(orig_main_1 + '\n' + orig_main_2).strip()
        assert self.project.tran_texts[1] == \
               str(orig_tran_1 + '\n' + orig_tran_2).strip()

        self.project.merge_subtitles([1, 2, 3, 4])
        self.project.undo()
        self.project.redo()

    def test_needs_resort(self):

        assert self.project.needs_resort(0, '99:59:59.999') is True
        assert self.project.needs_resort(0, '00:00:00.000') is False

    def test_paste_texts(self):

        self.project.tran_texts[2] = '2'
        self.project.tran_texts[3] = '3'
        self.project.copy_texts([2, 3], TRAN)
        self.project.paste_texts(0, MAIN)
        assert self.project.main_texts[0] == '2'
        assert self.project.main_texts[1] == '3'

        self.project.undo()
        assert self.project.main_texts[0] == 'test'
        assert self.project.main_texts[1] == 'test'

        self.project.redo()
        assert self.project.main_texts[0] == '2'
        assert self.project.main_texts[1] == '3'

    def test_paste_texts_excess(self):

        self.project.clipboard.data = ['excess'] * 999
        self.project.paste_texts(0, MAIN)
        assert len(self.project.times) == 999
        for i in range(999):
            assert self.project.main_texts[i] == 'excess'

        self.project.undo()
        assert len(self.project.times) < 999
        assert self.project.main_texts[0] == 'test'
        assert self.project.main_texts[1] == 'test'

        self.project.redo()
        assert len(self.project.times) == 999
        for i in range(999):
            assert self.project.main_texts[i] == 'excess'

    def test_remove_subtitles(self):

        orig_length = len(self.project.times)
        self.project.remove_subtitles([2, 3])
        assert len(self.project.times) == orig_length - 2

        self.project.undo()
        assert len(self.project.times) == orig_length
        assert self.project.main_texts[2] == 'test'
        assert self.project.main_texts[3] == 'test'

        self.project.redo()
        assert len(self.project.times) == orig_length - 2

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

    def test_set_frame(self):

        orig_hide_frame = self.project.frames[3][HIDE]
        orig_durn_frame = self.project.frames[3][DURN]
        orig_hide_time  = self.project.times[3][HIDE]
        orig_durn_time  = self.project.times[3][DURN]

        self.project.set_frame(3, HIDE, 999999)
        assert self.project.frames[3][HIDE] == 999999
        assert self.project.frames[3][DURN] >  orig_durn_frame
        assert self.project.times[3][HIDE]  >  orig_hide_time
        assert self.project.times[3][DURN]  >  orig_durn_time

        self.project.undo()
        assert self.project.frames[3][HIDE] == orig_hide_frame
        assert self.project.frames[3][DURN] == orig_durn_frame
        assert self.project.times[3][HIDE]  == orig_hide_time
        assert self.project.times[3][DURN]  == orig_durn_time

        self.project.redo()
        assert self.project.frames[3][HIDE] == 999999
        assert self.project.frames[3][DURN] >  orig_durn_frame
        assert self.project.times[3][HIDE]  >  orig_hide_time
        assert self.project.times[3][DURN]  >  orig_durn_time

    def test_set_text(self):

        self.project.set_text(2, MAIN, 's')
        assert self.project.main_texts[2] == 's'

        self.project.undo()
        assert self.project.main_texts[2] == 'test'

        self.project.redo()
        assert self.project.main_texts[2] == 's'

    def test_set_time(self):

        orig_hide_time  = self.project.times[3][HIDE]
        orig_durn_time  = self.project.times[3][DURN]
        orig_hide_frame = self.project.frames[3][HIDE]
        orig_durn_frame = self.project.frames[3][DURN]

        self.project.set_time(3, DURN, '33:33:33.333')
        assert self.project.times[3][HIDE]  >  orig_hide_time
        assert self.project.times[3][DURN]  == '33:33:33.333'
        assert self.project.frames[3][HIDE] >  orig_hide_frame
        assert self.project.frames[3][DURN] >  orig_durn_frame

        self.project.undo()
        assert self.project.times[3][HIDE]  == orig_hide_time
        assert self.project.times[3][DURN]  == orig_durn_time
        assert self.project.frames[3][HIDE] == orig_hide_frame
        assert self.project.frames[3][DURN] == orig_durn_frame

        self.project.redo()
        assert self.project.times[3][HIDE]  >  orig_hide_time
        assert self.project.times[3][DURN]  == '33:33:33.333'
        assert self.project.frames[3][HIDE] >  orig_hide_frame
        assert self.project.frames[3][DURN] >  orig_durn_frame

    def test_split_subtitle(self):

        orig_len = len(self.project.times)
        orig_times = self.project.times[1]
        orig_frames = self.project.frames[1]
        orig_main = self.project.main_texts[1]
        orig_tran = self.project.tran_texts[1]

        self.project.split_subtitle(1)
        assert len(self.project.times) == orig_len + 1
        assert self.project.times[2][HIDE] == orig_times[HIDE]
        assert self.project.frames[2][HIDE] == orig_frames[HIDE]
        assert self.project.main_texts[2] == orig_main
        assert self.project.tran_texts[2] == orig_tran

        self.project.undo()
        assert len(self.project.times) == orig_len
        assert self.project.times[1][HIDE] == orig_times[HIDE]
        assert self.project.frames[1][HIDE] == orig_frames[HIDE]

        self.project.redo()
        assert len(self.project.times) == orig_len + 1
        assert self.project.times[2][HIDE] == orig_times[HIDE]
        assert self.project.frames[2][HIDE] == orig_frames[HIDE]
        assert self.project.main_texts[2] == orig_main
        assert self.project.tran_texts[2] == orig_tran
