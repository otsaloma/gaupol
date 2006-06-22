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


from gaupol.gtk      import cons
from gaupol.gtk.view import View
from gaupol.test     import Test


class TestView(Test):

    def setup_method(self, method):

        self.view = View(cons.Mode.FRAME)
        store = self.view.get_model()
        store.append([1, 2, 3, 1, 'test', 'test'])
        store.append([2, 6, 7, 1, 'test', 'test'])
        store.append([3, 8, 9, 1, 'test', 'test'])

    def test_get_and_set_focus(self):

        self.view.set_focus(1, 3)
        row, col = self.view.get_focus()
        assert row == 1
        assert col == 3

    def test_get_and_set_selected_rows(self):

        self.view.select_rows([])
        rows = self.view.get_selected_rows()
        assert rows == []

        self.view.select_rows([0, 1, 2])
        rows = self.view.get_selected_rows()
        assert rows == [0, 1, 2]

    def test_scroll_to_row(self):

        self.view.scroll_to_row(2)
