# -*- coding: utf-8-unix -*-

# Copyright (C) 2005-2008,2010 Osmo Salomaa
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

import aeidon
import gaupol

from gi.repository import Gtk


class TestHeaderDialog(gaupol.TestCase):

    def run__show_mpsub_error_dialog(self):
        self.dialog._show_mpsub_error_dialog()

    def run_dialog__both(self):
        self.dialog.run()
        self.dialog.destroy()

    def run_dialog__main(self):
        self.dialog.destroy()
        self.setup_main()
        self.dialog.run()
        self.dialog.destroy()

    def run_dialog__translation(self):
        self.dialog.destroy()
        self.setup_translation()
        self.dialog.run()
        self.dialog.destroy()

    def setup_both(self):
        self.application = self.new_application()
        page = self.application.get_current_page()
        path = self.new_temp_file(aeidon.formats.SUBVIEWER2)
        self.application.open_main(path, "ascii")
        path = self.new_temp_file(aeidon.formats.MPSUB)
        self.application.open_translation(path, "ascii")
        self.dialog = gaupol.HeaderDialog(self.application.window,
                                          self.application)

        self.dialog.show()

    def setup_main(self):
        self.application = self.new_application()
        page = self.application.get_current_page()
        path = self.new_temp_file(aeidon.formats.SUBVIEWER2)
        self.application.open_main(path, "ascii")
        self.dialog = gaupol.HeaderDialog(self.application.window,
                                          self.application)

        self.dialog.show()

    def setup_method(self, method):
        return self.setup_both()

    def setup_translation(self):
        self.application = self.new_application()
        page = self.application.get_current_page()
        path = self.new_temp_file(aeidon.formats.SUBRIP)
        self.application.open_main(path, "ascii")
        path = self.new_temp_file(aeidon.formats.SUBVIEWER2)
        self.application.open_translation(path, "ascii")
        self.dialog = gaupol.HeaderDialog(self.application.window,
                                          self.application)

        self.dialog.show()

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
        self.dialog.response(Gtk.ResponseType.OK)

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

    @aeidon.deco.monkey_patch(gaupol.util, "flash_dialog")
    def test___show_mpsub_error_dialog(self):
        gaupol.util.flash_dialog = lambda *args: Gtk.ResponseType.OK
        self.dialog._show_mpsub_error_dialog()
