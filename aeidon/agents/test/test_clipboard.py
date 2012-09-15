# -*- coding: utf-8 -*-

# Copyright (C) 2005-2009 Osmo Salomaa
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
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# Gaupol. If not, see <http://www.gnu.org/licenses/>.

import aeidon


class TestClipboardAgent(aeidon.TestCase):

    def setup_method(self, method):
        self.project = self.new_project()

    def test_copy_texts(self):
        text_0 = self.project.subtitles[0].main_text
        text_2 = self.project.subtitles[2].main_text
        self.project.copy_texts((0, 2), aeidon.documents.MAIN)
        texts = self.project.clipboard.get_texts()
        assert texts == [text_0, None, text_2]
        assert self.project.subtitles[0].main_text == text_0
        assert self.project.subtitles[2].main_text == text_2

    @aeidon.deco.reversion_test
    def test_cut_texts(self):
        text_0 = self.project.subtitles[0].main_text
        text_2 = self.project.subtitles[2].main_text
        self.project.cut_texts((0, 2), aeidon.documents.MAIN)
        texts = self.project.clipboard.get_texts()
        assert texts == [text_0, None, text_2]
        assert self.project.subtitles[0].main_text == ""
        assert self.project.subtitles[2].main_text == ""

    @aeidon.deco.reversion_test
    def test_paste_texts__fit(self):
        subtitles = self.project.subtitles
        self.project.copy_texts((0, 1), aeidon.documents.TRAN)
        indices = self.project.paste_texts(2, aeidon.documents.MAIN)
        assert indices == (2, 3)
        assert subtitles[0].tran_text == subtitles[2].main_text
        assert subtitles[1].tran_text == subtitles[3].main_text

    @aeidon.deco.reversion_test
    def test_paste_texts__new(self):
        subtitles = self.project.subtitles
        self.project.copy_texts((0, 1), aeidon.documents.TRAN)
        last = len(subtitles) - 1
        indices = self.project.paste_texts(last, aeidon.documents.MAIN)
        assert list(indices) == [last, last + 1]
        assert len(subtitles) == last + 2
