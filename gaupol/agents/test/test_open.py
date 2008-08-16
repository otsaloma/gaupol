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
import os


class TestOpenAgent(gaupol.TestCase):

    def setup_method(self, method):

        self.project = self.get_project()
        self.delegate = self.project.open_main.im_self

    def test_open_main(self):

        for format in gaupol.formats:
            path = self.get_file_path(format)
            self.project.remove_subtitles([0])
            self.project.open_main(path, "ascii")
            assert self.project.subtitles

    def test_open_main__io_error(self):

        path = self.get_subrip_path()
        os.chmod(path, 0000)
        function = self.project.open_main
        self.raises(IOError, function, path, "ascii")
        os.chmod(path, 0777)

    def test_open_main__mpsub(self):

        path = self.get_file_path(gaupol.formats.MPSUB, "mpsub-frame")
        self.project.open_main(path, "ascii")
        assert self.project.framerate == self.project.main_file.framerate

    def test_open_main__parse_error(self):

        path = self.get_subrip_path()
        fobj = open(path, "w")
        fobj.write("00:00:01,000 --> 00:00:02,000\n\n")
        fobj.write("00:00:03,000 >>> 00:00:04,000\n\n")
        fobj.close()
        function = self.project.open_main
        self.raises(gaupol.ParseError, function, path, "ascii")

    def test_open_main__unicode_error(self):

        path = self.get_subrip_path()
        function = self.project.open_main
        self.raises(UnicodeError, function, path, "punycode")

    def test_open_main__unsorted(self):

        path = self.get_microdvd_path()
        fobj = open(path, "w")
        fobj.write("{100}{200}\n")
        fobj.write("{500}{600}\n")
        fobj.write("{300}{400}\n")
        fobj.close()
        assert self.project.open_main(path, "ascii") == 1

    def test_open_translation__align_number(self):

        align_method = gaupol.align_methods.NUMBER
        for format in gaupol.formats:
            path = self.get_file_path(format)
            self.project.remove_subtitles([0])
            self.project.open_translation(path, "ascii", align_method)

    def test_open_translation__align_position(self):

        align_method = gaupol.align_methods.POSITION
        for format in gaupol.formats:
            path = self.get_file_path(format)
            self.project.remove_subtitles([0])
            self.project.open_translation(path, "ascii", align_method)
