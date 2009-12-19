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

from __future__ import with_statement

import aeidon
import codecs
import sys


# pylint: disable-msg=W0223
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

    def test__read_lines__utf_16_be(self):
        with open(self.file.path, "r") as fobj:
            text = fobj.read()
        with codecs.open(self.file.path, "w", "utf_16_be") as fobj:
            fobj.write(unicode(codecs.BOM_UTF16_BE, "utf_16_be"))
            fobj.write(text)
        self.file.encoding = "utf_16_be"
        lines = self.file._read_lines()

    def test__read_lines__utf_16_le(self):
        with open(self.file.path, "r") as fobj:
            text = fobj.read()
        with codecs.open(self.file.path, "w", "utf_16_le") as fobj:
            fobj.write(unicode(codecs.BOM_UTF16_LE, "utf_16_le"))
            fobj.write(text)
        self.file.encoding = "utf_16_le"
        lines = self.file._read_lines()

    def test__read_lines__utf_8_sig(self):
        with open(self.file.path, "r") as fobj:
            text = fobj.read()
        with codecs.open(self.file.path, "w", "utf_8_sig") as fobj:
            fobj.write(text)
        self.file.encoding = "utf_8"
        lines = self.file._read_lines()
        assert self.file.encoding == "utf_8_sig"

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
        self.raises(NotImplementedError,
                    self.file.read)

    def test_write(self):
        self.raises(NotImplementedError,
                    self.file.write,
                    (), aeidon.documents.MAIN)

    def test_write_to_file(self):
        self.raises(NotImplementedError,
                    self.file.write_to_file,
                    (), aeidon.documents.MAIN, sys.stdout)
