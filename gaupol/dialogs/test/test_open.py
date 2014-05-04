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
import os

from gi.repository import Gtk
from gaupol.dialogs.test.test_file import _TestFileDialog


class TestOpenDialog(_TestFileDialog):

    def run_dialog__main(self):
        gaupol.conf.file.directory = os.getcwd()
        doc = aeidon.documents.MAIN
        self.dialog = gaupol.OpenDialog(Gtk.Window(), "test", doc)
        self.dialog.run()

    def run_dialog__translation(self):
        gaupol.conf.file.directory = os.getcwd()
        doc = aeidon.documents.TRAN
        self.dialog = gaupol.OpenDialog(Gtk.Window(), "test", doc)
        self.dialog.run()

    def setup_method(self, method):
        gaupol.conf.file.directory = os.getcwd()
        doc = aeidon.documents.MAIN
        self.dialog = gaupol.OpenDialog(Gtk.Window(), "test", doc)
        self.dialog.show()

    def test__on_response(self):
        self.dialog.response(Gtk.ResponseType.CANCEL)
