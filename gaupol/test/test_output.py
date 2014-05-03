# -*- coding: utf-8 -*-

# Copyright (C) 2005-2008,2010 Osmo Salomaa
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


class TestOutputWindow(gaupol.TestCase):

    def run__window(self):
        self.window.connect("notify::visible", Gtk.main_quit)
        Gtk.main()

    def setup_method(self, method):
        self.conf = gaupol.conf.output_window
        self.window = gaupol.OutputWindow()
        text = self.get_sample_text(aeidon.formats.SUBRIP)
        self.window.set_output(text)
        self.window.show()

    def test__init_sizes(self):
        self.conf.maximized = True
        self.window = gaupol.OutputWindow()

    def test__on_close_button_clicked(self):
        self.window._close_button.clicked()

    def test__on_close_key_pressed(self):
        self.window._on_close_key_pressed()

    def test__on_delete_event(self):
        self.window.emit("delete-event", None)

    def test__on_notify_visibile(self):
        self.window.hide()
        assert not self.conf.show
        self.window.show()
        assert self.conf.show

    def test__on_window_state_event(self):
        self.window.maximize()
        self.window.unmaximize()

    def test_set_output(self):
        self.window.set_output("test")
