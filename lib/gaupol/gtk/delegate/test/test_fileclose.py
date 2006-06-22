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

from gaupol.gtk                    import cons
from gaupol.gtk.app                import Application
from gaupol.gtk.colcons            import *
from gaupol.gtk.delegate.fileclose import _CloseWarningDialog
from gaupol.gtk.util               import gtklib
from gaupol.test                   import Test


class TestCloseWarningDialog(Test):

    def test_run(self):

        gtklib.run(_CloseWarningDialog(gtk.Window(), MAIN, 'test'))


class TestFileCloseDelegate(Test):

    def setup_method(self, method):

        self.app = Application()

    def teardown_method(self, method):

        self.app._window.destroy()

    def test_on_close_all_projects_activate(self):

        self.app.open_main_files([self.get_subrip_path()])
        self.app.open_main_files([self.get_subrip_path()])
        self.app.open_main_files([self.get_subrip_path()])
        self.app.on_close_all_projects_activate()

    def test_on_close_project_activate(self):

        self.app.open_main_files([self.get_subrip_path()])
        project = self.app.get_current_page().project
        project.set_text(0, MAIN, 'test')
        self.app.on_close_project_activate()

    def test_on_page_closed(self):

        self.app.open_main_files([self.get_subrip_path()])
        project = self.app.get_current_page().project
        project.set_text(0, MAIN, 'test')
        project.set_text(0, TRAN, 'test')
        self.app.on_page_closed(self.app.get_current_page())

    def test_on_quit_activate(self):

        try:
            self.app.on_quit_activate()
        except SystemExit:
            pass

    def test_on_window_delete_event(self):

        try:
            self.app.on_window_delete_event()
        except SystemExit:
            pass
