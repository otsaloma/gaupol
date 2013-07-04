# -*- coding: utf-8 -*-

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


class TestUpdateAgent(gaupol.TestCase):

    def setup_method(self, method):
        self.application = self.new_application()
        self.application.add_page(self.new_page())

    def test__on_activate_next_project_activate(self):
        self.application.notebook.set_current_page(0)
        self.application.get_action("activate_next_project").activate()

    def test__on_activate_previous_project_activate(self):
        self.application.notebook.set_current_page(-1)
        self.application.get_action("activate_previous_project").activate()

    def test__on_conf_application_window_notify_toolbar_style(self):
        for style in gaupol.toolbar_styles:
            gaupol.conf.application_window.toolbar_style = style

    def test__on_move_tab_left_activate(self):
        self.application.notebook.set_current_page(-1)
        self.application.get_action("move_tab_left").activate()

    def test__on_move_tab_right_activate(self):
        self.application.notebook.set_current_page(0)
        self.application.get_action("move_tab_right").activate()

    def test__on_notebook_page_reordered(self):
        self.application.notebook.set_current_page(-1)
        self.application.get_action("move_tab_left").activate()

    def test__on_notebook_switch_page(self):
        self.application.notebook.set_current_page(0)
        self.application.notebook.set_current_page(-1)

    def test__on_view_move_cursor(self):
        page = self.application.get_current_page()
        page.view.emit("move-cursor", 1, 1)
        page.view.emit("move-cursor", 1, 1)
        gaupol.util.iterate_main()

    def test__on_view_selection_changed(self):
        page = self.application.get_current_page()
        page.view.select_rows((0,))
        page.view.select_rows((1,))

    def test__on_window_window_state_event(self):
        self.application.window.unmaximize()
        self.application.window.maximize()
        self.application.window.unmaximize()
        gaupol.util.iterate_main()

    def test_flash_message(self):
        self.application.flash_message("")
        self.application.flash_message(None)

    def test_push_message(self):
        self.application.push_message("")
        self.application.push_message(None)

    def test_show_message(self):
        self.application.show_message("")
        self.application.show_message(None)

    def test_update_gui(self):
        self.application.update_gui()
        self.application.close_all()
        self.application.update_gui()

    def test_update_gui__revert(self):
        page = self.application.get_current_page()
        page.project.remove_subtitles((0,))
        page.project.remove_subtitles((0,))
        self.application.update_gui()
        page.project.undo()
        self.application.update_gui()
