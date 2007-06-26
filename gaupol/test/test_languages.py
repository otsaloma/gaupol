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


import gaupol
_ = gaupol.i18n._
dgettext = gaupol.i18n.dgettext

from gaupol import unittest
from .. import languages


class TestModule(unittest.TestCase):

    def test_get_country(self):

        country = languages.get_country("af_ZA")
        assert country == dgettext("iso_3166", "South Africa")
        country = languages.get_country("af")
        assert country is None

    def test_get_language(self):

        lang = languages.get_language("is_IS")
        assert lang == dgettext("iso_639", "Icelandic")
        lang = languages.get_language("is")
        assert lang == dgettext("iso_639", "Icelandic")

    def test_get_long_name(self):

        name = languages.get_long_name("mn_MN")
        lang = dgettext("iso_639", "Mongolian")
        country = dgettext("iso_3166", "Mongolia")
        assert name == _("%s (%s)") % (lang, country)

        name = languages.get_long_name("mn")
        lang = dgettext("iso_639", "Mongolian")
        assert name == lang
