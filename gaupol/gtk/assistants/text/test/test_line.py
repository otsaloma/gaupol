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
from .. import line


class TestLineBreakPage(unittest.TestCase):

    def run(self):

        window = gtk.Window()
        window.add(self.page)
        window.connect("delete-event", gtk.main_quit)
        window.show_all()
        gtk.main()

    def setup_method(self, method):

        self.page = line.LineBreakPage()

    def test_correct_texts(self):

        project = self.get_project()
        doc = gaupol.gtk.DOCUMENT.MAIN
        self.page.correct_texts(project, None, doc)


class TestLineBreakOptionsPage(unittest.TestCase):

    def run(self):

        window = gtk.Window()
        window.add(self.page)
        window.connect("delete-event", gtk.main_quit)
        window.show_all()
        gtk.main()

    def setup_method(self, method):

        self.page = line.LineBreakOptionsPage()

    def test__on_max_length_spin_value_changed(self):

        self.page._max_length_spin.set_value(2)
        self.page._max_length_spin.set_value(3)

    def test__on_max_lines_spin_value_changed(self):

        self.page._max_lines_spin.set_value(22)
        self.page._max_lines_spin.set_value(33)

    def test__on_max_skip_length_spin_value_changed(self):

        self.page._max_skip_length_spin.set_value(2)
        self.page._max_skip_length_spin.set_value(3)

    def test__on_max_skip_lines_spin_value_changed(self):

        self.page._max_skip_lines_spin.set_value(22)
        self.page._max_skip_lines_spin.set_value(33)

    def test__on_skip_length_check_toggled(self):

        self.page._skip_length_check.set_active(False)
        self.page._skip_length_check.set_active(True)

    def test__on_skip_lines_check_toggled(self):

        self.page._skip_lines_check.set_active(False)
        self.page._skip_lines_check.set_active(True)

    def test__on_skip_unit_combo_changed(self):

        self.page._skip_unit_combo.set_active(0)
        assert self.page._unit_combo.get_active() == 0
        self.page._skip_unit_combo.set_active(1)
        assert self.page._unit_combo.get_active() == 1

    def test__on_unit_combo_changed(self):

        self.page._unit_combo.set_active(0)
        assert self.page._skip_unit_combo.get_active() == 0
        self.page._unit_combo.set_active(1)
        assert self.page._skip_unit_combo.get_active() == 1
