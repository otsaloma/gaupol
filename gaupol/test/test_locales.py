# Copyright (C) 2005-2008 Osmo Salomaa
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
import os


class TestModule(gaupol.TestCase):

    def test_code_to_country(self):

        country = gaupol.i18n.dgettext("iso_3166", "South Africa")
        assert gaupol.locales.code_to_country("af_ZA") == country
        assert gaupol.locales.code_to_country("af") is None
        self.raises(KeyError, gaupol.locales.code_to_country, "xx_XX")

    def test_code_to_language(self):

        language = gaupol.i18n.dgettext("iso_639", "Icelandic")
        assert gaupol.locales.code_to_language("is_IS") == language
        assert gaupol.locales.code_to_language("is") == language
        self.raises(KeyError, gaupol.locales.code_to_language, "xx_XX")
        self.raises(KeyError, gaupol.locales.code_to_language, "xx")

    def test_code_to_name(self):

        language = gaupol.i18n.dgettext("iso_639", "Mongolian")
        country = gaupol.i18n.dgettext("iso_3166", "Mongolia")
        name = gaupol.i18n._("%(language)s (%(country)s)") % locals()
        assert gaupol.locales.code_to_name("mn_MN") == name
        assert gaupol.locales.code_to_name("mn") == language
        self.raises(KeyError, gaupol.locales.code_to_name, "xx_XX")
        self.raises(KeyError, gaupol.locales.code_to_name, "xx")

    def test_get_all(self):

        assert gaupol.locales.get_all()
        for locale in gaupol.locales.get_all():
            gaupol.locales.code_to_country(locale)
            gaupol.locales.code_to_language(locale)

    def test_get_system_code(self):

        gaupol.locales.get_system_code()

    def test_get_system_modifier(self):

        environment = os.environ.copy()
        os.environ.clear()
        reload(gaupol.locales)
        assert gaupol.locales.get_system_modifier() is None
        os.environ["LANGUAGE"] = "sr@Latn"
        reload(gaupol.locales)
        assert gaupol.locales.get_system_modifier() == "Latn"
        os.environ = environment
