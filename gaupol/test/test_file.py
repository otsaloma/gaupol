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
import sys


class PuppetSubtitleFile(gaupol.SubtitleFile):

    format = gaupol.formats.SUBVIEWER2
    mode = gaupol.modes.TIME


class TestSubtitleFile(gaupol.TestCase):

    def setup_method(self, method):

        path = self.new_temp_file(PuppetSubtitleFile.format)
        newline = gaupol.newlines.UNIX
        self.file = PuppetSubtitleFile(path, "ascii", newline)

    def test__read_lines(self):

        fobj = open(self.file.path, "a")
        fobj.write("\n\r\n\n")
        fobj.close()
        lines = self.file._read_lines()
        assert lines
        for line in lines:
            assert not line.endswith("\n")
        assert lines[-1]

    def test_copy_from(self):

        self.file.header = "test"
        format = gaupol.formats.SUBVIEWER2
        path = self.new_temp_file(PuppetSubtitleFile.format)
        new_file = PuppetSubtitleFile(path, "ascii")
        new_file.copy_from(self.file)
        assert new_file.header == "test"

    def test_get_template_header(self):

        assert self.file.get_template_header()
        global_dir = gaupol.DATA_DIR
        local_dir = gaupol.DATA_HOME_DIR
        gaupol.DATA_DIR = local_dir
        gaupol.DATA_HOME_DIR = global_dir
        assert self.file.get_template_header()
        gaupol.DATA_DIR = global_dir
        gaupol.DATA_HOME_DIR = local_dir

    def test_read(self):

        function = self.file.read
        self.raises(NotImplementedError, function)

    def test_write(self):

        function = self.file.write
        doc = gaupol.documents.MAIN
        self.raises(NotImplementedError, function, (), doc)

    def test_write_to_file(self):

        function = self.file.write_to_file
        doc = gaupol.documents.MAIN
        fobj = sys.stdout
        self.raises(NotImplementedError, function, (), doc, fobj)
