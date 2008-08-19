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
import gtk


class TestMenuAgent(gaupol.gtk.TestCase):

    def setup_method(self, method):

        self.application = self.get_application()
        self.delegate = self.application.set_menu_notify_events.im_self

    def test_on_open_button_show_menu(self):

        item = self.application.get_tool_item("open_main_files")
        item.emit("show-menu")

    def test_on_redo_button_show_menu(self):

        page = self.application.get_current_page()
        page.project.remove_subtitles((0,))
        page.project.remove_subtitles((0,))
        page.project.undo(2)
        item = self.application.get_tool_item("redo_action")
        item.emit("show-menu")
        item.get_menu().get_children()[0].activate()

    def test_on_show_recent_main_menu_activate(self):

        self.application.open_main_file(self.get_subrip_path())
        self.application.open_main_file(self.get_subrip_path())
        self.application.get_action("show_recent_main_menu").activate()

    def test_on_show_recent_translation_menu_activate(self):

        self.application.open_main_file(self.get_subrip_path())
        self.application.open_translation_file(self.get_subrip_path())
        self.application.open_main_file(self.get_subrip_path())
        self.application.open_translation_file(self.get_subrip_path())
        self.application.get_action("show_recent_translation_menu").activate()

    def test_on_undo_button_show_menu(self):

        page = self.application.get_current_page()
        page.project.remove_subtitles((0,))
        page.project.remove_subtitles((0,))
        item = self.application.get_tool_item("undo_action")
        item.emit("show-menu")
        item.get_menu().get_children()[0].activate()

    def test_set_menu_notify_events(self):

        self.application.set_menu_notify_events("main")
        self.application.set_menu_notify_events("projects")

    def test_update_project_actions(self):

        self.application.open_main_file(self.get_subrip_path())
        self.application.open_main_file(self.get_subrip_path())
        self.application.update_project_actions()
        self.application.update_project_actions()
