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


from gaupol import const, util
from gaupol.errors import FormatError
from gaupol.unittest import TestCase
from .. import determiner


class TestFormatDeterminer(TestCase):

    def setup_method(self, method):

        self.path = self.get_subrip_path()
        self.determiner = determiner.FormatDeterminer(self.path, "ascii")

    def test_determine(self):

        for format in const.FORMAT.members:
            text = self.get_text(format)
            util.write(self.path, text, "ascii")
            value = self.determiner.determine()
            assert value == format

        util.write(self.path, "", "ascii")
        function = self.determiner.determine
        self.raises(FormatError, function)
