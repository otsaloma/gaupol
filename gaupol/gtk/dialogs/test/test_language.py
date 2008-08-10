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

import gaupol.gtk
import gtk


class TestLanguageDialog(gaupol.gtk.TestCase):

    def run__dialog(self):

        self.dialog.run()
        self.dialog.destroy()

    def setup_method(self, method):

        self.dialog = gaupol.gtk.LanguageDialog(gtk.Window())
        self.dialog.show()

    def test__on_tree_view_selection_changed(self):

        store = self.dialog._tree_view.get_model()
        selection = self.dialog._tree_view.get_selection()
        store = self.dialog._tree_view.get_model()
        for i in range(len(store)):
            selection.select_path(i)

    def test__init_signal_handlers__field(self):

        self.dialog._main_radio.set_active(True)
        self.dialog._tran_radio.set_active(True)
        self.dialog._main_radio.set_active(True)

    def test__init_signal_handlers__target(self):

        self.dialog._current_radio.set_active(True)
        self.dialog._all_radio.set_active(True)
        self.dialog._current_radio.set_active(True)
