# -*- coding: utf-8 -*-

# Copyright (C) 2007 Osmo Salomaa
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

import aeidon

class TestMetadataItem(aeidon.TestCase):

    def setup_method(self, method):
        self.item = aeidon.MetadataItem()

    def test_get_description(self):
        self.item.set_field("Description", "test")
        assert self.item.get_description(localize=False) == "test"
        assert self.item.get_description(localize=True) == "test"

    def test_get_field(self):
        assert self.item.get_field("Test") is None
        self.item.set_field("Test", "test")
        assert self.item.get_field("Test") == "test"

    def test_get_field_boolean(self):
        assert self.item.get_field("Test") is None
        self.item.set_field("Test", "True")
        assert self.item.get_field_boolean("Test") is True

    def test_get_field_list(self):
        assert self.item.get_field("Test") is None
        self.item.set_field("Test", "Yee;Haw;")
        assert self.item.get_field_list("Test") == ["Yee", "Haw"]

    def test_get_name(self):
        self.item.set_field("Name", "test")
        assert self.item.get_name(localize=False) == "test"
        assert self.item.get_name(localize=True) == "test"

    def test_get_name__missing(self):
        assert self.item.get_name(localize=False) is None
        assert self.item.get_name(localize=True) is None

    def test_has_field(self):
        assert not self.item.has_field("Test")
        self.item.set_field("Test", "test")
        assert self.item.has_field("Test")

    def test_set_field(self):
        self.item.set_field("Test", "test")
        assert self.item.get_field("Test") == "test"
