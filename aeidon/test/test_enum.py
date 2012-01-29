# Copyright (C) 2005-2009,2011 Osmo Salomaa
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
        self.parent = object()
        self.item_0 = aeidon.EnumerationItem(0, "a", self.parent)
        self.item_1 = aeidon.EnumerationItem(1, "b", self.parent)
        self.item_2 = aeidon.EnumerationItem(2, "c", self.parent)

    def test___bool__(self):
        assert self.item_0
        assert self.item_1
        assert self.item_2

    def test___eq__(self):
        assert self.item_0 == self.item_0
        assert self.item_0 == 0

    def test___ge__(self):
        assert self.item_1 >= self.item_0
        assert self.item_1 >= self.item_1
        assert self.item_1 >= 0
        assert self.item_1 >= 1

    def test___gt__(self):
        assert self.item_2 > self.item_1
        assert self.item_2 > 1

    def test___hash__(self):
        {self.item_0: 0,
         self.item_1: 1,
         self.item_2: 2}

    def test___le__(self):
        assert self.item_1 <= self.item_2
        assert self.item_1 <= self.item_1
        assert self.item_1 <= 2
        assert self.item_1 <= 1

    def test___lt__(self):
        assert self.item_0 < self.item_1
        assert self.item_0 < 1

    def test___ne__(self):
        assert self.item_0 != self.item_1
        assert self.item_0 != 1

    def test___str__(self):
        assert str(self.item_0) == "a"
        assert str(self.item_1) == "b"
        assert str(self.item_2) == "c"


class TestEnumeration(aeidon.TestCase):

    def setup_method(self, method):
        self.fruits = aeidon.Enumeration()
        self.fruits.APPLE = aeidon.EnumerationItem()
        self.fruits.MANGO = aeidon.EnumerationItem()
        self.fruits.APPLE.size = 10
        self.fruits.MANGO.size = 20

    def test___contains____enum(self):
        assert self.fruits.APPLE in self.fruits
        assert self.fruits.MANGO in self.fruits

    def test___contains____int(self):
        assert 0 in self.fruits
        assert 1 in self.fruits

    def test___contains____other(self):
        item = aeidon.EnumerationItem(0, "test", object())
        assert not item in self.fruits

    def test___delattr__(self):
        value = self.fruits.MANGO
        delattr(self.fruits, "MANGO")
        assert not hasattr(self.fruits, "MANGO")
        assert not value in self.fruits

    def test___setattr__(self):
        assert self.fruits.APPLE == 0
        assert self.fruits.MANGO == 1
        assert self.fruits.APPLE.name == "APPLE"
        assert self.fruits.MANGO.name == "MANGO"
        assert self.fruits.APPLE.size == 10
        assert self.fruits.MANGO.size == 20

    def test_find_item(self):
        assert self.fruits.find_item("size", 10) == self.fruits.APPLE
        assert self.fruits.find_item("size", 20) == self.fruits.MANGO

    def test_find_item__value_error(self):
        self.assert_raises(ValueError,
                           self.fruits.find_item,
                           "size", 30)
