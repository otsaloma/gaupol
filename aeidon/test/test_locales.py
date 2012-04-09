# -*- coding: utf-8-unix -*-

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
import imp
import os


class TestModule(aeidon.TestCase):

    def test_code_to_country(self):
        country = aeidon.i18n.dgettext("iso_3166", "South Africa")
        assert aeidon.locales.code_to_country("af_ZA") == country
        assert aeidon.locales.code_to_country("af") is None

    def test_code_to_country__key_error(self):
        self.assert_raises(KeyError,
                           aeidon.locales.code_to_country,
                           "xx_XX")

    def test_code_to_language(self):
        language = aeidon.i18n.dgettext("iso_639", "Icelandic")
        assert aeidon.locales.code_to_language("is_IS") == language
        assert aeidon.locales.code_to_language("is") == language

    def test_code_to_language__key_error(self):
        self.assert_raises(KeyError,
                           aeidon.locales.code_to_language,
                           "xx_XX")

    def test_code_to_name(self):
        language = aeidon.i18n.dgettext("iso_639", "Mongolian")
        country = aeidon.i18n.dgettext("iso_3166", "Mongolia")
        name = aeidon.i18n._("{language} ({country})").format(**locals())
        assert aeidon.locales.code_to_name("mn_MN") == name
        assert aeidon.locales.code_to_name("mn") == language

    def test_code_to_name__key_error(self):
        self.assert_raises(KeyError,
                           aeidon.locales.code_to_name,
                           "xx_XX")

    def test_get_system_code(self):
        assert aeidon.locales.get_system_code()

    @aeidon.deco.monkey_patch(os, "environ")
    def test_get_system_modifier__latn(self):
        os.environ["LANGUAGE"] = "sr@Latn"
        imp.reload(aeidon.locales)
        assert aeidon.locales.get_system_modifier() == "Latn"

    @aeidon.deco.monkey_patch(os, "environ")
    def test_get_system_modifier__none(self):
        os.environ["LANGUAGE"] = "en"
        imp.reload(aeidon.locales)
        assert aeidon.locales.get_system_modifier() is None
