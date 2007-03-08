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


import gtk

from gaupol.gtk.page import Page
from gaupol.gtk.unittest import TestCase
from .. import app


class TestApplication(TestCase):

    def run(self):

        gtk.main()

    def setup_method(self, method):

        self.application = app.Application()

    def test_get_current_page(self):

        page = self.application.get_current_page()
        assert page is None

        path = self.get_subrip_path()
        self.application.open_main_files([path])
        page = self.application.get_current_page()
        assert isinstance(page, Page)

    def test_set_current_page(self):

        for page in self.application.pages:
            self.application.set_current_page(page)
            assert self.application.get_current_page() == page
