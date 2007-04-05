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

from gaupol import const
from gaupol.unittest import TestCase, reversion_test
from ..index import SHOW, HIDE, DURN


class TestEditAgent(TestCase):

    def setup_method(self, method):

        self.project = self.get_project()

    @reversion_test
    def test_clear_texts(self):

        self.project.clear_texts([0, 1], const.DOCUMENT.MAIN)
        assert self.project.main_texts[0] == ""
        assert self.project.main_texts[1] == ""

    def test_copy_texts(self):

        text_0 = self.project.main_texts[0]
        text_2 = self.project.main_texts[2]
        self.project.copy_texts([0, 2], const.DOCUMENT.MAIN)
        assert self.project.clipboard.data == [text_0, None, text_2]

    @reversion_test
    def test_cut_texts(self):

        text_1 = self.project.main_texts[1]
        text_3 = self.project.main_texts[3]
        self.project.cut_texts([1, 3], const.DOCUMENT.MAIN)
        assert self.project.clipboard.data == [text_1, None, text_3]
        assert self.project.main_texts[1] == ""
        assert self.project.main_texts[3] == ""

    @reversion_test
    def test_insert_blank_subtitles(self):

        orig_length = len(self.project.main_texts)
        self.project.insert_blank_subtitles([1, 2])
        assert len(self.project.main_texts) == orig_length + 2
        assert self.project.main_texts[1] == ""
        assert self.project.main_texts[2] == ""

    @reversion_test
    def test_insert_blank_subtitles_excess(self):

        orig_length = len(self.project.main_texts)
        self.project.insert_blank_subtitles([orig_length])
        assert len(self.project.main_texts) == orig_length + 1
        assert self.project.main_texts[orig_length] == ""

    @reversion_test
    def test_insert_blank_subtitles_multiple_ranges(self):

        orig_length = len(self.project.main_texts)
        self.project.insert_blank_subtitles([1, 3, 4])
        assert len(self.project.main_texts) == orig_length + 3
        assert self.project.main_texts[1] == ""
        assert self.project.main_texts[3] == ""
        assert self.project.main_texts[4] == ""

    @reversion_test
    def test_merge_subtitles(self):

        orig_times = copy.deepcopy(self.project.times)
        orig_frames = copy.deepcopy(self.project.frames)
        orig_main_texts = copy.deepcopy(self.project.main_texts)
        orig_tran_texts = copy.deepcopy(self.project.tran_texts)
        orig_length = len(self.project.times)
        self.project.merge_subtitles([1, 2])
        assert len(self.project.times) == orig_length - 1
        assert self.project.times[1][SHOW] == orig_times[1][SHOW]
        assert self.project.times[1][HIDE] == orig_times[2][HIDE]
        assert self.project.frames[1][SHOW] == orig_frames[1][SHOW]
        assert self.project.frames[1][HIDE] == orig_frames[2][HIDE]
        assert self.project.main_texts[1] == "\n".join(orig_main_texts[1:3])
        assert self.project.tran_texts[1] == "\n".join(orig_tran_texts[1:3])

    @reversion_test
    def test_paste_texts(self):

        texts = self.project.tran_texts[2:4]
        self.project.copy_texts([2, 3], const.DOCUMENT.TRAN)
        assert self.project.paste_texts(0, const.DOCUMENT.MAIN) == [0, 1]
        assert self.project.main_texts[0:2] == texts

    @reversion_test
    def test_paste_texts_excess(self):

        self.project.clipboard.data = ["x"] * 99
        rows = self.project.paste_texts(1, const.DOCUMENT.MAIN)
        assert rows == range(1, 100)
        assert len(self.project.times) == 100
        for i in range(1, 100):
            assert self.project.main_texts[i] == "x"

    @reversion_test
    def test_remove_subtitles(self):

        orig_length = len(self.project.times)
        self.project.remove_subtitles([2, 3])
        assert len(self.project.times) == orig_length - 2

    @reversion_test
    def test_split_subtitle(self):

        orig_times = self.project.times[1]
        orig_frames = self.project.frames[1]
        orig_length = len(self.project.times)
        self.project.split_subtitle(1)
        assert len(self.project.times) == orig_length + 1
        assert self.project.times[1][HIDE] == self.project.times[2][SHOW]
        assert self.project.frames[1][HIDE] == self.project.frames[2][SHOW]
        assert self.project.times[2][SHOW] > orig_times[SHOW]
        assert self.project.times[2][SHOW] < orig_times[HIDE]
        assert self.project.frames[2][SHOW] > orig_frames[SHOW]
        assert self.project.frames[2][SHOW] < orig_frames[HIDE]
        assert self.project.times[2][HIDE] == orig_times[HIDE]
        assert self.project.frames[2][HIDE] == orig_frames[HIDE]
        assert self.project.main_texts[2] == ""
        assert self.project.tran_texts[2] == ""
