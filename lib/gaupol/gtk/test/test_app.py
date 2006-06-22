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


from gaupol.gtk.app  import Application
from gaupol.gtk.page import Page
from gaupol.test     import Test


class TestApplication(Test):

    def setup_method(self, method):

        self.app = Application()

    def teardown_method(self, method):

        Test.teardown_method(self, method)
        self.app._window.destroy()

    def test_get_current_page(self):

        page = self.app.get_current_page()
        assert page is None

        path = self.get_subrip_path()
        self.app.open_main_files([path])
        page = self.app.get_current_page()
        assert isinstance(page, Page)
