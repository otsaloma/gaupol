# Copyright (C) 2005-2006 Osmo Salomaa
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


from gaupol.base                 import cons
from gaupol.base.file.classes    import *
from gaupol.base.file.determiner import FileFormatDeterminer
from gaupol.test                 import Test


class TestFileFormatDeterminer(Test):

    def test_determine(self):

        for format, name in enumerate(cons.Format.class_names):
            if name == 'MicroDVD':
                continue
            path = self.get_subrip_path()
            file_ = SubRip(path, 'utf_8')
            data = file_.read()
            file_ = eval(name)(path, 'utf_8', file_.newlines)
            file_.write(*data)
            determiner = FileFormatDeterminer(path, 'utf_8')
            assert determiner.determine() == format

        path = self.get_microdvd_path()
        determiner = FileFormatDeterminer(path, 'utf_8')
        assert determiner.determine() == cons.Format.MICRODVD
