# Copyright (C) 2005-2008 Osmo Salomaa
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

import gaupol


class TestSubStationAlpha(gaupol.TestCase):

    def setup_method(self, method):

        format = gaupol.formats.SSA
        path = self.get_file_path(format)
        self.file = gaupol.files.new(format, path, "ascii")

    def test_copy_from(self):

        self.file.header = "test"
        self.file.event_fields = ("Marked",)
        path = self.get_file_path(self.file.format)
        new_file = gaupol.files.new(self.file.format, path, "ascii")
        new_file.copy_from(self.file)
        assert new_file.header == "test"
        assert new_file.event_fields == ("Marked",)

    def test_read(self):

        assert self.file.read()
        assert self.file.header

    def test_write(self):

        subtitles = self.file.read()
        doc = gaupol.documents.MAIN
        self.file.write(subtitles, doc)
        text = open(self.file.path, "r").read().strip()
        reference = self.get_file_text(self.file.format)
        assert text == reference
