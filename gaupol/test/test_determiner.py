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


from gaupol import cons, util
from gaupol.errors import FormatError
from gaupol.unittest import TestCase
from .. import determiner


class TestFormatDeterminer(TestCase):

    def setup_method(self, method):

        self.determiner = determiner.FormatDeterminer("", "ascii")

    def test___init__(self):

        assert self.determiner.re_ids

    def test_determine(self):

        self.determiner.path = self.get_subrip_path()
        assert self.determiner.determine() == cons.FORMAT.SUBRIP

        self.determiner.path = self.get_microdvd_path()
        assert self.determiner.determine() == cons.FORMAT.MICRODVD

        path = self.get_subrip_path()
        util.write(path, "test", "ascii")
        self.determiner.path = path
        try:
            self.determiner.determine()
            raise AssertionError
        except FormatError:
            pass
