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


class TestOpenAgent(aeidon.TestCase):

    def setup_method(self, method):
        self.project = self.new_project()

    def test_open_main(self):
        for format in aeidon.formats:
            path = self.new_temp_file(format)
            self.project.open_main(path, "ascii")
            assert self.project.subtitles

    def test_open_main__bom(self):
        path = self.new_subrip_file()
        blob = open(path, "rb").read()
        open(path, "wb").write(codecs.BOM_UTF8 + blob)
        self.project.open_main(path, "ascii")
        assert self.project.subtitles
        assert self.project.main_file.encoding == "utf_8_sig"

    def test_open_main__sort(self):
        path = self.new_microdvd_file()
        with open(path, "w") as f:
            f.write("{100}{200}\n")
            f.write("{500}{600}\n")
            f.write("{300}{400}\n")
        sort_count = self.project.open_main(path, "ascii")
        assert sort_count == 1

    def test_open_translation__align_number(self):
        for format in aeidon.formats:
            path = self.new_temp_file(format)
            method = aeidon.align_methods.NUMBER
            self.project.open_translation(path, "ascii", method)

    def test_open_translation__align_position(self):
        for format in aeidon.formats:
            path = self.new_temp_file(format)
            method = aeidon.align_methods.POSITION
            self.project.open_translation(path, "ascii", method)

    def test_open_translation__bom(self):
        path = self.new_subrip_file()
        blob = open(path, "rb").read()
        open(path, "wb").write(codecs.BOM_UTF8 + blob)
        self.project.open_translation(path, "ascii")
        assert self.project.subtitles
        assert self.project.tran_file.encoding == "utf_8_sig"
