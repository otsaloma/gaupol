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


import gtk

from gaupol import enclib
from gaupol.gtk.unittest import TestCase
from .. import encoding


class TestEncodingDialog(TestCase):

    def run(self):

        self.dialog.run()
        self.dialog.destroy()

    def setup_method(self, method):

        self.dialog = encoding.EncodingDialog(gtk.Window())

    def test_get_encoding(self):

        store = self.dialog._tree_view.get_model()
        selection = self.dialog._tree_view.get_selection()
        selection.unselect_all()
        name = self.dialog.get_encoding()
        assert name is None
        for i in range(len(store)):
            selection.select_path(i)
            name = self.dialog.get_encoding()
            assert enclib.is_valid(name)


class TestAdvEncodingDialog(TestEncodingDialog):

    def setup_method(self, method):

        self.dialog = encoding.AdvEncodingDialog(gtk.Window())

    def test_get_visible_encodings(self):

        store = self.dialog._tree_view.get_model()
        for i in range(len(store)):
            store[i][2] = False
        assert not self.dialog.get_visible_encodings()

        for i in range(len(store)):
            store[i][2] = True
        visibles = self.dialog.get_visible_encodings()
        assert visibles
        for name in visibles:
            assert enclib.is_valid(name)
