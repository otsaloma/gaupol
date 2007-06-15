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


from gaupol import unittest
from .. import const


class TestConstantMember(unittest.TestCase):

    def setup_method(self, method):

        self.member = const.ConstantMember(0, "test")

    def test___str__(self):

        assert str(self.member) == "test"


class TestConstantSection(unittest.TestCase):

    def setup_method(self, method):

        self.FRUIT = const.ConstantSection()
        self.FRUIT.APPLE = const.ConstantMember()
        self.FRUIT.APPLE.color = "green"
        self.FRUIT.ORANGE = const.ConstantMember()
        self.FRUIT.ORANGE.color = "orange"
        self.FRUIT.finalize()

    def test_attributes(self):

        assert self.FRUIT.APPLE == 0
        assert self.FRUIT.APPLE.name == "APPLE"
        assert self.FRUIT.APPLE.color == "green"
        assert self.FRUIT.members[0] == self.FRUIT.APPLE
        assert self.FRUIT.names[0] == "APPLE"
        assert self.FRUIT.colors[0] == "green"

        assert self.FRUIT.ORANGE == 1
        assert self.FRUIT.ORANGE.name == "ORANGE"
        assert self.FRUIT.ORANGE.color == "orange"
        assert self.FRUIT.members[1] == self.FRUIT.ORANGE
        assert self.FRUIT.names[1] == "ORANGE"
        assert self.FRUIT.colors[1] == "orange"
