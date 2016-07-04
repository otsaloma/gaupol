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

import gaupol


class TestViewAgent(gaupol.TestCase):

    def setup_method(self, method):
        self.application = self.new_application()

    def test__on_toggle_duration_column_toggled(self):
        name = "toggle-duration-column"
        self.application.get_action(name).activate()
        self.application.get_action(name).activate()

    def test__on_toggle_end_column_toggled(self):
        name = "toggle-end-column"
        self.application.get_action(name).activate()
        self.application.get_action(name).activate()

    def test__on_toggle_main_text_column_toggled(self):
        name = "toggle-main-text-column"
        self.application.get_action(name).activate()
        self.application.get_action(name).activate()

    def test__on_toggle_main_toolbar_toggled(self):
        name = "toggle-main-toolbar"
        self.application.get_action(name).activate()
        self.application.get_action(name).activate()

    def test__on_toggle_number_column_toggled(self):
        name = "toggle-number-column"
        self.application.get_action(name).activate()
        self.application.get_action(name).activate()

    def test__on_toggle_start_column_toggled(self):
        name = "toggle-start-column"
        self.application.get_action(name).activate()
        self.application.get_action(name).activate()

    def test__on_toggle_translation_text_column_toggled(self):
        name = "toggle-translation-text-column"
        self.application.get_action(name).activate()
        self.application.get_action(name).activate()
