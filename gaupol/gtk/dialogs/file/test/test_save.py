# Copyright (C) 2005-2007 Osmo Salomaa
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


import gaupol.gtk
import gtk

from .test_subtitle import _TestSubtitleFileDialog
from .. import save


class TestSaveDialog(_TestSubtitleFileDialog):

    def setup_method(self, method):

        self.dialog = save.SaveDialog(gtk.Window(), "test")

    def test__on_format_combo_changed(self):

        for format in gaupol.gtk.FORMAT.members:
            self.dialog.set_format(format)

    def test__on_response(self):

        self.dialog.response(gtk.RESPONSE_OK)

    def test_get_format(self):

        for format in gaupol.gtk.FORMAT.members:
            self.dialog.set_format(format)
            value = self.dialog.get_format()
            assert value == format

    def test_get_newline(self):

        for newline in gaupol.gtk.NEWLINE.members:
            self.dialog.set_newline(newline)
            value = self.dialog.get_newline()
            assert value == newline

    def test_set_format(self):

        for format in gaupol.gtk.FORMAT.members:
            self.dialog.set_format(format)
            value = self.dialog.get_format()
            assert value == format

    def test_set_newline(self):

        for newline in gaupol.gtk.NEWLINE.members:
            self.dialog.set_newline(newline)
            value = self.dialog.get_newline()
            assert value == newline

    def test_set_name(self):

        self.dialog.set_name("test")
        self.dialog.set_name(self.get_subrip_path())
