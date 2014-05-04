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


class TestUtilityAgent(gaupol.TestCase):

    def setup_method(self, method):
        self.application = self.new_application()

    def test_get_action(self):
        self.application.get_action("open_main_files")
        self.application.get_action("show_times")
        self.application.get_action("toggle_number_column")

    def test_get_action_value_error(self):
        self.assert_raises(ValueError,
                           self.application.get_action,
                           "xxx")

    def test_get_action_group(self):
        self.application.get_action_group("main-safe")
        self.application.get_action_group("main-unsafe")
        self.application.get_action_group("audio-tracks")
        self.application.get_action_group("projects")

    def test_get_column_action(self):
        for field in gaupol.fields:
            self.application.get_column_action(field)

    def test_get_current_page(self):
        page = self.application.pages[0]
        self.application.set_current_page(page)
        value = self.application.get_current_page()
        assert value == page

    def test_get_framerate_action(self):
        for framerate in aeidon.framerates:
            self.application.get_framerate_action(framerate)

    def test_get_menu_item(self):
        self.application.get_menu_item("open_main_files")
        self.application.get_menu_item("show_times")
        self.application.get_menu_item("toggle_number_column")

    def test_get_mode_action(self):
        for mode in (aeidon.modes.TIME, aeidon.modes.FRAME):
            self.application.get_mode_action(mode)

    def test_get_target_pages(self):
        get_pages = self.application.get_target_pages
        pages = get_pages(gaupol.targets.SELECTED)
        assert pages == (self.application.get_current_page(),)
        pages = get_pages(gaupol.targets.CURRENT)
        assert pages == (self.application.get_current_page(),)
        pages = get_pages(gaupol.targets.ALL)
        assert pages == tuple(self.application.pages)

    def test_get_target_rows(self):
        page = self.application.get_current_page()
        page.view.select_rows((1, 2, 3))
        get_rows = self.application.get_target_rows
        assert get_rows(gaupol.targets.SELECTED) == (1, 2, 3)
        assert get_rows(gaupol.targets.CURRENT) is None
        assert get_rows(gaupol.targets.ALL) is None

    def test_get_tool_item(self):
        self.application.get_tool_item("undo_action")
        self.application.get_tool_item("insert_subtitles")

    def test_set_current_page(self):
        for i, page in enumerate(self.application.pages):
            self.application.set_current_page(page)
            value = self.application.get_current_page()
            assert value == page
