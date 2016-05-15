# -*- coding: utf-8 -*-

# Copyright (C) 2005 Osmo Salomaa
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
import imp

from aeidon.i18n   import _, d_
from unittest.mock import patch


class TestModule(aeidon.TestCase):

    def test_code_to_country(self):
        country = d_("iso_3166", "South Africa")
        assert aeidon.locales.code_to_country("af_ZA") == country
        assert aeidon.locales.code_to_country("af") is None

    def test_code_to_language(self):
        language = d_("iso_639", "Icelandic")
        assert aeidon.locales.code_to_language("is_IS") == language
        assert aeidon.locales.code_to_language("is") == language

    def test_code_to_name(self):
        language = d_("iso_639", "Mongolian")
        country = d_("iso_3166", "Mongolia")
        name = _("{language} ({country})").format(**locals())
        assert aeidon.locales.code_to_name("mn_MN") == name
        assert aeidon.locales.code_to_name("mn") == language

    def test_get_system_code(self):
        assert aeidon.locales.get_system_code()

    @patch.dict("os.environ", dict(LANGUAGE="sr@Latn"))
    def test_get_system_modifier__latn(self):
        imp.reload(aeidon.locales)
        assert aeidon.locales.get_system_modifier() == "Latn"

    @patch.dict("os.environ", dict(LANGUAGE="en"))
    def test_get_system_modifier__none(self):
        imp.reload(aeidon.locales)
        assert aeidon.locales.get_system_modifier() is None
