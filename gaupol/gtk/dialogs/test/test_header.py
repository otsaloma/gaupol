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

import functools
import gaupol.gtk
import gtk


class TestHeaderDialog(gaupol.gtk.TestCase):

    def run__dialog__both(self):

        self.setup_both()
        self.dialog.run()
        self.dialog.destroy()

    def run__dialog__main(self):

        self.setup_main()
        self.dialog.run()
        self.dialog.destroy()

    def run__dialog__translation(self):

        self.setup_translation()
        self.dialog.run()
        self.dialog.destroy()

    def run__show_mpsub_error_dialog(self):

        flash_dialog = gaupol.gtk.Runner.flash_dialog
        flash_dialog = functools.partial(flash_dialog, self.application)
        self.dialog.flash_dialog = flash_dialog
        self.dialog._show_mpsub_error_dialog()

    def setup_both(self):

        self.application = self.get_application()
        page = self.application.get_current_page()
        path = self.new_temp_file(gaupol.formats.SUBVIEWER2)
        self.application.open_main_file(path, "ascii")
        path = self.new_temp_file(gaupol.formats.MPSUB)
        self.application.open_translation_file(path, "ascii")
        args = (self.application.window, self.application)
        self.dialog = gaupol.gtk.HeaderDialog(*args)
        self.dialog.show()

    def setup_main(self):

        self.application = self.get_application()
        page = self.application.get_current_page()
        path = self.new_temp_file(gaupol.formats.SUBVIEWER2)
        self.application.open_main_file(path, "ascii")
        path = self.new_temp_file(gaupol.formats.SUBRIP)
        self.application.open_translation_file(path, "ascii")
        args = (self.application.window, self.application)
        self.dialog = gaupol.gtk.HeaderDialog(*args)
        self.dialog.show()

    def setup_method(self, method):

        return self.setup_both()

    def setup_translation(self):

        self.application = self.get_application()
        page = self.application.get_current_page()
        path = self.new_temp_file(gaupol.formats.SUBRIP)
        self.application.open_main_file(path, "ascii")
        path = self.new_temp_file(gaupol.formats.SUBVIEWER2)
        self.application.open_translation_file(path, "ascii")
        args = (self.application.window, self.application)
        self.dialog = gaupol.gtk.HeaderDialog(*args)
        self.dialog.show()

    def test__get_main_header(self):

        self.dialog._set_main_header("test")
        value = self.dialog._get_main_header()
        assert value == "test"

    def test__get_translation_header(self):

        self.dialog._set_translation_header("test")
        value = self.dialog._get_translation_header()
        assert value == "test"

    def test__init_sizes(self):

        self.setup_both()
        self.setup_main()
        self.setup_translation()

    def test__on_copy_down_button_clicked(self):

        self.dialog._copy_down_button.clicked()
        value = self.dialog._get_translation_header()
        assert value == self.dialog._main_file.header

    def test__on_copy_up_button_clicked(self):

        self.dialog._copy_up_button.clicked()
        value = self.dialog._get_main_header()
        assert value == self.dialog._tran_file.header

    def test__on_main_clear_button_clicked(self):

        self.dialog._main_clear_button.clicked()
        value = self.dialog._get_main_header()
        assert value == ""

    def test__on_main_template_button_clicked(self):

        self.dialog._main_template_button.clicked()
        value = self.dialog._get_main_header()
        format = self.dialog._main_file.format
        assert value == aeidon.util.get_template_header(format)

    def test__on_main_revert_button_clicked(self):

        self.dialog._main_clear_button.clicked()
        self.dialog._main_revert_button.clicked()
        value = self.dialog._get_main_header()
        assert value == self.dialog._main_file.header

    def test__on_response(self):

        self.dialog.response(gtk.RESPONSE_OK)

    def test__on_tran_clear_button_clicked(self):

        self.dialog._tran_clear_button.clicked()
        value = self.dialog._get_translation_header()
        assert value == ""

    def test__on_tran_template_button_clicked(self):

        self.dialog._tran_template_button.clicked()
        value = self.dialog._get_translation_header()
        format = self.dialog._tran_file.format
        assert value == aeidon.util.get_template_header(format)

    def test__on_tran_revert_button_clicked(self):

        self.dialog._tran_clear_button.clicked()
        self.dialog._tran_revert_button.clicked()
        value = self.dialog._get_translation_header()
        assert value == self.dialog._tran_file.header

    def test__save_mpsub_header(self):

        respond = lambda *args: gtk.RESPONSE_DELETE_EVENT
        self.dialog.flash_dialog = respond
        self.dialog._set_translation_header("test")
        self.dialog.response(gtk.RESPONSE_OK)
        self.dialog._set_translation_header("FORMAT=23.98")
        self.dialog.response(gtk.RESPONSE_OK)

    def test__set_main_header(self):

        self.dialog._set_main_header("test")
        value = self.dialog._get_main_header()
        assert value == "test"

    def test__set_translation_header(self):

        self.dialog._set_translation_header("test")
        value = self.dialog._get_translation_header()
        assert value == "test"

    def test__show_mpsub_error_dialog(self):

        respond = lambda *args: gtk.RESPONSE_DELETE_EVENT
        self.dialog.flash_dialog = respond
        self.dialog._show_mpsub_error_dialog()
