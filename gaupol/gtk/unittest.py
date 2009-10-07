# Copyright (C) 2005-2008 Osmo Salomaa
#
# This file is part of Gaupol.
#
# Gaupol is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# Gaupol is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# Gaupol. If not, see <http://www.gnu.org/licenses/>.

"""Base class for GTK unit test cases."""

import gaupol.gtk

__all__ = ("TestCase",)


class TestCase(gaupol.TestCase):

    """Base class for GTK unit test cases."""

    application = None

    def get_application(self):
        """Return a new application with two open pages."""

        application = gaupol.gtk.Application()
        application.add_new_page(self.get_page())
        application.window.show()
        TestCase.application = application
        return application

    def get_page(self):
        """Return a new page with two open documents."""

        page = gaupol.gtk.Page()
        page.project.open_main(self.new_subrip_file(), "ascii")
        page.project.open_translation(self.new_microdvd_file(), "ascii", False)
        return page

    def teardown_method(self, method):
        """Remove state set for executing tests in method."""

        gaupol.gtk.util.iterate_main()
        if hasattr(self, "dialog"):
            self.dialog.destroy()
        if hasattr(self, "window"):
            self.window.destroy()
        if self.application is not None:
            for page in self.application.pages:
                self.application.close_page(page, False)
            self.application.window.destroy()
        TestCase.application = None
        gaupol.gtk.util.iterate_main()
        gaupol.gtk.conf.restore_defaults()
