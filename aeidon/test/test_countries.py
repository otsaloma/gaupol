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

from aeidon.i18n import d_


class TestModule(aeidon.TestCase):

    def test_code_to_name(self):
        name = d_("iso_3166", "Ireland")
        assert aeidon.countries.code_to_name("IE") == name
        name = d_("iso_3166", "Yemen")
        assert aeidon.countries.code_to_name("YE") == name

    def test_is_valid(self):
        assert aeidon.countries.is_valid("RU")
        assert not aeidon.countries.is_valid("XX")
