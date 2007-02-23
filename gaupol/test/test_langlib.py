# Copyright (C) 2005-2006 Osmo Salomaa
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


from gettext import dgettext
from gettext import gettext as _

from gaupol.unittest import TestCase
from .. import langlib


class TestModule(TestCase):

    def test_get_country(self):

        country = langlib.get_country("af_ZA")
        assert country == dgettext("iso_3166", "South Africa")
        country = langlib.get_country("af")
        assert country is None

        try:
            langlib.get_country("xx_XX")
            raise AssertionError
        except KeyError:
            pass

    def test_get_language(self):

        lang = langlib.get_language("is_IS")
        assert lang == dgettext("iso_639", "Icelandic")
        lang = langlib.get_language("is")
        assert lang == dgettext("iso_639", "Icelandic")

        try:
            langlib.get_language("xx")
            raise AssertionError
        except KeyError:
            pass

    def test_get_long_name(self):

        name = langlib.get_long_name("mn_MN")
        lang = dgettext("iso_639", "Mongolian")
        country = dgettext("iso_3166", "Mongolia")
        assert name == _("%s (%s)") % (lang, country)

        name = langlib.get_long_name("mn")
        lang = dgettext("iso_639", "Mongolian")
        assert name == lang

        try:
            langlib.get_long_name("xx_XX")
            raise AssertionError
        except KeyError:
            pass
