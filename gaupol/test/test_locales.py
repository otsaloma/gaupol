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


import gaupol
from gaupol import unittest
from .. import locales


class TestModule(unittest.TestCase):

    def test__init_locales(self):

        assert locales.locales

    def test_code_to_country(self):

        country = gaupol.i18n.dgettext("iso_3166", "South Africa")
        assert locales.code_to_country("af_ZA") == country
        assert locales.code_to_country("af") is None

    def test_code_to_language(self):

        language = gaupol.i18n.dgettext("iso_639", "Icelandic")
        assert locales.code_to_language("is_IS") == language
        assert locales.code_to_language("is") == language

    def test_code_to_name(self):

        language = gaupol.i18n.dgettext("iso_639", "Mongolian")
        country = gaupol.i18n.dgettext("iso_3166", "Mongolia")
        name = gaupol.i18n._("%(language)s (%(country)s)") % locals()
        assert locales.code_to_name("mn_MN") == name
        assert locales.code_to_name("mn") == language
