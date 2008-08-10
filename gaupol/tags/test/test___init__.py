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

    def test_add_class(self):

        gaupol.tags.add_class(gaupol.tags.SubRip)

    def test_new(self):

        file = gaupol.tags.new(gaupol.formats.SUBRIP)
        assert isinstance(file, gaupol.tags.SubRip)

    def test_new__value_error(self):

        self.raises(ValueError, gaupol.tags.new, None)
