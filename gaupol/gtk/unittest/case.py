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


"""Base class for GTK unit test cases."""


import gtk

from gaupol import unittest
from gaupol.gtk.app import Application
from gaupol.gtk.page import Page


class TestCase(unittest.TestCase):

    """Base class for GTK unit test cases."""

    APPLICATION = Application()

    def __init__(self):

        unittest.TestCase.__init__(self)
        while gtk.events_pending():
            gtk.main_iteration()

    def get_application(self):
        """Get a new application."""

        application = self.APPLICATION
        while application.pages:
            application.close(application.pages[0], False)
        application.add_new_page(self.get_page())
        application.add_new_page(self.get_page())
        return application

    def get_page(self):
        """Get a new page."""

        page = Page()
        page.project.open_main(self.get_subrip_path(), "ascii")
        page.project.open_translation(self.get_microdvd_path(), "ascii")
        return page
