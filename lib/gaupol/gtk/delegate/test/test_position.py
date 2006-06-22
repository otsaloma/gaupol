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


from gaupol.gtk     import cons
from gaupol.gtk.app import Application
from gaupol.test    import Test


ALL      = cons.Target.ALL
CURRENT  = cons.Target.CURRENT
SELECTED = cons.Target.SELECTED


class TestPositionDelegate(Test):

    def setup_method(self, method):

        Test.__init__(self)
        self.app = Application()
        self.app.open_main_files([self.get_subrip_path()])
        self.app.open_main_files([self.get_subrip_path()])

    def teardown_method(self, method):

        Test.teardown_method(self, method)
        self.app._window.destroy()

    def test_actions(self):

        self.app.on_adjust_durations_activate()
        self.app.on_adjust_positions_activate()
        self.app.on_convert_framerate_activate()
        self.app.on_shift_positions_activate()

    def test_get_target_pages(self):

        page = self.app.get_current_page()
        assert self.app.get_target_pages(ALL)      == self.app.pages
        assert self.app.get_target_pages(CURRENT)  == [page]
        assert self.app.get_target_pages(SELECTED) == [page]

    def test_get_target_rows(self):

        page = self.app.get_current_page()
        page.view.select_rows([1, 2, 3])
        assert self.app.get_target_rows(ALL)      is None
        assert self.app.get_target_rows(CURRENT)  is None
        assert self.app.get_target_rows(SELECTED) == [1, 2, 3]
