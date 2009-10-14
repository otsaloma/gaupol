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


class TestModule(aeidon.TestCase):

    def test_code_to_name(self):
        name = aeidon.i18n.dgettext("iso_639", "Nauru")
        assert aeidon.languages.code_to_name("na") == name
        name = aeidon.i18n.dgettext("iso_639", "Sindhi")
        assert aeidon.languages.code_to_name("sd") == name

    def test_code_to_name__key_error(self):
        self.raises(KeyError, aeidon.languages.code_to_name, "xx")

    def test_is_valid(self):
        assert aeidon.languages.is_valid("sv")
        assert not aeidon.languages.is_valid("xx")
