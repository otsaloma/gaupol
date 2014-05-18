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


class TestTMPlayerOneDigitHour(aeidon.TestCase):

    format = aeidon.formats.TMPLAYER
    name = "tmplayer-1"

    def setup_method(self, method):
        path = self.new_temp_file(self.format, self.name)
        self.file = aeidon.files.new(self.format, path, "ascii")

    def test_read(self):
        assert self.file.read()

    def test_write(self):
        self.file.write(self.file.read(), aeidon.documents.MAIN)
        text = open(self.file.path, "r").read().strip()
        assert text == self.get_sample_text(self.format, self.name)


class TestTMPlayerTwoDigitHour(TestTMPlayerOneDigitHour):

    name = "tmplayer-2"
