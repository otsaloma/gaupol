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


# For some reason the below code fails if the middle line is missing. As a
# result automatic testing cannot not cover enough. Test this shit manually,
# especially the addition of extension before overwrite confirmation.
#
#   dialog.set_filename(path)
#   dialog.run()
#   assert dialog.get_filename() == path


import gtk

from gaupol import enclib
from gaupol.gtk import cons
from gaupol.gtk.index import *
from gaupol.gtk.unittest import TestCase
from .. import file


class _TestFileDialog(TestCase):

    # pylint: disable-msg=E1101

    def run(self):

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

        # pylint: disable-msg=W0612
        for encoding, name in self.dialog._encodings:
            if enclib.is_valid(encoding):
                self.dialog.set_encoding(encoding)
                assert self.dialog.get_encoding() == encoding
        self.dialog.set_encoding("johab")
        assert self.dialog.get_encoding() == "johab"

    def test_set_encoding(self):

        # pylint: disable-msg=W0612
        for encoding, name in self.dialog._encodings:
            if enclib.is_valid(encoding):
                self.dialog.set_encoding(encoding)
                assert self.dialog.get_encoding() == encoding
        self.dialog.set_encoding("johab")
        assert self.dialog.get_encoding() == "johab"


class TestOpenDialogMain(_TestFileDialog):

    def setup_method(self, method):

        self.dialog = file.OpenDialog(cons.DOCUMENT.MAIN, "test", gtk.Window())


class TestOpenDialogTranslation(_TestFileDialog):

    def setup_method(self, method):

        self.dialog = file.OpenDialog(cons.DOCUMENT.TRAN, "test", gtk.Window())


class TestAppendDialog(_TestFileDialog):

    def setup_method(self, method):

        self.dialog = file.AppendDialog(gtk.Window())


class TestSaveDialog(_TestFileDialog):

    def setup_method(self, method):

        self.dialog = file.SaveDialog("test", gtk.Window())

    def test__on_format_combo_changed(self):

        for format in cons.FORMAT.members:
            self.dialog.set_format(format)

    def test__on_response(self):

        self.dialog.response(gtk.RESPONSE_OK)

    def test_get_format(self):

        for format in cons.FORMAT.members:
            self.dialog.set_format(format)
            assert self.dialog.get_format() == format

    def test_get_newline(self):

        for newline in cons.NEWLINE.members:
            self.dialog.set_newline(newline)
            assert self.dialog.get_newline() == newline

    def test_set_format(self):

        for format in cons.FORMAT.members:
            self.dialog.set_format(format)
            assert self.dialog.get_format() == format

    def test_set_newline(self):

        for newline in cons.NEWLINE.members:
            self.dialog.set_newline(newline)
            assert self.dialog.get_newline() == newline

    def test_set_name(self):

        self.dialog.set_name("test")
        self.dialog.set_name(self.get_subrip_path())


class TestVideoDialog(TestCase):

    def run(self):

        self.dialog.run()
        self.dialog.destroy()

    def setup_method(self, method):

        self.dialog = file.VideoDialog(gtk.Window())

    def test___init__(self):

        pass
