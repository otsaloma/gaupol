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

import gaupol


class TestMenuAgent(gaupol.TestCase):

    def setup_method(self, method):
        self.application = self.new_application()
        self.delegate = self.application.set_menu_notify_events.im_self

    def test_on_redo_button_show_menu(self):
        page = self.application.get_current_page()
        page.project.remove_subtitles((0,))
        page.project.remove_subtitles((0,))
        page.project.undo(2)
        item = self.application.get_tool_item("redo_action")
        item.emit("show-menu")
        item.get_menu().get_children()[0].activate()

    def test_on_show_projects_menu_activate(self):
        self.application.get_action("show_projects_menu").activate()
        self.application.get_action("show_projects_menu").activate()
        self.application.get_action("show_projects_menu").activate()

    def test_on_undo_button_show_menu(self):
        page = self.application.get_current_page()
        page.project.remove_subtitles((0,))
        page.project.remove_subtitles((0,))
        item = self.application.get_tool_item("undo_action")
        item.emit("show-menu")
        item.get_menu().get_children()[0].activate()

    def test_set_menu_notify_events(self):
        self.application.set_menu_notify_events("main-safe")
        self.application.set_menu_notify_events("main-unsafe")
        self.application.set_menu_notify_events("projects")
