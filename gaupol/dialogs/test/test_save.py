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


class TestSaveDialog(_TestFileDialog):

    def run_dialog(self):
        self.dialog.run()
        self.dialog.destroy()

    def setup_method(self, method):
        gaupol.conf.file.directory = os.getcwd()
        self.dialog = gaupol.SaveDialog(parent=Gtk.Window(),
                                        title="test",
                                        mode=aeidon.modes.TIME)

        self.dialog.show()

    def test_get_format(self):
        self.dialog.set_format(aeidon.formats.SUBRIP)
        value = self.dialog.get_format()
        assert value == aeidon.formats.SUBRIP

    def test_get_framerate(self):
        self.dialog.set_framerate(aeidon.framerates.FPS_23_976)
        value = self.dialog.get_framerate()
        assert value == aeidon.framerates.FPS_23_976

    def test_get_newline(self):
        self.dialog.set_newline(aeidon.newlines.UNIX)
        value = self.dialog.get_newline()
        assert value == aeidon.newlines.UNIX

    def test__on_response(self):
        self.dialog.response(Gtk.ResponseType.CANCEL)

    def test_set_format(self):
        self.dialog.set_format(aeidon.formats.MICRODVD)
        value = self.dialog.get_format()
        assert value == aeidon.formats.MICRODVD

    def test_set_framerate(self):
        self.dialog.set_framerate(aeidon.framerates.FPS_25_000)
        value = self.dialog.get_framerate()
        assert value == aeidon.framerates.FPS_25_000

    def test_set_name__name__basename(self):
        self.dialog.set_name("test")

    def test_set_name__name__path(self):
        self.dialog.set_name(self.new_subrip_file())

    def test_set_newline(self):
        self.dialog.set_newline(aeidon.newlines.WINDOWS)
        value = self.dialog.get_newline()
        assert value == aeidon.newlines.WINDOWS
