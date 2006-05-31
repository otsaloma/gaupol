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


from gaupol.base.util import listlib
from gaupol.test      import Test


class TestModule(Test):

    def test_remove_duplicates(self):

        lst = [4, 1, 5, 5, 1, 3, 6, 4, 4]
        lst = listlib.remove_duplicates(lst)
        assert lst == [4, 1, 5, 3, 6]

    def test_sort_and_remove_duplicates(self):

        lst = [4, 1, 5, 5, 1, 3, 6, 4, 4]
        lst = listlib.sort_and_remove_duplicates(lst)
        assert lst == [1, 3, 4, 5, 6]
