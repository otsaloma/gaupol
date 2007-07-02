# Copyright (C) 2005-2007 Osmo Salomaa
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
# A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# Gaupol.  If not, see <http://www.gnu.org/licenses/>.


import gaupol

from gaupol import unittest
from .. import determiner


class TestFormatDeterminer(unittest.TestCase):

    def setup_method(self, method):

        self.determiner = determiner.FormatDeterminer()

    def test_determine(self):

        path = self.get_subrip_path()
        for format in gaupol.FORMAT.members:
            text = self.get_file_text(format)
            gaupol.util.write(path, text, "ascii")
            value = self.determiner.determine(path, "ascii")
            assert value == format

        gaupol.util.write(path, "", "ascii")
        function = self.determiner.determine
        self.raises(gaupol.FormatError, function, path, "ascii")
