# Copyright (C) 2005-2008 Osmo Salomaa
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

import gaupol.gtk


class TestUtilityAgent(gaupol.gtk.TestCase):

    def setup_method(self, method):

        self.application = self.get_application()

    def test_get_action(self):

        self.application.get_action("open_main_files")
        self.application.get_action("show_times")
        self.application.get_action("toggle_number_column")

    def test_get_action_group(self):

        self.application.get_action_group("main")
        self.application.get_action_group("projects")

    def test_get_column_action(self):

        for field in gaupol.gtk.fields:
            self.application.get_column_action(field)
        function = self.application.get_column_action
        self.raises(ValueError, function, None)

    def test_get_current_page(self):

        page = self.application.pages[0]
        self.application.set_current_page(page)
        current_page = self.application.get_current_page()
        assert current_page == page

    def test_get_framerate_action(self):

        for framerate in gaupol.framerates:
            self.application.get_framerate_action(framerate)
        function = self.application.get_framerate_action
        self.raises(ValueError, function, None)

    def test_get_menu_item(self):

        self.application.get_menu_item("open_main_files")
        self.application.get_menu_item("show_times")
        self.application.get_menu_item("toggle_number_column")

    def test_get_mode_action(self):

        for mode in gaupol.modes:
            self.application.get_mode_action(mode)
        function = self.application.get_mode_action
        self.raises(ValueError, function, None)

    def test_get_target_pages(self):

        get_pages = self.application.get_target_pages
        pages = get_pages(gaupol.gtk.targets.SELECTED)
        assert pages == (self.application.get_current_page(),)
        pages = get_pages(gaupol.gtk.targets.CURRENT)
        assert pages == (self.application.get_current_page(),)
        pages = get_pages(gaupol.gtk.targets.ALL)
        assert pages == tuple(self.application.pages)
        self.raises(ValueError, get_pages, None)

    def test_get_target_rows(self):

        page = self.application.get_current_page()
        get_rows = self.application.get_target_rows
        page.view.select_rows((1, 2, 3))
        assert get_rows(gaupol.gtk.targets.SELECTED) == (1, 2, 3)
        assert get_rows(gaupol.gtk.targets.CURRENT) is None
        assert get_rows(gaupol.gtk.targets.ALL) is None

    def test_get_tool_item(self):

        self.application.get_tool_item("undo_action")
        self.application.get_tool_item("insert_subtitles")

    def test_set_current_page(self):

        for i, page in enumerate(self.application.pages):
            self.application.set_current_page(page)
            current_page = self.application.get_current_page()
            assert current_page == page
