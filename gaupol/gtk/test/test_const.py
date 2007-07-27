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

from gaupol.gtk import unittest
from .. import const


class TestModule(unittest.TestCase):

    def test_attributes(self):

        constants = (
            ("COLUMN", (
                "actions",
                "labels",
                "names",)),
            ("FRAMERATE", (
                "actions",)),
            ("LENGTH_UNIT", (
                "names",)),
            ("MODE", (
                "actions",)),
            ("TARGET", (
                "names",)),
            ("TOOLBAR_STYLE", (
                "names",
                "values",)))

        for section_name, attr_names in constants:
            section = getattr(const, section_name)
            attr_names = attr_names + ("names",)
            for attr_name in attr_names:
                getattr(section, attr_name)
                for member in section.members:
                    getattr(member, attr_name[:-1])
