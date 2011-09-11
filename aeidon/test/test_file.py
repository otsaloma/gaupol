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
import codecs
import sys


# pylint: disable=W0223
class PuppetSubtitleFile(aeidon.SubtitleFile):

    format = aeidon.formats.SUBVIEWER2
    mode = aeidon.modes.TIME


class TestSubtitleFile(aeidon.TestCase):

    def setup_method(self, method):
        path = self.new_temp_file(PuppetSubtitleFile.format)
        newline = aeidon.newlines.UNIX
        self.file = PuppetSubtitleFile(path, "ascii", newline)

    def test__read_lines(self):
        with open(self.file.path, "a") as fobj:
            fobj.write("\n\r\n\n")
        lines = self.file._read_lines()
        assert lines
        for line in lines:
            assert not line.endswith("\n")
        assert lines[-1]

    def test_copy_from(self):
        self.file.has_utf_16_bom = False
        self.file.header = "test"
        format = aeidon.formats.SUBVIEWER2
        path = self.new_temp_file(PuppetSubtitleFile.format)
        new_file = PuppetSubtitleFile(path, "ascii")
        new_file.copy_from(self.file)
        assert new_file.has_utf_16_bom == False
        assert new_file.header == "test"

    def test_read(self):
        self.assert_raises(NotImplementedError,
                    self.file.read)

    def test_read__utf_16(self):
        path = self.new_subrip_file()
        with open(path, "r") as fobj:
            text = fobj.read()
        with codecs.open(path, "w", "utf_16") as fobj:
            fobj.write(text)
        sfile = aeidon.files.new(aeidon.formats.SUBRIP, path, "utf_16")
        sfile.read()

    def test_read__utf_16_be(self):
        path = self.new_subrip_file()
        with open(path, "r") as fobj:
            text = fobj.read()
        with codecs.open(path, "w", "utf_16_be") as fobj:
            fobj.write(str(codecs.BOM_UTF16_BE, "utf_16_be"))
            fobj.write(text)
        sfile = aeidon.files.new(aeidon.formats.SUBRIP, path, "utf_16_be")
        sfile.read()

    def test_read__utf_16_le(self):
        path = self.new_subrip_file()
        with open(path, "r") as fobj:
            text = fobj.read()
        with codecs.open(path, "w", "utf_16_le") as fobj:
            fobj.write(str(codecs.BOM_UTF16_LE, "utf_16_le"))
            fobj.write(text)
        sfile = aeidon.files.new(aeidon.formats.SUBRIP, path, "utf_16_le")
        sfile.read()

    def test_read__utf_8_sig(self):
        path = self.new_subrip_file()
        with open(path, "r") as fobj:
            text = fobj.read()
        with codecs.open(path, "w", "utf_8_sig") as fobj:
            fobj.write(text)
        sfile = aeidon.files.new(aeidon.formats.SUBRIP, path, "utf_8_sig")
        sfile.read()

    def test_write(self):
        self.assert_raises(NotImplementedError,
                    self.file.write,
                    (), aeidon.documents.MAIN)

    def test_write_to_file(self):
        self.assert_raises(NotImplementedError,
                    self.file.write_to_file,
                    (), aeidon.documents.MAIN, sys.stdout)
