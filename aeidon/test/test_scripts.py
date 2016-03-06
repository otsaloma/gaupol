# -*- coding: utf-8 -*-

# Copyright (C) 2007 Osmo Salomaa
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
        name = d_("iso_15924", "Arabic")
        assert aeidon.scripts.code_to_name("Arab") == name
        name = d_("iso_15924", "Latin")
        assert aeidon.scripts.code_to_name("Latn") == name

    def test_is_valid(self):
        assert aeidon.scripts.is_valid("Latn")
        assert not aeidon.scripts.is_valid("Xxxx")
