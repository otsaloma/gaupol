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
import os


class TestOpenAgent(aeidon.TestCase):

    def setup_method(self, method):
        self.project = self.new_project()
        self.delegate = self.project.open_main.__self__

    def test_open__main(self):
        for format in aeidon.formats:
            self.project.remove_subtitles((0,))
            self.project.open(aeidon.documents.MAIN,
                              self.new_temp_file(format),
                              "ascii")

            assert self.project.subtitles

    def test_open__translation(self):
        for format in aeidon.formats:
            self.project.remove_subtitles((0,))
            self.project.open(aeidon.documents.TRAN,
                              self.new_temp_file(format),
                              "ascii")

    def test_open_main(self):
        for format in aeidon.formats:
            self.project.remove_subtitles((0,))
            self.project.open_main(self.new_temp_file(format),
                                   "ascii")

            assert self.project.subtitles

    def test_open_main__bom(self):
        path = self.new_subrip_file()
        blob = open(path, "rb").read()
        open(path, "wb").write(codecs.BOM_UTF8 + blob)
        self.project.open_main(path, "ascii")
        assert self.project.subtitles
        assert self.project.main_file.encoding == "utf_8_sig"

    def test_open_main__io_error(self):
        path = self.new_subrip_file()
        os.chmod(path, 0000)
        self.assert_raises(IOError,
                           self.project.open_main,
                           path, "ascii")

        os.chmod(path, 0o777)

    def test_open_main__parse_error(self):
        path = self.new_subrip_file()
        f = open(path, "w")
        f.write("00:00:01,000 --> 00:00:02,000\n\n")
        f.write("00:00:03,000 <-- 00:00:04,000\n\n")
        f.close()
        self.assert_raises(aeidon.ParseError,
                           self.project.open_main,
                           path, "ascii")

    def test_open_main__unicode_error(self):
        self.assert_raises(UnicodeError,
                           self.project.open_main,
                           self.new_subrip_file(),
                           "punycode")

    def test_open_main__unsorted(self):
        path = self.new_microdvd_file()
        f = open(path, "w")
        f.write("{100}{200}\n")
        f.write("{500}{600}\n")
        f.write("{300}{400}\n")
        f.close()
        assert self.project.open_main(path, "ascii") == 1

    def test_open_translation__align_number(self):
        for format in aeidon.formats:
            self.project.remove_subtitles((0,))
            self.project.open_translation(self.new_temp_file(format),
                                          "ascii",
                                          aeidon.align_methods.NUMBER)

    def test_open_translation__align_position(self):
        for format in aeidon.formats:
            self.project.remove_subtitles((0,))
            self.project.open_translation(self.new_temp_file(format),
                                          "ascii",
                                          aeidon.align_methods.POSITION)

    def test_open_translation__bom(self):
        path = self.new_subrip_file()
        blob = open(path, "rb").read()
        open(path, "wb").write(codecs.BOM_UTF8 + blob)
        self.project.open_translation(path, "ascii")
        assert self.project.tran_file.encoding == "utf_8_sig"
