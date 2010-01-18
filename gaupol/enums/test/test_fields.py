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


class TestModule(gaupol.TestCase):

    def test_attributes(self):
        for field in gaupol.fields:
            assert hasattr(field, "is_position")
            assert hasattr(field, "is_text")
            assert hasattr(field, "label")

    def test_items(self):
        assert hasattr(gaupol.fields, "NUMBER")
        assert hasattr(gaupol.fields, "START")
        assert hasattr(gaupol.fields, "END")
        assert hasattr(gaupol.fields, "DURATION")
        assert hasattr(gaupol.fields, "MAIN_TEXT")
        assert hasattr(gaupol.fields, "TRAN_TEXT")
