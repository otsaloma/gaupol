# Copyright (C) 2005-2006 Osmo Salomaa
#
# This file is part of Gaupol.
#
# Gaupol is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Gaupol is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Gaupol; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA


from gaupol.base.cons import Newlines
from gaupol.base.file import SubtitleFile
from gaupol.test      import Test


class TestSubtitleFile(Test):

    def test_init(self):

        SubtitleFile('test', 'utf_8')
        SubtitleFile('test', 'utf_8', Newlines.UNIX)

    def test_get_newline_character(self):

        for i, value in enumerate(Newlines.values):
            sub_file = SubtitleFile('test', 'utf_8', i)
            chars = sub_file._get_newline_character()
            assert chars == value

    def test_read_lines(self):

        path = self.get_subrip_path()
        sub_file = SubtitleFile(path, 'utf_8')
        lines = sub_file._read_lines()
        assert sub_file.newlines in range(3)
        assert len(lines) > 0
        for line in lines:
            assert isinstance(line, basestring)
