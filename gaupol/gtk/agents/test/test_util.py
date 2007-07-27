# Copyright (C) 2005-2007 Osmo Salomaa
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
# A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# Gaupol.  If not, see <http://www.gnu.org/licenses/>.

import gaupol.gtk

from gaupol.gtk import unittest


class TestUtilityAgent(unittest.TestCase):

    def setup_method(self, method):

        self.application = self.get_application()

    def test_get_action(self):

        self.application.get_action("open_main_files")
        self.application.get_action("show_times")
        self.application.get_action("toggle_number_column")

    def test_get_action_group(self):

        self.application.get_action_group("main")
        self.application.get_action_group("projects")

    def test_get_current_page(self):

        page = self.application.pages[0]
        self.application.set_current_page(page)
        value = self.application.get_current_page()
        assert value == page

    def test_get_menu_item(self):

        self.application.get_menu_item("open_main_files")
        self.application.get_menu_item("show_times")
        self.application.get_menu_item("toggle_number_column")

    def test_get_target_pages(self):

        get_target_pages = self.application.get_target_pages
        pages = get_target_pages(gaupol.gtk.TARGET.SELECTED)
        assert pages == [self.application.get_current_page()]
        pages = get_target_pages(gaupol.gtk.TARGET.CURRENT)
        assert pages == [self.application.get_current_page()]
        pages = get_target_pages(gaupol.gtk.TARGET.ALL)
        assert pages == self.application.pages

    def test_get_target_rows(self):

        page = self.application.get_current_page()
        get_target_rows = self.application.get_target_rows
        page.view.select_rows([1, 2, 3])
        assert get_target_rows(gaupol.gtk.TARGET.SELECTED) == [1, 2, 3]
        assert get_target_rows(gaupol.gtk.TARGET.CURRENT) is None
        assert get_target_rows(gaupol.gtk.TARGET.ALL) is None

    def test_get_tool_item(self):

        self.application.get_tool_item("undo_action")
        self.application.get_tool_item("insert_subtitles")

    def test_set_current_page(self):

        page = self.application.pages[-1]
        self.application.set_current_page(page)
        value = self.application.get_current_page()
        assert value == page
