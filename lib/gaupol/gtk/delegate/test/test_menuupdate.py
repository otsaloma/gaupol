# Copyright (C) 2005-2006 Osmo Salomaa
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


import gtk

from gaupol.gtk.app                 import Application
from gaupol.gtk.delegate.menuupdate import MenuUpdateDelegate
from gaupol.test                    import Test


class TestMenuUpdateDelegate(Test):

    def setup_method(self, method):

        self.app = Application()
        self.app.open_main_files([self.get_subrip_path()])
        self.delegate = MenuUpdateDelegate(self.app)

        page = self.app.get_current_page()
        page.project.remove_subtitles([0])
        page.project.remove_subtitles([0])
        page.project.remove_subtitles([0])
        self.app.undo()

    def teardown_method(self, method):

        Test.teardown_method(self, method)
        self.app._window.destroy()

    def test_get_action_group(self):

        for name in ('main', 'recent', 'projects'):
            group = self.delegate._get_action_group(name)
            assert isinstance(group, gtk.ActionGroup)

    def test_set_menu_notify_events(self):

        for name in ('main', 'recent', 'projects'):
            self.app.set_menu_notify_events(name)

    def test_show_menus(self):

        self.app.on_open_button_show_menu()
        self.app.on_redo_button_show_menu()
        self.app.on_show_file_menu_activate()
        self.app.on_show_projects_menu_activate()
        self.app.on_undo_button_show_menu()
