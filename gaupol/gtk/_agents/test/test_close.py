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

from gaupol.gtk import cons
from gaupol.gtk.errors import Default
from gaupol.gtk.unittest import TestCase


class TestCloseAgent(TestCase):

    def setup_method(self, method):

        self.application = self.get_application()
        self.delegate = self.application.close.im_self

        def respond(*args):
            return gtk.RESPONSE_DELETE_EVENT
        self.delegate.flash_dialog = respond
        self.delegate.run_dialog = respond

    def test__show_close_warning_dialog(self):

        self.delegate._show_close_warning_dialog(cons.DOCUMENT.MAIN, "test")

    def test_close_confirm(self):

        while self.application.pages:
            self.application.close(self.application.pages[-1])

    def test_close_no_confirm(self):

        while self.application.pages:
            self.application.close(self.application.pages[-1], False)

    def test_on_close_all_projects_activate(self):

        self.application.on_close_all_projects_activate()

    def test_on_close_project_activate(self):

        self.application.on_close_project_activate()

    def test_on_page_close_request(self):

        page = self.application.get_current_page()
        self.application.on_page_close_request(page)

    def test_on_quit_activate(self):

        try:
            self.application.on_quit_activate()
        except SystemExit:
            pass
