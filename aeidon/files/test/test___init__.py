# -*- coding: utf-8-unix -*-

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

    def test_add(self):
        aeidon.files.add(aeidon.files.SubRip)

    def test_new(self):
        format = aeidon.formats.SUBRIP
        file = aeidon.files.new(format, "", "ascii")
        assert isinstance(file, aeidon.files.SubRip)

    def test_new__value_error(self):
        self.assert_raises(ValueError,
                           aeidon.files.new,
                           None, "", "ascii")
