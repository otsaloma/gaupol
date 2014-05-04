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
import codecs


class PuppetSubtitleFile(aeidon.SubtitleFile):

    format = aeidon.formats.SUBVIEWER2
    mode = aeidon.modes.TIME


class TestSubtitleFile(aeidon.TestCase):

    def setup_method(self, method):
        path = self.new_temp_file(PuppetSubtitleFile.format)
        newline = aeidon.newlines.UNIX
        self.file = PuppetSubtitleFile(path, "ascii", newline)

    def test_read__utf_16(self):
        path = self.new_subrip_file()
        with open(path, "r") as f:
            text = f.read()
        with open(path, "w", encoding="utf_16") as f:
            f.write(text)
        file = aeidon.files.new(aeidon.formats.SUBRIP, path, "utf_16")
        file.read()

    def test_read__utf_16_be(self):
        path = self.new_subrip_file()
        with open(path, "r") as f:
            text = f.read()
        with open(path, "w", encoding="utf_16_be") as f:
            f.write(str(codecs.BOM_UTF16_BE, "utf_16_be"))
            f.write(text)
        file = aeidon.files.new(aeidon.formats.SUBRIP, path, "utf_16_be")
        file.read()

    def test_read__utf_16_le(self):
        path = self.new_subrip_file()
        with open(path, "r") as f:
            text = f.read()
        with open(path, "w", encoding="utf_16_le") as f:
            f.write(str(codecs.BOM_UTF16_LE, "utf_16_le"))
            f.write(text)
        file = aeidon.files.new(aeidon.formats.SUBRIP, path, "utf_16_le")
        file.read()

    def test_read__utf_8_sig(self):
        path = self.new_subrip_file()
        with open(path, "r") as f:
            text = f.read()
        with open(path, "w", encoding="utf_8_sig") as f:
            f.write(text)
        file = aeidon.files.new(aeidon.formats.SUBRIP, path, "utf_8")
        file.read()
