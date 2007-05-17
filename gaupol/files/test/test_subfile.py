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


def omit_abstract(function):

    def wrapper(*args, **kwargs):
        if args[0].__class__ != TestSubtitleFile:
            return function(*args, **kwargs)
        return None

    return wrapper


class TestSubtitleFile(TestCase):

    def setup_method(self, method):

        self.file = None

    @omit_abstract
    def test__read_lines(self):

        assert self.file._read_lines()

    @omit_abstract
    def test_get_template_header(self):

        if self.file.format.has_header:
            self.file.get_template_header()

    @omit_abstract
    def test_read(self):

        path = self.get_file_path(self.file.format)
        self.file.path = path
        assert self.file.read()

    @omit_abstract
    def test_write(self):

        path = self.get_file_path(self.file.format)
        self.file.path = path
        self.file.newline = const.NEWLINE.UNIX
        self.file.write(*self.file.read())
