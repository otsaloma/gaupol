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
        self.label.flash_text("Testing...")
        self.window.connect("notify::visible", Gtk.main_quit)
        Gtk.main()

    def setup_method(self, method):
        # We need an application to load our custom CSS.
        # See Application._init_css.
        self.application = self.new_application()
        self.window = Gtk.Window()
        self.window.set_default_size(800, 480)
        self.window.connect("delete-event", Gtk.main_quit)
        self.overlay = Gtk.Overlay()
        self.overlay.add(Gtk.Label())
        self.window.add(self.overlay)
        self.label = gaupol.FloatingLabel()
        self.overlay.add_overlay(self.label)
        self.window.show_all()

    def test_flash_text(self):
        self.label.flash_text("Test")

    def test_get_text(self):
        self.label.set_text("Test")
        text = self.label.get_text()
        assert text == "Test"

    def test_hide(self):
        self.label.set_text("Test")
        self.label.show()
        self.label.hide()
        assert not self.label.props.visible

    def test_register_hide_event(self):
        self.label.show()
        button = Gtk.Button()
        self.label.register_hide_event(button, "clicked")
        button.emit("clicked")
        assert not self.label.props.visible

    def test_set_text(self):
        self.label.set_text("Test")
        text = self.label.get_text()
        assert text == "Test"

    def test_show(self):
        self.label.set_text("Test")
        self.label.show()
        assert self.label.props.visible
        self.label.hide()
