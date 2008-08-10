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

import gaupol.gtk
import gtk


class TestOutputWindow(gaupol.gtk.TestCase):

    def run__window(self):

        self.window.connect("notify::visible", gtk.main_quit)
        gtk.main()

    def setup_method(self, method):

        self.conf = gaupol.gtk.conf.output_window
        self.window = gaupol.gtk.OutputWindow()
        text = self.get_file_text(gaupol.formats.MPSUB)
        self.window.set_output(text)
        self.window.show()

    def test__init_sizes(self):

        self.conf.maximized = True
        self.window = gaupol.gtk.OutputWindow()

    def test__on_close_button_clicked(self):

        self.window._close_button.clicked()

    def test__on_close_key_pressed(self):

        self.window._on_close_key_pressed()

    def test__on_delete_event(self):

        self.window.emit("delete-event", None)

    def test__on_notify_visibility(self):

        self.window.hide()
        assert not self.conf.show
        self.window.show()
        assert self.conf.show

    def test__on_window_state_event(self):

        self.window.maximize()
        self.window.unmaximize()

    def test_set_output(self):

        self.window.set_output("test")
        text_buffer = self.window._text_view.get_buffer()
        bounds = text_buffer.get_bounds()
        assert text_buffer.get_text(*bounds) == "test"
