# Copyright (C) 2005-2007 Osmo Salomaa
#
# This file is part of Gaupol.
#
# Gaupol is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# Gaupol is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# Gaupol.  If not, see <http://www.gnu.org/licenses/>.

import gaupol

from gaupol import unittest


class TestEditAgent(unittest.TestCase):

    def setup_method(self, method):

        self.project = self.get_project()

    @unittest.reversion_test
    def test_clear_texts(self):

        self.project.clear_texts([0, 1], gaupol.DOCUMENT.MAIN)
        assert self.project.subtitles[0].main_text == ""
        assert self.project.subtitles[1].main_text == ""

    @unittest.reversion_test
    def test_insert_blank_subtitles__end(self):

        subtitles = self.project.subtitles
        orig_length = len(subtitles)
        indices = range(orig_length, orig_length + 10)
        self.project.insert_blank_subtitles(indices)
        assert len(subtitles) == orig_length + 10
        for i in range(0, len(subtitles) - 1):
            assert subtitles[i] <= subtitles[i + 1]

    @unittest.reversion_test
    def test_insert_blank_subtitles__middle(self):

        subtitles = self.project.subtitles
        orig_length = len(subtitles)
        self.project.insert_blank_subtitles([1, 2, 3])
        assert len(subtitles) == orig_length + 3
        for i in range(0, len(subtitles) - 1):
            assert subtitles[i] <= subtitles[i + 1]

    @unittest.reversion_test
    def test_insert_blank_subtitles__start(self):

        subtitles = self.project.subtitles
        orig_length = len(subtitles)
        self.project.insert_blank_subtitles([0, 1])
        assert len(subtitles) == orig_length + 2
        for i in range(0, len(subtitles) - 1):
            assert subtitles[i] <= subtitles[i + 1]

    @unittest.reversion_test
    def test_insert_subtitles(self):

        subtitles = self.project.subtitles
        orig_length = len(subtitles)
        new_subtitles = []
        for i in range(3):
            subtitle = self.project.get_subtitle()
            subtitle.start = i
            subtitle.end = i + 1
            subtitle.main_text = str(i)
            subtitle.tran_text = str(i)
            new_subtitles.append(subtitle)
        self.project.insert_subtitles([0, 1, 2], new_subtitles)
        assert len(subtitles) == orig_length + 3
        assert subtitles[0:3] == new_subtitles

    @unittest.reversion_test
    def test_merge_subtitles(self):

        subtitles = self.project.subtitles
        subtitle_1 = subtitles[1].copy()
        subtitle_2 = subtitles[2].copy()
        orig_length = len(subtitles)
        self.project.merge_subtitles([1, 2])
        assert len(subtitles) == orig_length - 1
        assert subtitles[1].start == subtitle_1.start
        assert subtitles[1].end == subtitle_2.end

    @unittest.reversion_test
    def test_remove_subtitles(self):

        subtitles = self.project.subtitles
        orig_length = len(subtitles)
        self.project.remove_subtitles([2, 3])
        assert len(subtitles) == orig_length - 2

    @unittest.reversion_test
    def test_replace_positions(self):

        new_subtitles = []
        for i in range(3):
            subtitle = self.project.get_subtitle()
            subtitle.start = i
            subtitle.end = i + 1
            new_subtitles.append(subtitle)
        self.project.replace_positions([0, 1, 2], new_subtitles)
        subtitles = self.project.subtitles
        for i in range(3):
            assert subtitles[i].start == new_subtitles[i].start
            assert subtitles[i].end == new_subtitles[i].end

    @unittest.reversion_test
    def test_replace_texts(self):

        doc = gaupol.DOCUMENT.MAIN
        self.project.replace_texts([1, 2], doc, ["", ""])
        assert self.project.subtitles[1].main_text == ""
        assert self.project.subtitles[2].main_text == ""

    @unittest.reversion_test
    def test_split_subtitle(self):

        subtitles = self.project.subtitles
        subtitle = subtitles[1].copy()
        orig_length = len(subtitles)
        self.project.split_subtitle(1)
        assert len(subtitles) == orig_length + 1
        assert subtitles[1].start == subtitle.start
        assert subtitles[1].end < subtitle.end
        assert subtitles[2].start < subtitle.end
        assert subtitles[2].end == subtitle.end
