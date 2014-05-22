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


class TestSetAgent(aeidon.TestCase):

    def setup_method(self, method):
        self.project = self.new_project()

    @aeidon.deco.reversion_test
    def test_set_duration(self):
        subtitles = self.project.subtitles
        self.project.set_duration(0, "00:01:11.111")
        assert subtitles[0].duration_time == "00:01:11.111"

    @aeidon.deco.reversion_test
    def test_set_end(self):
        subtitles = self.project.subtitles
        self.project.set_end(0, 600000)
        assert subtitles[0].end_frame == 600000

    @aeidon.deco.reversion_test
    def test_set_main_text(self):
        subtitles = self.project.subtitles
        self.project.set_main_text(0, "m")
        assert subtitles[0].main_text == "m"

    @aeidon.deco.reversion_test
    def test_set_start(self):
        subtitles = self.project.subtitles
        self.project.set_start(0, -100.0)
        assert subtitles[0].start_seconds == -100.0

    @aeidon.deco.reversion_test
    def test_set_start__reorder(self):
        subtitles = self.project.subtitles
        text_0 = subtitles[0].main_text
        text_3 = subtitles[3].main_text
        self.project.set_start(3, -1000)
        assert subtitles[0].start_frame == -1000
        assert subtitles[0].main_text == text_3
        assert subtitles[1].main_text == text_0

    @aeidon.deco.reversion_test
    def test_set_text__main(self):
        subtitles = self.project.subtitles
        self.project.set_text(0, aeidon.documents.MAIN, "m")
        assert subtitles[0].main_text == "m"

    @aeidon.deco.reversion_test
    def test_set_text__translation(self):
        subtitles = self.project.subtitles
        self.project.set_text(0, aeidon.documents.TRAN, "t")
        assert subtitles[0].tran_text == "t"

    @aeidon.deco.reversion_test
    def test_set_translation_text(self):
        subtitles = self.project.subtitles
        self.project.set_translation_text(0, "t")
        assert subtitles[0].tran_text == "t"
