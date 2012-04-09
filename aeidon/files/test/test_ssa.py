# -*- coding: utf-8-unix -*-

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


class TestSubStationAlpha(aeidon.TestCase):

    format = aeidon.formats.SSA

    def setup_method(self, method):
        self.file = aeidon.files.new(self.format,
                                     self.new_temp_file(self.format),
                                     "ascii")

    def test_copy_from(self):
        self.file.header = "test"
        self.file.event_fields = ("Marked",)
        path = self.new_temp_file(self.format)
        new_file = aeidon.files.new(self.format, path, "ascii")
        new_file.copy_from(self.file)
        assert new_file.header == "test"
        assert new_file.event_fields == ("Marked",)

    def test_read(self):
        assert self.file.read()
        assert self.file.header

    def test_write(self):
        self.file.write(self.file.read(), aeidon.documents.MAIN)
        text = open(self.file.path, "r").read().strip()
        reference = self.get_sample_text(self.format)
        assert text == reference
