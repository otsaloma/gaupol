# Copyright (C) 2005-2007 Osmo Salomaa
#
# This file is part of Gaupol.
#
# Gaupol is free software; you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.
#
# Gaupol is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# Gaupol; if not, write to the Free Software Foundation, Inc., 51 Franklin
# Street, Fifth Floor, Boston, MA 02110-1301, USA.


import gaupol.gtk
from gaupol.gtk import unittest


class TestUpdateAgent(unittest.TestCase):

    def setup_method(self, method):

        self.application = self.get_application()
        self.application.add_new_page(self.get_page())

    def test_flash_message(self):

        self.application.flash_message("")
        self.application.flash_message(None)

    def test_on_activate_next_project_activate(self):
z
        self.application.notebook.set_current_page(0)
        self.application.on_activate_next_project_activate()

    def test_on_activate_previous_project_activate(self):

        self.application.notebook.set_current_page(1)
        self.application.on_activate_previous_project_activate()

    def test_on_conf_application_window_notify_toolbar_style(self):

        for style in gaupol.gtk.TOOLBAR_STYLE.members:
            gaupol.gtk.conf.application_window.toolbar_style = style

    def test_on_move_tab_left_activate(self):

        self.application.notebook.set_current_page(1)
        self.application.on_move_tab_left_activate()

    def test_on_move_tab_right_activate(self):

        self.application.notebook.set_current_page(0)
        self.application.on_move_tab_right_activate()

    def test_on_notebook_page_reordered(self):

        self.application.notebook.set_current_page(0)
        self.application.on_move_tab_right_activate()

    def test_on_notebook_switch_page(self):

        self.application.notebook.set_current_page(0)
        self.application.notebook.set_current_page(1)

    def test_on_view_move_cursor(self):

        page = self.application.get_current_page()
        page.view.set_focus(0, 1)
        page.view.set_focus(1, 2)

    def test_on_view_selection_changed(self):

        page = self.application.get_current_page()
        page.view.select_rows([0])
        page.view.select_rows([1])

    def test_on_window_window_state_event(self):

        self.application.window.maximize()
        self.application.window.unmaximize()
        self.application.window.maximize()
        self.application.window.unmaximize()

    def test_push_message(self):

        self.application.push_message("")
        self.application.push_message(None)

    def test_update_gui(self):

        # FIX
        self.application.update_gui()
        #self.application.on_close_all_projects_activate()
        #self.application.update_gui()
