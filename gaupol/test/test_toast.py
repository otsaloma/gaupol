# -*- coding: utf-8 -*-

# Copyright (C) 2013 Osmo Salomaa
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

import gaupol

from gi.repository import Gtk


class TestToast(gaupol.TestCase):

    def run(self):
        self.toast.flash_text("Testing toast notification")
        self.main_loop(self.window)

    def setup_method(self, method):
        self.window = Gtk.Window()
        gaupol.style.load_css(self.window)
        self.window.set_default_size(800, 480)
        self.overlay = Gtk.Overlay()
        self.overlay.set_child(Gtk.Label())
        self.window.set_child(self.overlay)
        self.toast = gaupol.Toast()
        self.overlay.add_overlay(self.toast)
        self.window.show()
