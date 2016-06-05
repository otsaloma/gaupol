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


class TestUpdateAgent(gaupol.TestCase):

    def setup_method(self, method):
        self.application = self.new_application()
        self.application.add_page(self.new_page())

    def test_flash_message(self):
        self.application.flash_message("")
        self.application.flash_message(None)

    def test__on_activate_next_project_activate(self):
        self.application.notebook.set_current_page(0)
        self.application.get_action("activate-next-project").activate()

    def test__on_activate_previous_project_activate(self):
        self.application.notebook.set_current_page(-1)
        self.application.get_action("activate-previous-project").activate()

    def test__on_move_tab_left_activate(self):
        self.application.notebook.set_current_page(-1)
        self.application.get_action("move-tab-left").activate()

    def test__on_move_tab_right_activate(self):
        self.application.notebook.set_current_page(0)
        self.application.get_action("move-tab-right").activate()

    def test_show_message(self):
        self.application.show_message("")
        self.application.show_message(None)

    def test_update_gui(self):
        self.application.update_gui()
        self.application.close_all()
        self.application.update_gui()
