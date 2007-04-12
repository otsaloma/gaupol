# Copyright (C) 2005-2007 Osmo Salomaa
#
# This file is part of Gaupol.
#
# Gaupol is free software; you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.
#
# Gaupol is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# Gaupol; if not, write to the Free Software Foundation, Inc., 51 Franklin
# Street, Fifth Floor, Boston, MA 02110-1301, USA.


from gaupol import const
from gaupol.unittest import TestCase
from .. import _subfile


class TestSubtitleFile(TestCase):

    def setup_method(self, method):

        path = self.get_subrip_path()
        self.file = _subfile.SubtitleFile(path, "ascii")

    def test_attributes(self):

        if self.file.__class__ != _subfile.SubtitleFile:
            assert self.file.format in const.FORMAT.members
            assert self.file.mode in const.MODE.members
            assert isinstance(self.file.has_header, bool)
            self.file.identifier.findall("test")

    def test__read_lines(self):

        assert self.file._read_lines()

    def test_get_template_header(self):

        if self.file.has_header:
            header = self.file.get_template_header()
            assert isinstance(header, basestring)

    def test_read(self):

        if self.file.__class__ != _subfile.SubtitleFile:
            path = self.get_file_path(self.file.format)
            self.file.path = path
            assert self.file.read()

    def test_write(self):

        if self.file.__class__ != _subfile.SubtitleFile:
            path = self.get_file_path(self.file.format)
            self.file.path = path
            self.file.newline = const.NEWLINE.UNIX
            data = self.file.read()
            self.file.write(*data)
