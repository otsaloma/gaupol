# Copyright (C) 2005-2009 Osmo Salomaa
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
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# Gaupol. If not, see <http://www.gnu.org/licenses/>.

import aeidon


class TestEnumerationItem(aeidon.TestCase):

    def setup_method(self, method):
        self.item = aeidon.EnumerationItem(0, "test", object())

    def test___bool__(self):
        assert self.item

    def test___cmp____equal(self):
        if not aeidon.debug: return
        assert self.item == self.item
        assert self.item == 0

    def test___cmp____value_error(self):
        if not aeidon.debug: return
        other = aeidon.EnumerationItem(0, "rest", object())
        self.raises(ValueError, cmp, self.item, other)
        self.raises(ValueError, cmp, self.item, "xxx")

    def test___str__(self):
        assert str(self.item) == "test"


class TestEnumeration(aeidon.TestCase):

    def setup_method(self, method):
        self.fruits = aeidon.Enumeration()
        self.fruits.APPLE = aeidon.EnumerationItem()
        self.fruits.APPLE.size = 10
        self.fruits.MANGO = aeidon.EnumerationItem()
        self.fruits.MANGO.size = 15

    def test___contains____different(self):
        if not aeidon.debug: return
        item = aeidon.EnumerationItem(0, "test", object())
        assert not item in self.fruits

    def test___contains____int(self):
        if not aeidon.debug: return
        assert 0 in self.fruits
        assert 1 in self.fruits

    def test___contains____item(self):
        if not aeidon.debug: return
        assert self.fruits.APPLE in self.fruits
        assert self.fruits.MANGO in self.fruits

    def test___setattr__(self):
        assert self.fruits.APPLE == 0
        assert self.fruits.MANGO == 1
        assert self.fruits.APPLE.name == "APPLE"
        assert self.fruits.MANGO.name == "MANGO"
        assert self.fruits.APPLE.size == 10
        assert self.fruits.MANGO.size == 15

    def test_find_item(self):
        find_item = self.fruits.find_item
        assert find_item("size", 10) == self.fruits.APPLE
        assert find_item("size", 15) == self.fruits.MANGO

    def test_find_item__value_error(self):
        find_item = self.fruits.find_item
        self.raises(ValueError, find_item, "size", 20)
