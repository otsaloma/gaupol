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

from gaupol.gtk.dialog.encoding import EncodingDialog, AdvancedEncodingDialog
from gaupol.test                import Test


class TestEncodingDialog(Test):

    def setup_method(self, method):

        self.dialog = EncodingDialog(gtk.Window())

    def test_get_selection(self):

        selection = self.dialog._tree_view.get_selection()
        selection.unselect_all()
        encoding = self.dialog.get_encoding()
        assert encoding is None

        selection.select_path(0)
        encoding = self.dialog.get_encoding()
        assert isinstance(encoding, basestring)

    def test_run(self):

        self.dialog.run()
        self.dialog.destroy()


class TestAdvancedEncodingDialog(TestEncodingDialog):

    def setup_method(self, method):

        self.dialog = AdvancedEncodingDialog(gtk.Window())

    def test_get_visible_encodings(self):

        store = self.dialog._tree_view.get_model()
        for row in range(len(store)):
            store[row][2] = False
        visible = self.dialog.get_visible_encodings()
        assert visible == []

        store[1][2] = True
        store[3][2] = True
        visible = self.dialog.get_visible_encodings()
        assert len(visible) == 2
        assert isinstance(visible[0], basestring)
        assert isinstance(visible[1], basestring)
