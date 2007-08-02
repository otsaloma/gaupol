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

import gaupol.gtk
import gtk

from gaupol.gtk import unittest
from .. import hearing
from .. import introduction


class TestIntroductionPage(unittest.TestCase):

    def run(self):

        window = gtk.Window()
        window.add(self.page)
        window.connect("delete-event", gtk.main_quit)
        window.show_all()
        gtk.main()

    def setup_method(self, method):

        self.page = introduction.IntroductionPage()
        pages = [hearing.HearingImpairedPage()]
        self.page.populate_tree_view(pages)

    def test__on_tree_view_cell_toggled(self):

        store = self.page._tree_view.get_model()
        column = self.page._tree_view.get_column(0)
        renderer = column.get_cell_renderers()[0]
        for i in range(len(store)):
            renderer.emit("toggled", i)
            renderer.emit("toggled", i)

    def test_get_column(self):

        column = self.page.get_column()
        assert column in gaupol.gtk.COLUMN.members

    def test_get_selected_pages(self):

        self.page.get_selected_pages()

    def test_get_target(self):

        target = self.page.get_target()
        assert target in gaupol.gtk.TARGET.members

    def test_populate_tree_view(self):

        pages = [hearing.HearingImpairedPage()]
        self.page.populate_tree_view(pages)
