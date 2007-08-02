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
from .. import confirmation


class TestConfirmationPage(unittest.TestCase):

    def run(self):

        window = gtk.Window()
        window.add(self.page)
        window.connect("delete-event", gtk.main_quit)
        window.show_all()
        gtk.main()

    def setup_method(self, method):

        self.page = confirmation.ConfirmationPage()
        self.test_populate_tree_view()

    def test__on_mark_all_button_clicked(self):

        self.page._mark_all_button.emit("clicked")

    def test__on_remove_check_toggled(self):

        self.page._remove_check.set_active(False)
        self.page._remove_check.set_active(True)

    def test__on_tree_view_cell_toggled(self):

        store = self.page._tree_view.get_model()
        column = self.page._tree_view.get_column(0)
        renderer = column.get_cell_renderers()[0]
        for i in range(len(store)):
            renderer.emit("toggled", i)
            renderer.emit("toggled", i)

    def test__on_tree_view_selection_changed(self):

        selection = self.page._tree_view.get_selection()
        store = self.page._tree_view.get_model()
        for i in range(len(store)):
            selection.select_path(i)

    def test__on_unmark_all_button_clicked(self):

        self.page._unmark_all_button.emit("clicked")

    def test_get_confirmed_changes(self):

        self.page.get_confirmed_changes()

    def test_populate_tree_view(self):

        changes = []
        page = self.get_page()
        for i in range(len(page.project.subtitles)):
            old = page.project.subtitles[i].main_text
            new = page.project.subtitles[i].tran_text
            changes.append((page, i, old, new))
        self.page.populate_tree_view(changes)
