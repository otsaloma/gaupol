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


from gaupol.gtk.app     import Application
from gaupol.gtk.colcons import *
from gaupol.test        import Test


class TestViewUpdateDelegate(Test):

    def setup_method(self, method):

        self.app = Application()
        self.app.open_main_files([self.get_subrip_path()])

    def teardown_method(self, method):

        Test.teardown_method(self, method)
        self.app._window.destroy()

    def test_on_view_move_cursor(self):

        self.app.on_view_move_cursor()
        page = self.app.get_current_page()
        page.view.set_focus(3, MTXT)

    def test_on_view_selection_changed(self):

        self.app.on_view_selection_changed()
        page = self.app.get_current_page()
        page.view.select_rows([1, 2])
        page.view.select_rows([])

    def test_set_character_status(self):

        page = self.app.get_current_page()
        page.view.set_focus(1, MTXT)
        self.app.set_character_status(page)
