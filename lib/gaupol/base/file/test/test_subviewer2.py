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


from gaupol.base.file.subrip     import SubRip
from gaupol.base.file.subviewer2 import SubViewer2
from gaupol.test                 import Test


class TestSubViewer2(Test):

    def test_read_and_write(self):

        path = self.get_subrip_path()
        sub_file = SubRip(path, 'utf_8')
        data = sub_file.read()

        sub_file = SubViewer2(path, 'utf_8', sub_file.newlines)
        sub_file.write(*data)
        data_1 = sub_file.read()
        sub_file.write(*data_1)
        data_2 = sub_file.read()
        assert data_2 == data_1
