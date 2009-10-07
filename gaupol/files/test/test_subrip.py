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


class TestSubRip(gaupol.TestCase):

    name = "subrip"

    def setup_method(self, method):

        format = gaupol.formats.SUBRIP
        path = self.new_temp_file(format, self.name)
        self.file = gaupol.files.new(format, path, "ascii")

    def test_read(self):

        assert self.file.read()

    def test_write(self):

        subtitles = self.file.read()
        doc = gaupol.documents.MAIN
        self.file.write(subtitles, doc)
        text = open(self.file.path, "r").read().strip()
        reference = self.get_sample_text(self.file.format, self.name)
        assert text == reference


class TestSubRipExtended(TestSubRip):

    name = "subrip-extended"
