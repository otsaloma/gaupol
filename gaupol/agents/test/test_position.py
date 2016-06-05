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
from unittest.mock import patch


class TestPositionAgent(gaupol.TestCase):

    def setup_method(self, method):
        self.application = self.new_application()

    @patch("gaupol.util.flash_dialog", lambda *args: Gtk.ResponseType.CANCEL)
    def test__on_adjust_durations_activate(self):
        self.application.get_action("adjust-durations").activate()

    @patch("gaupol.util.flash_dialog", lambda *args: Gtk.ResponseType.CANCEL)
    def test__on_convert_framerate_activate(self):
        self.application.get_action("convert-framerate").activate()

    @patch("gaupol.util.flash_dialog", lambda *args: Gtk.ResponseType.CANCEL)
    def test__on_shift_positions_activate__frame(self):
        page = self.application.get_current_page()
        page.edit_mode = aeidon.modes.FRAME
        self.application.get_action("shift-positions").activate()

    @patch("gaupol.util.flash_dialog", lambda *args: Gtk.ResponseType.CANCEL)
    def test__on_shift_positions_activate__time(self):
        page = self.application.get_current_page()
        page.edit_mode = aeidon.modes.TIME
        self.application.get_action("shift-positions").activate()

    @patch("gaupol.util.flash_dialog", lambda *args: Gtk.ResponseType.CANCEL)
    def test__on_transform_positions_activate__frame(self):
        page = self.application.get_current_page()
        page.edit_mode = aeidon.modes.FRAME
        self.application.get_action("transform-positions").activate()

    @patch("gaupol.util.flash_dialog", lambda *args: Gtk.ResponseType.CANCEL)
    def test__on_transform_positions_activate__time(self):
        page = self.application.get_current_page()
        page.edit_mode = aeidon.modes.TIME
        self.application.get_action("transform-positions").activate()
