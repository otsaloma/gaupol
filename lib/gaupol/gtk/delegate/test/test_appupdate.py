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


from gaupol.gtk.app import Application
from gaupol.test    import Test


class TestApplicationUpdateDelegate(Test):

    def setup_method(self, method):

        self.app = Application()
        self.app.open_main_files([
            self.get_subrip_path(),
            self.get_microdvd_path()
        ])

    def teardown_method(self, method):

        Test.teardown_method(self, method)
        self.app._window.destroy()

    def test_notebook_page_switches(self):

        self.app._uim.get_action('/ui/menubar/projects/next').activate()
        self.app._uim.get_action('/ui/menubar/projects/previous').activate()
        self.app._uim.get_action('/ui/menubar/projects/next').activate()
        self.app._uim.get_action('/ui/menubar/projects/previous').activate()
        self.app._uim.get_action('/ui/menubar/projects/next').activate()

    def test_on_window_state_event(self):

        self.app._window.maximize()
        self.app._window.unmaximize()
        self.app._window.maximize()
        self.app._window.unmaximize()

    def test_set_sensitivities(self):

        page = self.app.get_current_page()
        page.project.insert_subtitles([1])
        self.app._uim.get_action('/ui/menubar/file/close').activate()
        self.app._uim.get_action('/ui/menubar/file/close').activate()
        self.app._uim.get_action('/ui/menubar/file/new').activate()

    def test_set_status_message(self):

        self.app.set_status_message('test')
        self.app.set_status_message('test', False)
        self.app.set_status_message(None)
