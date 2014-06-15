# -*- coding: utf-8 -*-

# Copyright (C) 2005 Osmo Salomaa
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import aeidon
import gaupol

from gi.repository import Gtk
from gaupol.dialogs.test.test_file import _TestFileDialog


class TestMultiSaveDialog(_TestFileDialog):

    def run_dialog(self):
        self.dialog.run()
        self.dialog.destroy()

    @aeidon.deco.silent(gaupol.Default)
    def run__show_overwrite_question_dialog(self):
        files = [x.project.main_file for x in self.application.pages]
        self.dialog._show_overwrite_question_dialog(files, "test")

    def setup_method(self, method):
        self.application = self.new_application()
        self.application.add_page(self.new_page())
        self.application.add_page(self.new_page())
        modes = [x.project.main_file.mode for x in self.application.pages]
        self.dialog = gaupol.MultiSaveDialog(parent=Gtk.Window(),
                                             application=self.application,
                                             modes=modes)

        self.dialog.show()

    def test__on_response(self):
        self.dialog.response(Gtk.ResponseType.CANCEL)
