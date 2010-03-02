# Copyright (C) 2005-2008,2010 Osmo Salomaa
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
import gtk


class _TestFileDialog(gaupol.TestCase):

    # pylint: disable-msg=E1101

    def run__dialog(self):
        self.dialog.run()
        self.dialog.destroy()

    def test__on_encoding_combo_changed(self):
        responder = iter((gtk.RESPONSE_OK, gtk.RESPONSE_CANCEL))
        def run_dialog(dialog):
            selection = dialog._tree_view.get_selection()
            selection.select_path(0)
            return responder.next()
        self.dialog.run_dialog = run_dialog
        store = self.dialog._encoding_combo.get_model()
        self.dialog._encoding_combo.set_active(len(store) - 1)
        self.dialog._encoding_combo.set_active(len(store) - 1)

    def test_get_encoding(self):
        encoding = gaupol.conf.encoding.visible[0]
        self.dialog.set_encoding(encoding)
        assert self.dialog.get_encoding() == encoding
        self.dialog.set_encoding("johab")
        assert self.dialog.get_encoding() == "johab"

    def test_set_encoding(self):
        encoding = gaupol.conf.encoding.visible[0]
        self.dialog.set_encoding(encoding)
        assert self.dialog.get_encoding() == encoding
        self.dialog.set_encoding("johab")
        assert self.dialog.get_encoding() == "johab"
