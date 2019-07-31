# -*- coding: utf-8 -*-

# Copyright (C) 2005 Osmo Salomaa
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""Base class for GTK unit test cases."""

import aeidon
import gaupol

__all__ = ("TestCase",)


class TestCase(aeidon.TestCase):

    """
    Base class for GTK unit test cases.

    Unit tests are designed to be run with ``py.test``, ``nose`` or something
    compatible. Tests should use plain ``assert`` statements to allow multiple
    different tools to be used to run the tests.
    """

    def new_application(self):
        """Return a new application with one open page."""
        application = gaupol.Application()
        application.add_page(self.new_page())
        application.window.show()
        return application

    def new_page(self):
        """Return a new page with two open documents."""
        page = gaupol.Page()
        page.project.open_main(self.new_subrip_file(), "ascii")
        page.project.open_translation(self.new_microdvd_file(), "ascii")
        return page

    def teardown_method(self, method):
        """Remove state set for executing tests in `method`."""
        gaupol.util.iterate_main()
        for name in ("assistant", "dialog", "window"):
            if hasattr(self, name):
                getattr(self, name).destroy()
        if hasattr(self, "application"):
            self.application.window.hide()
            self.application.window.destroy()
        gaupol.util.iterate_main()
        gaupol.conf.restore_defaults()
