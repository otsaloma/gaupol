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


from gaupol.gtk import unittest


class TestMenuAgent(unittest.TestCase):

    def setup_method(self, method):

        self.application = self.get_application()
        self.delegate = self.application.set_menu_notify_events.im_self

    def test_on_open_button_show_menu(self):

        self.application.on_open_button_show_menu()

    def test_on_redo_button_show_menu(self):

        self.application.on_redo_button_show_menu()

    def test_on_show_projects_menu_activate(self):

        self.application.on_show_projects_menu_activate()

    def test_on_show_recent_main_menu_activate(self):

        self.application.on_show_recent_main_menu_activate()

    def test_on_show_recent_translation_menu_activate(self):

        self.application.on_show_recent_translation_menu_activate()

    def test_on_undo_button_show_menu(self):

        self.application.on_undo_button_show_menu()

    def test_set_menu_notify_events(self):

        self.application.set_menu_notify_events("main")
