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


import re

from gaupol.base              import cons
from gaupol.base.file         import SubtitleFile
from gaupol.base.file.classes import *
from gaupol.test              import Test


class TestSubtitleFile(Test):

    def test_get_newline_character(self):

        for i, value in enumerate(cons.Newlines.values):
            file_ = SubtitleFile('test', 'utf_8', i)
            chars = file_._get_newline_character()
            assert chars == value

    def test_attributes(self):

        for name in cons.Format.class_names:
            cls = eval(name)
            assert isinstance(cls.format, int)
            assert isinstance(cls.mode, int)
            assert isinstance(cls.has_header, bool)
            re.compile(*cls.identifier)

    def test_read_lines(self):

        path = self.get_subrip_path()
        file_ = SubtitleFile(path, 'utf_8')
        lines = file_._read_lines()
        assert file_.newlines in range(3)
        assert len(lines) > 0
        for line in lines:
            assert isinstance(line, basestring)

    def test_get_template_header(self):

        path = self.get_subrip_path()
        for name in cons.Format.class_names:
            cls = eval(name)
            if cls.has_header:
                file_ = cls(path, 'utf_8')
                header = file_.get_template_header()
                assert isinstance(header, basestring)

    def test_read_and_write(self):

        for name in cons.Format.class_names:
            if name == 'MicroDVD':
                continue
            path = self.get_subrip_path()
            file_ = SubRip(path, 'utf_8')
            data = file_.read()
            file_ = eval(name)(path, 'utf_8', file_.newlines)
            file_.write(*data)
            data_1 = file_.read()
            file_.write(*data_1)
            data_2 = file_.read()
            assert data_2 == data_1

        path = self.get_microdvd_path()
        file_ = MicroDVD(path, 'utf_8')
        data_1 = file_.read()
        file_.write(*data_1)
        data_2 = file_.read()
        assert data_2 == data_1
