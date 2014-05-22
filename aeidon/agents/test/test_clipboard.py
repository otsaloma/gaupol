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


class TestClipboardAgent(aeidon.TestCase):

    def setup_method(self, method):
        self.project = self.new_project()

    @aeidon.deco.reversion_test
    def test_cut_texts(self):
        self.project.cut_texts((0, 2), aeidon.documents.MAIN)

    @aeidon.deco.reversion_test
    def test_paste_texts(self):
        self.project.copy_texts((0, 1), aeidon.documents.TRAN)
        self.project.paste_texts(2, aeidon.documents.MAIN)

    @aeidon.deco.reversion_test
    def test_paste_texts__new(self):
        nsubtitles = len(self.project.subtitles)
        self.project.copy_texts((0, 1), aeidon.documents.TRAN)
        self.project.paste_texts(nsubtitles-1, aeidon.documents.MAIN)
        assert len(self.project.subtitles) == nsubtitles + 1
