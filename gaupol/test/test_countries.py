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
from .. import countries


class TestModule(unittest.TestCase):

    def test__init_countries(self):

        assert countries.countries

    def test_code_to_name(self):

        name = gaupol.i18n.dgettext("iso_3166", "Ireland")
        assert countries.code_to_name("IE") == name
        name = gaupol.i18n.dgettext("iso_3166", "Yemen")
        assert countries.code_to_name("YE") == name
