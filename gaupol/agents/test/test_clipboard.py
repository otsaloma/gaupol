# Copyright (C) 2005-2007 Osmo Salomaa
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


from gaupol import const
from gaupol.unittest import TestCase, reversion_test


class TestClipboardAgent(TestCase):

    def setup_method(self, method):

        self.project = self.get_project()

    def test_copy_texts(self):

        text_0 = self.project.subtitles[0].main_text
        text_2 = self.project.subtitles[2].main_text
        self.project.copy_texts([0, 2], const.DOCUMENT.MAIN)
        texts = self.project.clipboard.get_texts()
        assert texts == [text_0, None, text_2]

    @reversion_test
    def test_cut_texts(self):

        text_0 = self.project.subtitles[0].main_text
        text_2 = self.project.subtitles[2].main_text
        self.project.cut_texts([0, 2], const.DOCUMENT.MAIN)
        texts = self.project.clipboard.get_texts()
        assert texts == [text_0, None, text_2]
        assert self.project.subtitles[0].main_text == ""
        assert self.project.subtitles[2].main_text == ""

    @reversion_test
    def test_paste_texts__excess(self):

        subtitles = self.project.subtitles
        self.project.copy_texts([0, 1], const.DOCUMENT.TRAN)
        last_index = len(subtitles) - 1
        indexes = self.project.paste_texts(last_index, const.DOCUMENT.MAIN)
        assert indexes == [last_index, last_index + 1]
        assert len(subtitles) == last_index + 2

    @reversion_test
    def test_paste_texts__fit(self):

        subtitles = self.project.subtitles
        self.project.copy_texts([0, 1], const.DOCUMENT.TRAN)
        indexes = self.project.paste_texts(2, const.DOCUMENT.MAIN)
        assert indexes == [2, 3]
        assert subtitles[0].main_text == subtitles[2].main_text
        assert subtitles[1].main_text == subtitles[3].main_text
