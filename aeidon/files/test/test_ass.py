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


class TestSubStationAlpha(aeidon.TestCase):

    format = aeidon.formats.ASS

    def setup_method(self, method):
        self.file = aeidon.files.new(self.format,
                                     self.new_temp_file(self.format),
                                     "ascii")

    def test_read(self):
        assert self.file.read()
        assert self.file.header

    def test_write(self):
        self.file.write(self.file.read(), aeidon.documents.MAIN)
        text = open(self.file.path, "r").read().strip()
        assert text == self.get_sample_text(self.format)
