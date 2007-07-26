# Copyright (C) 2007 Osmo Salomaa
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


import re
from gaupol import unittest
from .. import pattern


class TestPattern(unittest.TestCase):

    def setup_method(self, method):

        self.pattern = pattern.Pattern()

    def test_get_description(self):

        self.pattern.set_field("Description", "test")
        assert self.pattern.get_description(False) == "test"
        assert self.pattern.get_description(True) == "test"

    def test_get_field(self):

        self.pattern.set_field("Test", "test")
        assert self.pattern.get_field("Test") == "test"

    def test_get_flags(self):

        self.pattern.set_field("Flags", "DOTALL,UNICODE")
        flags = self.pattern.get_flags()
        assert flags == re.DOTALL | re.UNICODE

    def test_get_name(self):

        self.pattern.set_field("Name", "test")
        assert self.pattern.get_name(False) == "test"
        assert self.pattern.get_name(True) == "test"

    def test_set_field(self):

        self.pattern.set_field("Test", "test")
        assert self.pattern.get_field("Test") == "test"
