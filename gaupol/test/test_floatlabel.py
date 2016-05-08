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


class TestFloatingLabel(gaupol.TestCase):

    def run(self):
        self.label.flash_text("Testing floating label")
        self.window.connect("notify::visible", Gtk.main_quit)
        Gtk.main()

    def setup_method(self, method):
        self.window = Gtk.Window()
        gaupol.style.load_css(self.window)
        self.window.set_default_size(800, 480)
        self.window.connect("delete-event", Gtk.main_quit)
        self.overlay = Gtk.Overlay()
        self.overlay.add(Gtk.Label())
        self.window.add(self.overlay)
        self.label = gaupol.FloatingLabel()
        self.overlay.add_overlay(self.label)
        self.window.show_all()
