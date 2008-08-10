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
import os

from .test_file import _TestFileDialog


class TestSaveDialog(_TestFileDialog):

    def setup_method(self, method):

        gaupol.gtk.conf.file.directory = os.getcwd()
        self.dialog = gaupol.gtk.SaveDialog(gtk.Window(), "test")
        self.dialog.show()

    def test__on_format_combo_changed(self):

        path = self.get_subrip_path()
        self.dialog.set_filename(path)
        gaupol.gtk.util.iterate_main()
        for format in gaupol.formats:
            self.dialog.set_format(format)

    def test__on_response(self):

        self.dialog.response(gtk.RESPONSE_CANCEL)

    def test_get_format(self):

        for format in gaupol.formats:
            self.dialog.set_format(format)
            value = self.dialog.get_format()
            assert value == format

    def test_get_newline(self):

        for newline in gaupol.newlines:
            self.dialog.set_newline(newline)
            value = self.dialog.get_newline()
            assert value == newline

    def test_set_format(self):

        for format in gaupol.formats:
            self.dialog.set_format(format)
            value = self.dialog.get_format()
            assert value == format

    def test_set_newline(self):

        for newline in gaupol.newlines:
            self.dialog.set_newline(newline)
            value = self.dialog.get_newline()
            assert value == newline

    def test_set_name(self):

        self.dialog.set_name("test")
        self.dialog.set_name(self.get_subrip_path())
