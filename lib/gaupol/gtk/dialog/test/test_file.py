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


import os

import gtk

from gaupol.base.util       import enclib
from gaupol.gtk             import cons
from gaupol.gtk.dialog.file import OpenFileDialog
from gaupol.gtk.dialog.file import OpenVideoDialog
from gaupol.gtk.dialog.file import SaveFileDialog
from gaupol.gtk.dialog.file import _OverwriteQuestionDialog
from gaupol.gtk.dialog.file import _TextFileDialog
from gaupol.gtk.util        import gtklib
from gaupol.test            import Test


class TestOverwriteQuestionDialog(Test):

    def test_run(self):

        gtklib.run(_OverwriteQuestionDialog(gtk.Window(), 'test'))


class _TestTextFileDialog(Test):

    def test_get_and_set_encoding(self):

        for entry in self.dialog._encodings:
            if enclib.is_valid(entry[0]):
                self.dialog.set_encoding(entry[0])
                encoding = self.dialog.get_encoding()
                assert encoding == entry[0]

        self.dialog.set_encoding('johab')
        encoding = self.dialog.get_encoding()
        assert encoding == 'johab'

    def test_on_encoding_combo_changed(self):

        model = self.dialog._encoding_combo.get_model()
        self.dialog._encoding_combo.set_active(len(model) - 1)

    def test_run(self):

        gtklib.run(self.dialog)


class TestOpenFileDialog(_TestTextFileDialog):

    def setup_method(self, method):

        self.dialog = OpenFileDialog('test', True, gtk.Window())

    def test_set_open_button(self):

        self.dialog.set_open_button(gtk.STOCK_SELECT_COLOR, 'Test')


class TestSaveFileDialog(_TestTextFileDialog):

    def setup_method(self, method):

        self.dialog = SaveFileDialog('test', gtk.Window())

    def test_confirm_overwrite(self):

        self.dialog.set_current_name('test')
        confirm = self.dialog._confirm_overwrite()
        assert confirm == gtk.FILE_CHOOSER_CONFIRMATION_ACCEPT_FILENAME

        self.dialog.set_format(cons.Format.SUBRIP)
        path = self.get_subrip_path()
        self.dialog.set_filename(path)
        self.dialog.set_current_name(os.path.basename(path))
        confirm = self.dialog._confirm_overwrite()
        assert confirm in (
            gtk.FILE_CHOOSER_CONFIRMATION_ACCEPT_FILENAME,
            gtk.FILE_CHOOSER_CONFIRMATION_SELECT_AGAIN
        )

    def test_get_full_filename(self):

        self.dialog.set_current_name('test')
        self.dialog.set_format(cons.Format.SUBRIP)
        name = self.dialog.get_full_filename()
        assert name.endswith('test.srt')

    def test_get_and_set_format(self):

        self.dialog.set_current_name('test')
        self.dialog.set_format(cons.Format.SUBRIP)

        for i, extension in enumerate(cons.Format.extensions):
            self.dialog.set_format(i)
            name = self.dialog.get_filename()
            assert name.endswith('test' + extension)
            format = self.dialog.get_format()
            assert format == i

    def test_get_and_set_newlines(self):

        self.dialog.set_current_name('test')
        self.dialog.set_newlines(cons.Newlines.UNIX)

        for i in range(len(cons.Newlines.values)):
            self.dialog.set_newlines(i)
            newlines = self.dialog.get_newlines()
            assert newlines == i

    def test_set_name(self):

        path = self.get_subrip_path()
        self.dialog.set_name(path)
        self.dialog.set_name('test')


class TestOpenVideoDialog(Test):

    def test_run(self):

        gtklib.run(OpenVideoDialog(gtk.Window()))
