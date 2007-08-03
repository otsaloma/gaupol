# Copyright (C) 2007 Osmo Salomaa
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
# A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# Gaupol.  If not, see <http://www.gnu.org/licenses/>.

import gtk

from gaupol.gtk import unittest
from .. import progress


class TestProgressPage(unittest.TestCase):

    def run(self):

        self.test_set_progress()
        window = gtk.Window()
        window.add(self.page)
        window.connect("delete-event", gtk.main_quit)
        window.show_all()
        gtk.main()

    def setup_method(self, method):

        self.page = progress.ProgressPage()
        self.page.reset(100)

    def test_bump_progress(self):

        self.page.bump_progress()

    def test_reset(self):

        self.page.reset(100)

    def test_set_progress(self):

        self.page.set_progress(33, 100)

    def test_set_project_name(self):

        self.page.set_project_name("Test")

    def test_set_task_name(self):

        self.page.set_task_name("Test")
