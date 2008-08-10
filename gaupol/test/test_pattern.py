# Copyright (C) 2007-2008 Osmo Salomaa
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

import gaupol
import re


class TestPattern(gaupol.TestCase):

    def assert_name_in_locale(self, code, modifier=None):

        get_code = gaupol.locales.get_system_code
        get_modifier = gaupol.locales.get_system_modifier
        gaupol.locales.get_system_code = lambda: code
        gaupol.locales.get_system_modifier = lambda: modifier
        self.pattern.set_field("Name", "system")
        key = (code if modifier is None else "%s@%s" % (code, modifier))
        self.pattern.set_field("Name[%s]" % key, "local")
        assert self.pattern.get_name() == "local"
        gaupol.locales.get_system_code = get_code
        gaupol.locales.get_system_modifier = get_modifier

    def setup_method(self, method):

        self.pattern = gaupol.Pattern()

    def test_get_description(self):

        self.pattern.set_field("Description", "test")
        assert self.pattern.get_description(False) == "test"
        assert self.pattern.get_description(True) == "test"

    def test_get_field(self):

        assert self.pattern.get_field("Xxxx") is None
        self.pattern.set_field("Test", "test")
        assert self.pattern.get_field("Test") == "test"

    def test_get_field_boolean(self):

        assert self.pattern.get_field("Xxxx") is None
        self.pattern.set_field("Test", "True")
        assert self.pattern.get_field_boolean("Test") is True
        self.pattern.set_field("Test", "False")
        assert self.pattern.get_field_boolean("Test") is False
        self.pattern.set_field("Test", "Xxxx")
        function = self.pattern.get_field_boolean
        self.raises(ValueError, function, "Test")

    def test_get_field_list(self):

        assert self.pattern.get_field("Xxxx") is None
        self.pattern.set_field("Test", "Yee,Haw")
        assert self.pattern.get_field_list("Test") == ["Yee", "Haw"]

    def test_get_flags(self):

        self.pattern.set_field("Flags", "DOTALL,UNICODE")
        flags = self.pattern.get_flags()
        assert flags == re.DOTALL | re.UNICODE

    def test_get_name(self):

        self.pattern.set_field("Name", "test")
        assert self.pattern.get_name(False) == "test"
        assert self.pattern.get_name(True) == "test"

    def test_get_name__localization(self):

        self.assert_name_in_locale("en_US", "Latn")
        self.assert_name_in_locale("en_US", None)
        self.assert_name_in_locale("en", "Latn")
        self.assert_name_in_locale("en", None)

    def test_get_name__no_locale(self):

        get_code = gaupol.locales.get_system_code
        gaupol.locales.get_system_code = lambda: None
        self.pattern.set_field("Name", "system")
        assert self.pattern.get_name() == "system"
        gaupol.locales.get_system_code = get_code

    def test_set_field(self):

        self.pattern.set_field("Test", "test")
        assert self.pattern.get_field("Test") == "test"
