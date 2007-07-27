# Copyright (C) 2005-2007 Osmo Salomaa
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
# A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# Gaupol.  If not, see <http://www.gnu.org/licenses/>.

import gaupol.gtk
import gtk

from gaupol.gtk import unittest
from .. import output


class TestOutputWindow(unittest.TestCase):

    def run(self):

        @gaupol.gtk.util.asserted_return
        def destroy(*args):
            assert not self.window.props.visible
            self.window.destroy()
            gtk.main_quit()
        self.window.connect("notify::visible", destroy)
        text = self.get_file_text(gaupol.gtk.FORMAT.MPSUB)
        self.window.set_output(text)
        self.window.show()
        gtk.main()

    def setup_method(self, method):

        self.window = output.OutputWindow()

    def test__on_close_button_clicked(self):

        self.window._on_close_button_clicked()

    def test__on_close_key_pressed(self):

        self.window._on_close_key_pressed()

    def test__on_delete_event(self):

        self.window._on_delete_event()

    def test_on_window_state_event(self):

        self.window.maximize()
        self.window.unmaximize()

    def test__save_geometry(self):

        self.window._save_geometry()

    def test_set_output(self):

        self.window.set_output("test")
        text_buffer = self.window._text_view.get_buffer()
        bounds = text_buffer.get_bounds()
        text = text_buffer.get_text(*bounds)
        assert text == "test"
