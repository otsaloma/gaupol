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

from gaupol.gtk                    import cons
from gaupol.gtk.dialog.filechooser import OverwriteQuestionDialog
from gaupol.gtk.dialog.filechooser import TextFileChooserDialog
from gaupol.gtk.dialog.filechooser import OpenFileDialog
from gaupol.gtk.dialog.filechooser import SaveFileDialog
from gaupol.gtk.dialog.filechooser import OpenVideoDialog
from gaupol.test                   import Test


class TestOverwriteQuestionDialog(Test):

    def test_init(self):

        OverwriteQuestionDialog(gtk.Window(), 'test')


class _TestTextFileChooserDialog(Test):

    def test_get_and_set_encoding(self):

        for entry in self.dialog._encodings:
            self.dialog.set_encoding(entry[0])
            encoding = self.dialog.get_encoding()
            assert encoding == entry[0]

    def test_on_current_folder_changed(self):

        self.dialog.set_current_folder(os.getcwd())

    def test_on_encoding_combo_changed(self):

        model = self.dialog._encoding_combo.get_model()
        self.dialog._encoding_combo.set_active(len(model) - 1)


class TestOpenFileDialog(_TestTextFileChooserDialog):

    def setup_method(self, method):

        self.dialog = OpenFileDialog('test', gtk.Window())

class TestSaveFileDialog(_TestTextFileChooserDialog):

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

    def test_get_filename_with_extension(self):

        self.dialog.set_current_name('test')
        self.dialog.set_format(cons.Format.SUBRIP)
        name = self.dialog.get_filename_with_extension()
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

    def test_set_filename_or_current_name(self):

        path = self.get_subrip_path()
        self.dialog.set_filename_or_current_name(path)
        self.dialog.set_filename_or_current_name('test')


class TestOpenVideoDialog(Test):

    def test_init(self):

        OpenVideoDialog(gtk.Window())
