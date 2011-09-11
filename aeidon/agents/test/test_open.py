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
        text = open(path, "r").read()
        open(path, "w").write(codecs.BOM_UTF8 + text)
        self.project.open_main(path, "ascii")
        assert self.project.subtitles
        assert self.project.main_file.encoding == "utf_8_sig"

    def test_open_main__mpsub(self):
        self.project.remove_subtitles((0,))
        path = self.new_temp_file(aeidon.formats.MPSUB, "mpsub-frame")
        self.project.open_main(path, "ascii")
        assert self.project.subtitles

    def test_open_main__io_error(self):
        path = self.new_subrip_file()
        os.chmod(path, 0000)
        self.assert_raises(IOError,
                    self.project.open_main,
                    path, "ascii")

        os.chmod(path, 0o777)

    @aeidon.deco.monkey_patch(aeidon, "debug")
    def test_open_main__parse_error(self):
        aeidon.debug = False
        path = self.new_subrip_file()
        fobj = open(path, "w")
        fobj.write("00:00:01,000 --> 00:00:02,000\n\n")
        fobj.write("00:00:03,000 <-- 00:00:04,000\n\n")
        fobj.close()
        self.assert_raises(aeidon.ParseError,
                    self.project.open_main,
                    path, "ascii")

    def test_open_main__unicode_error(self):
        self.assert_raises(UnicodeError,
                    self.project.open_main,
                    self.new_subrip_file(), "punycode")

    def test_open_main__unsorted(self):
        path = self.new_microdvd_file()
        fobj = open(path, "w")
        fobj.write("{100}{200}\n")
        fobj.write("{500}{600}\n")
        fobj.write("{300}{400}\n")
        fobj.close()
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
        text = open(path, "r").read()
        open(path, "w").write(codecs.BOM_UTF8 + text)
        self.project.open_translation(path, "ascii")
        assert self.project.tran_file.encoding == "utf_8_sig"
