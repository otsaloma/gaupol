# Copyright (C) 2005-2008,2010 Osmo Salomaa
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

import aeidon
import gaupol


class TestViewAgent(gaupol.TestCase):

    def setup_method(self, method):
        self.application = self.new_application()

    def test_on_framerate_combo_changed__frames(self):
        self.application.get_action("show_frames").activate()
        for framerate in aeidon.framerates:
            self.application.framerate_combo.set_active(framerate)

    def test_on_framerate_combo_changed__times(self):
        self.application.get_action("show_times").activate()
        for framerate in aeidon.framerates:
            self.application.framerate_combo.set_active(framerate)

    def test_on_output_window_notify_visible(self):
        self.application.output_window.show()
        self.application.output_window.hide()

    def test_on_show_framerate_24_changed__frames(self):
        self.application.get_action("show_frames").activate()
        for framerate in aeidon.framerates:
            self.application.get_framerate_action(framerate).activate()

    def test_on_show_framerate_24_changed__times(self):
        self.application.get_action("show_times").activate()
        for framerate in aeidon.framerates:
            self.application.get_framerate_action(framerate).activate()

    def test_on_show_times_changed(self):
        for mode in aeidon.modes:
            self.application.get_mode_action(mode).activate()

    def test_on_toggle_duration_column_toggled(self):
        name = "toggle_duration_column"
        self.application.get_action(name).activate()
        self.application.get_action(name).activate()

    def test_on_toggle_end_column_toggled(self):
        name = "toggle_end_column"
        self.application.get_action(name).activate()
        self.application.get_action(name).activate()

    def test_on_toggle_main_text_column_toggled(self):
        name = "toggle_main_text_column"
        self.application.get_action(name).activate()
        self.application.get_action(name).activate()

    def test_on_toggle_main_toolbar_toggled(self):
        name = "toggle_main_toolbar"
        self.application.get_action(name).activate()
        self.application.get_action(name).activate()

    def test_on_toggle_number_column_toggled(self):
        name = "toggle_number_column"
        self.application.get_action(name).activate()
        self.application.get_action(name).activate()

    def test_on_toggle_output_window_toggled(self):
        name = "toggle_output_window"
        self.application.get_action(name).activate()
        self.application.get_action(name).activate()

    def test_on_toggle_start_column_toggled(self):
        name = "toggle_start_column"
        self.application.get_action(name).activate()
        self.application.get_action(name).activate()

    def test_on_toggle_statusbar_activate(self):
        name = "toggle_statusbar"
        self.application.get_action(name).activate()
        self.application.get_action(name).activate()

    def test_on_toggle_translation_text_column_toggled(self):
        name = "toggle_translation_text_column"
        self.application.get_action(name).activate()
        self.application.get_action(name).activate()

    def test_on_toggle_video_toolbar_toggled(self):
        name = "toggle_video_toolbar"
        self.application.get_action(name).activate()
        self.application.get_action(name).activate()
