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

from gaupol.base.file.classes import *
from gaupol.gtk               import cons
from gaupol.gtk.dialog.header import HeaderDialog
from gaupol.gtk.dialog.header import _MPsubErrorDialog
from gaupol.gtk.util          import gtklib
from gaupol.test              import Test


class TestMPsubErrorDialog(Test):

    def test_run(self):

        gtklib.run(_MPsubErrorDialog(gtk.Window()))


class TestHeaderDialog(Test):

    def setup_method(self, method):

        self.project = self.get_project()

        self.project.save_main_file((
            self.project.main_file.path,
            cons.Format.SUBVIEWER2,
            'utf_8',
            self.project.main_file.newlines
        ))
        self.project.save_translation_file((
            self.project.tran_file.path,
            cons.Format.ASS,
            'utf_8',
            self.project.tran_file.newlines
        ))

        self.dialog = HeaderDialog(gtk.Window(), self.project)
        self.main_header = self.project.main_file.header
        self.tran_header = self.project.tran_file.header
        self.main_temp = self.project.main_file.get_template_header()
        self.tran_temp = self.project.tran_file.get_template_header()

    def test_on_copy_down_button_clicked(self):

        self.dialog._copy_down_button.emit('clicked')
        tran_header = self.dialog._get_translation_header()
        assert tran_header == self.main_header

    def test_on_copy_up_button_clicked(self):

        self.dialog._copy_up_button.emit('clicked')
        main_header = self.dialog._get_main_header()
        assert main_header == self.tran_header

    def test_on_main_clear_button_clicked(self):

        self.dialog._main_clear_button.emit('clicked')
        main_header = self.dialog._get_main_header()
        assert main_header == ''

    def test_on_main_temp_button_clicked(self):

        self.dialog._main_temp_button.emit('clicked')
        main_header = self.dialog._get_main_header()
        assert main_header == self.main_temp

    def test_on_main_revert_button_clicked(self):

        self.dialog._main_clear_button.emit('clicked')
        self.dialog._main_revert_button.emit('clicked')
        main_header = self.dialog._get_main_header()
        assert main_header == self.main_header

    def test_on_tran_clear_button_clicked(self):

        self.dialog._tran_clear_button.emit('clicked')
        tran_header = self.dialog._get_translation_header()
        assert tran_header == ''

    def test_on_tran_temp_button_clicked(self):

        self.dialog._tran_temp_button.emit('clicked')
        tran_header = self.dialog._get_translation_header()
        assert tran_header == self.tran_temp

    def test_on_tran_revert_button_clicked(self):

        self.dialog._tran_clear_button.emit('clicked')
        self.dialog._tran_revert_button.emit('clicked')
        tran_header = self.dialog._get_translation_header()
        assert tran_header == self.tran_header

    def test_get_and_set_main_header(self):

        self.dialog._set_main_header('test')
        main_header = self.dialog._get_main_header()
        assert main_header == 'test'

    def test_get_and_set_translation_header(self):

        self.dialog._set_translation_header('test')
        tran_header = self.dialog._get_translation_header()
        assert tran_header == 'test'

    def test_run(self):

        gtklib.run(self.dialog)
