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


class TestOutputWindow(gaupol.TestCase):

    def run_window(self):
        self.window.connect("notify::visible", Gtk.main_quit)
        Gtk.main()

    def setup_method(self, method):
        self.window = gaupol.OutputWindow()
        text = self.get_sample_text(aeidon.formats.SUBRIP)
        self.window.set_output(text)
        self.window.show()
