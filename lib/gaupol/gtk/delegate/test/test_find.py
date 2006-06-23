# Copyright (C) 2006 Osmo Salomaa
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


from gaupol.gtk.app           import Application
from gaupol.gtk.icons         import *
from gaupol.gtk.delegate.find import FindDelegate
from gaupol.test              import Test


class TestFindDelegate(Test):

    def setup_method(self, method):

        self.app = Application()
        self.app.open_main_files([self.get_subrip_path()])
        self.delegate = FindDelegate(self.app)

    def test_on_dialog_coordinate_request(self):

        page, row, doc = self.delegate._on_dialog_coordinate_request(None)
        assert page == self.app.get_current_page()
        assert row is None
        assert doc is None

        page = self.app.get_current_page()
        page.view.set_focus(3, MTXT)
        page, row, doc = self.delegate._on_dialog_coordinate_request(None)
        assert page == self.app.get_current_page()
        assert row == 3
        assert doc == MAIN

    def test_on_dialog_next_page(self):

        self.delegate._on_dialog_next_page(None)

    def test_on_dialog_previous_page(self):

        self.delegate._on_dialog_previous_page(None)

    def test_on_dialog_update(self):

        self.delegate._on_dialog_update(None)

    def test_actions(self):

        self.app.on_find_activate()
        self.app.on_replace_activate()
