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

    def get_application(self):
        """Return a new application with two open pages."""

        if not hasattr(TestCase, "application"):
            TestCase.application = gaupol.gtk.Application()
            TestCase.application.window.hide()
        application = TestCase.application
        while application.pages:
            application.close_page(application.pages[0], False)
        application.add_new_page(self.get_page())
        application.window.show()
        return application

    def get_page(self):
        """Return a new page with two open documents."""

        page = gaupol.gtk.Page()
        page.project.open_main(self.get_subrip_path(), "ascii")
        page.project.open_translation(self.get_microdvd_path(), "ascii", False)
        return page

    def teardown_method(self, method):
        """Remove state set for executing tests in method."""

        # pylint: disable-msg=E1101
        gaupol.gtk.util.iterate_main()
        if hasattr(self, "dialog"):
            self.dialog.destroy()
        if hasattr(self, "window"):
            self.window.destroy()
        gaupol.gtk.conf.restore_defaults()
