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

MAIN = aeidon.documents.MAIN
TRAN = aeidon.documents.TRAN


class TestRegisterAgent(aeidon.TestCase):

    def setup_method(self, method):
        self.project = self.new_project()
        self.delegate = self.project.undo.__self__

    def test_redo(self):
        text_0 = self.project.subtitles[0].main_text
        text_1 = self.project.subtitles[1].main_text
        text_2 = self.project.subtitles[2].main_text
        self.project.clear_texts((0,), MAIN)
        self.project.clear_texts((1,), MAIN)
        self.project.clear_texts((2,), MAIN)
        self.project.undo(3)
        assert self.project.subtitles[0].main_text == text_0
        assert self.project.subtitles[1].main_text == text_1
        assert self.project.subtitles[2].main_text == text_2
        self.project.redo(1)
        self.project.redo(2)
        assert self.project.subtitles[0].main_text == ""
        assert self.project.subtitles[1].main_text == ""
        assert self.project.subtitles[2].main_text == ""

    def test_undo(self):
        text_0 = self.project.subtitles[0].main_text
        text_1 = self.project.subtitles[1].main_text
        text_2 = self.project.subtitles[2].main_text
        self.project.clear_texts((0,), MAIN)
        self.project.clear_texts((1,), MAIN)
        self.project.clear_texts((2,), MAIN)
        self.project.undo(1)
        self.project.undo(2)
        assert self.project.subtitles[0].main_text == text_0
        assert self.project.subtitles[1].main_text == text_1
        assert self.project.subtitles[2].main_text == text_2
        self.project.redo(3)
        assert self.project.subtitles[0].main_text == ""
        assert self.project.subtitles[1].main_text == ""
        assert self.project.subtitles[2].main_text == ""
