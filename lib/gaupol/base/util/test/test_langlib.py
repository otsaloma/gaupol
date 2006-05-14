# Copyright (C) 2005-2006 Osmo Salomaa
#
# This file is part of Gaupol.
#
# Gaupol is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Gaupol is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Gaupol; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA


from gaupol.base.util import langlib
from gaupol.test      import Test


class TestModule(Test):

    def test_get_country(self):

        country = langlib.get_country('af_ZA')
        assert isinstance(country, basestring)

        country = langlib.get_country('af')
        assert country is None

        try:
            langlib.get_country('xx_XX')
            raise AssertionError
        except KeyError:
            pass

    def test_get_descriptive_name(self):

        name = langlib.get_descriptive_name('af_ZA')
        assert isinstance(name, basestring)

        name = langlib.get_descriptive_name('af')
        assert isinstance(name, basestring)

        try:
            langlib.get_descriptive_name('xx')
            raise AssertionError
        except KeyError:
            pass

    def test_get_language(self):

        lang = langlib.get_language('af_ZA')
        assert isinstance(lang, basestring)

        try:
            langlib.get_language('xx')
            raise AssertionError
        except KeyError:
            pass
