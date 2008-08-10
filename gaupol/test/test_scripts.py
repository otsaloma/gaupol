# Copyright (C) 2007-2008 Osmo Salomaa
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


class TestModule(gaupol.TestCase):

    def test_code_to_name(self):

        name = gaupol.i18n.dgettext("iso_15924", "Arabic")
        assert gaupol.scripts.code_to_name("Arab") == name
        name = gaupol.i18n.dgettext("iso_15924", "Latin")
        assert gaupol.scripts.code_to_name("Latn") == name

    def test_is_valid(self):

        assert gaupol.scripts.is_valid("Latn")
        assert not gaupol.scripts.is_valid("Xxxx")
