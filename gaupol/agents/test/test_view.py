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


class TestViewAgent(gaupol.TestCase):

    def setup_method(self, method):
        self.application = self.new_application()

    def test__on_output_window_notify_visible(self):
        self.application.output_window.show()
        self.application.output_window.hide()

    def test__on_show_framerate_23_976_changed__frames(self):
        self.application.get_action("show_frames").activate()
        framerate = aeidon.framerates.FPS_25_000
        self.application.get_framerate_action(framerate).activate()

    def test__on_show_framerate_23_976_changed__times(self):
        self.application.get_action("show_times").activate()
        framerate = aeidon.framerates.FPS_29_970
        self.application.get_framerate_action(framerate).activate()

    def test__on_show_times_changed(self):
        self.application.get_action("show_frames").activate()
        self.application.get_action("show_times").activate()

    def test__on_toggle_duration_column_toggled(self):
        name = "toggle_duration_column"
        self.application.get_action(name).activate()
        self.application.get_action(name).activate()

    def test__on_toggle_end_column_toggled(self):
        name = "toggle_end_column"
        self.application.get_action(name).activate()
        self.application.get_action(name).activate()

    def test__on_toggle_main_text_column_toggled(self):
        name = "toggle_main_text_column"
        self.application.get_action(name).activate()
        self.application.get_action(name).activate()

    def test__on_toggle_main_toolbar_toggled(self):
        name = "toggle_main_toolbar"
        self.application.get_action(name).activate()
        self.application.get_action(name).activate()

    def test__on_toggle_number_column_toggled(self):
        name = "toggle_number_column"
        self.application.get_action(name).activate()
        self.application.get_action(name).activate()

    def test__on_toggle_output_window_toggled(self):
        name = "toggle_output_window"
        self.application.get_action(name).activate()
        self.application.get_action(name).activate()

    def test__on_toggle_start_column_toggled(self):
        name = "toggle_start_column"
        self.application.get_action(name).activate()
        self.application.get_action(name).activate()

    def test__on_toggle_translation_text_column_toggled(self):
        name = "toggle_translation_text_column"
        self.application.get_action(name).activate()
        self.application.get_action(name).activate()
