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
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import aeidon

from unittest.mock import patch


class TestMetadataItem(aeidon.TestCase):

    def assert_name_in_locale(self, code, modifier):
        with patch("aeidon.locales.get_system_code", lambda: code):
            with patch("aeidon.locales.get_system_modifier", lambda: modifier):
                self.item.set_field("Name", "system")
                key = "{}@{}".format(code, modifier) if modifier else code
                self.item.set_field("Name[{}]".format(key), "local")
                assert self.item.get_name(localize=True) == "local"

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

    def test_get_name__localize(self):
        self.assert_name_in_locale("en_US", "Latn")
        self.assert_name_in_locale("en_US", None)
        self.assert_name_in_locale("en", "Latn")
        self.assert_name_in_locale("en", None)

    @patch("aeidon.locales.get_system_code", lambda: None)
    def test_get_name__no_locale(self):
        self.item.set_field("Name", "system")
        assert self.item.get_name() == "system"

    def test_has_field(self):
        assert not self.item.has_field("Test")
        self.item.set_field("Test", "test")
        assert self.item.has_field("Test")

    def test_set_field(self):
        self.item.set_field("Test", "test")
        assert self.item.get_field("Test") == "test"
