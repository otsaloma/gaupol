# -*- coding: utf-8 -*-

# Copyright (C) 2005 Osmo Salomaa
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import aeidon


class TestEditAgent(aeidon.TestCase):

    def setup_method(self, method):
        self.project = self.new_project()

    @aeidon.deco.reversion_test
    def test_clear_texts(self):
        self.project.clear_texts((0, 1), aeidon.documents.MAIN)
        assert self.project.subtitles[0].main_text == ""
        assert self.project.subtitles[1].main_text == ""

    @aeidon.deco.reversion_test
    def test_insert_subtitles(self):
        subtitles = self.project.subtitles
        orig_length = len(subtitles)
        new_subtitles = []
        for i in range(3):
            subtitle = self.project.new_subtitle()
            subtitle.start_frame = i
            subtitle.end_frame = i + 1
            new_subtitles.append(subtitle)
        self.project.insert_subtitles((0, 1, 2), new_subtitles)
        assert len(subtitles) == orig_length + 3
        assert subtitles[0:3] == new_subtitles

    @aeidon.deco.reversion_test
    def test_insert_subtitles__blank_end(self):
        subtitles = self.project.subtitles
        orig_length = len(subtitles)
        indices = list(range(orig_length, orig_length + 3))
        self.project.insert_subtitles(indices)
        assert len(subtitles) == orig_length + 3
        assert subtitles == sorted(subtitles)

    @aeidon.deco.reversion_test
    def test_insert_subtitles__blank_middle(self):
        subtitles = self.project.subtitles
        orig_length = len(subtitles)
        self.project.insert_subtitles((1, 2, 3))
        assert len(subtitles) == orig_length + 3
        assert subtitles == sorted(subtitles)

    @aeidon.deco.reversion_test
    def test_insert_subtitles__blank_start(self):
        subtitles = self.project.subtitles
        orig_length = len(subtitles)
        self.project.insert_subtitles((0, 1, 2))
        assert len(subtitles) == orig_length + 3
        assert subtitles == sorted(subtitles)

    @aeidon.deco.reversion_test
    def test_merge_subtitles(self):
        subtitles = self.project.subtitles
        subtitle_1 = subtitles[1].copy()
        subtitle_2 = subtitles[2].copy()
        orig_length = len(subtitles)
        self.project.merge_subtitles((1, 2))
        assert len(subtitles) == orig_length - 1
        assert subtitles[1].start == subtitle_1.start
        assert subtitles[1].end == subtitle_2.end

    @aeidon.deco.reversion_test
    def test_remove_subtitles(self):
        subtitles = self.project.subtitles
        orig_length = len(subtitles)
        self.project.remove_subtitles((2, 3))
        assert len(subtitles) == orig_length - 2

    @aeidon.deco.reversion_test
    def test_replace_positions(self):
        new_subtitles = []
        for i in range(3):
            subtitle = self.project.new_subtitle()
            subtitle.start_frame = i
            subtitle.end_frame = i + 1
            new_subtitles.append(subtitle)
        self.project.replace_positions((0, 1, 2), new_subtitles)
        subtitles = self.project.subtitles
        for i in range(3):
            assert subtitles[i].start == new_subtitles[i].start
            assert subtitles[i].end == new_subtitles[i].end

    @aeidon.deco.reversion_test
    def test_replace_texts(self):
        doc = aeidon.documents.MAIN
        self.project.replace_texts((1, 2), doc, ("", ""))
        assert self.project.subtitles[1].main_text == ""
        assert self.project.subtitles[2].main_text == ""

    @aeidon.deco.reversion_test
    def test_split_subtitle(self):
        subtitles = self.project.subtitles
        subtitle = subtitles[1].copy()
        orig_length = len(subtitles)
        self.project.split_subtitle(1)
        assert len(subtitles) == orig_length + 1
        assert subtitles[1].start == subtitle.start
        assert subtitles[2].end == subtitle.end
