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
from .. import converter


class TestTagConverter(unittest.TestCase):

    def test_convert(self):

        for from_format in gaupol.FORMAT.members:
            for to_format in gaupol.FORMAT.members:
                conv = converter.TagConverter(from_format, to_format)
                assert conv.convert("test") == "test"
