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


import gtk

from gaupol.gtk import const
from gaupol.gtk.unittest import TestCase
from .. import header


class TestHeaderDialog(TestCase):

    # pylint: disable-msg=W0201

    def run_both(self):

        self.dialog.run()
        self.dialog.destroy()

    def run_main(self):

        page = self.application.get_current_page()
        page.project.save(const.DOCUMENT.TRAN, (
            page.project.main_file.path,
            const.FORMAT.SUBRIP,
            "ascii",
            page.project.main_file.newline))
        self.dialog = header.HeaderDialog(
            self.application.window, self.application)
        self.dialog.run()
        self.dialog.destroy()

    def run_translation(self):

        page = self.application.get_current_page()
        page.project.save(const.DOCUMENT.MAIN, (
            page.project.main_file.path,
            const.FORMAT.SUBRIP,
            "ascii",
            page.project.main_file.newline))
        self.dialog = header.HeaderDialog(
            self.application.window, self.application)
        self.dialog.run()
        self.dialog.destroy()

    def setup_method(self, method):

        # pylint: disable-msg=E1101
        self.application = self.get_application()
        page = self.application.get_current_page()
        page.project.save(const.DOCUMENT.MAIN, (
            page.project.main_file.path,
            const.FORMAT.SUBVIEWER2,
            "ascii",
            page.project.main_file.newline))
        page.project.save(const.DOCUMENT.TRAN, (
            page.project.tran_file.path,
            const.FORMAT.ASS,
            "ascii",
            page.project.tran_file.newline))
        self.dialog = header.HeaderDialog(
            self.application.window, self.application)

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

    def test__on_main_temp_button_clicked(self):

        self.dialog._on_main_temp_button_clicked()
        value = self.dialog._get_main_header()
        assert value == self.dialog._main_file.get_template_header()

    def test__on_main_revert_button_clicked(self):

        self.dialog._on_main_clear_button_clicked()
        self.dialog._on_main_revert_button_clicked()
        value = self.dialog._get_main_header()
        assert value == self.dialog._main_file.header

    def test__on_tran_clear_button_clicked(self):

        self.dialog._on_tran_clear_button_clicked()
        value = self.dialog._get_translation_header()
        assert value == ""

    def test__on_tran_temp_button_clicked(self):

        self.dialog._on_tran_temp_button_clicked()
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
