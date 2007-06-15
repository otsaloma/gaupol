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


import functools
import gaupol.gtk
import gtk

from gaupol.gtk import unittest
from .. import header


class TestHeaderDialog(unittest.TestCase):

    # pylint: disable-msg=W0201

    def run__both(self):

        self.dialog.run()
        self.dialog.destroy()

    def run__main(self):

        page = self.application.get_current_page()
        path = self.get_file_path(gaupol.gtk.FORMAT.SUBRIP)
        self.application.open_translation_file(path, "ascii")
        parent = self.application.window
        self.dialog = header.HeaderDialog(parent, self.application)
        self.dialog.run()
        self.dialog.destroy()

    def run__translation(self):

        page = self.application.get_current_page()
        path = self.get_file_path(gaupol.gtk.FORMAT.SUBRIP)
        self.application.open_main_file(path, "ascii")
        path = self.get_file_path(gaupol.gtk.FORMAT.SUBVIEWER2)
        self.application.open_translation_file(path, "ascii")
        parent = self.application.window
        self.dialog = header.HeaderDialog(parent, self.application)
        self.dialog.run()
        self.dialog.destroy()

    def run__show_mpsub_error_dialog(self):

        flash_dialog = gaupol.gtk.Runner.flash_dialog
        flash_dialog = functools.partial(flash_dialog, self.application)
        self.dialog.flash_dialog = flash_dialog
        self.dialog._show_mpsub_error_dialog()

    def setup_method(self, method):

        self.application = self.get_application()
        page = self.application.get_current_page()
        path = self.get_file_path(gaupol.gtk.FORMAT.SUBVIEWER2)
        self.application.open_main_file(path, "ascii")
        path = self.get_file_path(gaupol.gtk.FORMAT.MPSUB)
        self.application.open_translation_file(path, "ascii")
        parent = self.application.window
        self.dialog = header.HeaderDialog(parent, self.application)
        respond = lambda *args: gtk.RESPONSE_DELETE_EVENT
        self.dialog.flash_dialog = respond
        self.dialog.run_dialog = respond

    def test__get_main_header(self):

        self.dialog._set_main_header("test")
        value = self.dialog._get_main_header()
        assert value == "test"

    def test__get_translation_header(self):

        self.dialog._set_translation_header("test")
        value = self.dialog._get_translation_header()
        assert value == "test"

    def test__on_copy_down_button_clicked(self):

        self.dialog._on_copy_down_button_clicked()
        value = self.dialog._get_translation_header()
        assert value == self.dialog._main_file.header

    def test__on_copy_up_button_clicked(self):

        self.dialog._on_copy_up_button_clicked()
        value = self.dialog._get_main_header()
        assert value == self.dialog._tran_file.header

    def test__on_main_clear_button_clicked(self):

        self.dialog._on_main_clear_button_clicked()
        value = self.dialog._get_main_header()
        assert value == ""

    def test__on_main_template_button_clicked(self):

        self.dialog._on_main_template_button_clicked()
        value = self.dialog._get_main_header()
        assert value == self.dialog._main_file.get_template_header()

    def test__on_main_revert_button_clicked(self):

        self.dialog._on_main_clear_button_clicked()
        self.dialog._on_main_revert_button_clicked()
        value = self.dialog._get_main_header()
        assert value == self.dialog._main_file.header

    def test__on_response(self):

        self.dialog.response(gtk.RESPONSE_OK)

    def test__on_tran_clear_button_clicked(self):

        self.dialog._on_tran_clear_button_clicked()
        value = self.dialog._get_translation_header()
        assert value == ""

    def test__on_tran_template_button_clicked(self):

        self.dialog._on_tran_template_button_clicked()
        value = self.dialog._get_translation_header()
        assert value == self.dialog._tran_file.get_template_header()

    def test__on_tran_revert_button_clicked(self):

        self.dialog._on_tran_clear_button_clicked()
        self.dialog._on_tran_revert_button_clicked()
        value = self.dialog._get_translation_header()
        assert value == self.dialog._tran_file.header

    def test__set_main_header(self):

        self.dialog._set_main_header("test")
        value = self.dialog._get_main_header()
        assert value == "test"

    def test__set_translation_header(self):

        self.dialog._set_translation_header("test")
        value = self.dialog._get_translation_header()
        assert value == "test"

    def test__show_mpsub_error_dialog(self):

        self.dialog._show_mpsub_error_dialog()
