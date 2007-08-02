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


class TestHearingImpairedPage(unittest.TestCase):

    def run(self):

        window = gtk.Window()
        window.add(self.page)
        window.connect("delete-event", gtk.main_quit)
        window.show_all()
        gtk.main()

    def setup_method(self, method):

        self.page = hearing.HearingImpairedPage()

    def test__get_country(self):

        country = self.page._get_country()
        if country is not None:
            assert country in gaupol.countries.countries

    def test__get_language(self):

        language = self.page._get_language()
        if language is not None:
            assert language in gaupol.languages.languages

    def test__get_script(self):

        script = self.page._get_script()
        if script is not None:
            assert script in gaupol.scripts.scripts

    def test__on_country_combo_changed(self):

        store = self.page._country_combo.get_model()
        for i in range(len(store)):
            if store[i][0] != gaupol.gtk.COMBO_SEPARATOR:
                self.page._country_combo.set_active(i)

    def test__on_language_combo_changed(self):

        store = self.page._language_combo.get_model()
        for i in range(len(store)):
            if store[i][0] != gaupol.gtk.COMBO_SEPARATOR:
                self.page._language_combo.set_active(i)

    def test__on_script_combo_changed(self):

        store = self.page._script_combo.get_model()
        for i in range(len(store)):
            if store[i][0] != gaupol.gtk.COMBO_SEPARATOR:
                self.page._script_combo.set_active(i)

    def test__on_tree_view_cell_toggled(self):

        store = self.page._tree_view.get_model()
        column = self.page._tree_view.get_column(0)
        renderer = column.get_cell_renderers()[0]
        for i in range(len(store)):
            renderer.emit("toggled", i)
            renderer.emit("toggled", i)

    def test__populate_tree_view(self):

        self.page._populate_tree_view()

    def test_correct_texts(self):

        project = self.get_project()
        doc = gaupol.gtk.DOCUMENT.MAIN
        self.page.correct_texts(project, None, doc)
