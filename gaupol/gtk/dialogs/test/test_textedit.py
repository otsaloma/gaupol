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

import gtk
import gaupol.gtk


class TestTextEditDialog(gaupol.gtk.TestCase):

    def run__dialog(self):

        self.dialog.run()
        self.dialog.destroy()

    def setup_method(self, method):

        gaupol.gtk.conf.editor.use_custom_font = True
        gaupol.gtk.conf.editor.custom_font = "sans"
        self.dialog = gaupol.gtk.TextEditDialog(gtk.Window())
        self.dialog.show()

    def test_get_text(self):

        self.dialog.set_text("test")
        text = self.dialog.get_text()
        assert text == "test"

    def test_set_text(self):

        self.dialog.set_text("test")
        text = self.dialog.get_text()
        assert text == "test"
