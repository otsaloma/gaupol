# -*- coding: utf-8-unix -*-

# Copyright (C) 2005-2008,2010 Osmo Salomaa
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

import gaupol

from gi.repository import Gtk


class TestDurationAdjustDialog(gaupol.TestCase):

    def run_dialog(self):
        self.dialog.run()
        self.dialog.destroy()

    def setup_method(self, method):
        self.application = self.new_application()
        page = self.application.get_current_page()
        page.view.select_rows((1, 2, 3))
        self.dialog = gaupol.DurationAdjustDialog(self.application.window,
                                                  self.application)

        self.dialog.show()

    def test___init____no_selection(self):
        page = self.application.get_current_page()
        page.view.select_rows(())
        gaupol.conf.duration_adjust.target = gaupol.targets.SELECTED
        self.dialog = gaupol.DurationAdjustDialog(self.application.window,
                                                  self.application)

    def test__on_gap_check_toggled(self):
        self.dialog._gap_check.set_active(True)
        self.dialog._gap_check.set_active(False)
        self.dialog._gap_check.set_active(True)

    def test__on_lengthen_check_toggled(self):
        self.dialog._lengthen_check.set_active(True)
        self.dialog._lengthen_check.set_active(False)
        self.dialog._lengthen_check.set_active(True)

    def test__on_max_check_toggled(self):
        self.dialog._max_check.set_active(True)
        self.dialog._max_check.set_active(False)
        self.dialog._max_check.set_active(True)

    def test__on_min_check_toggled(self):
        self.dialog._min_check.set_active(True)
        self.dialog._min_check.set_active(False)
        self.dialog._min_check.set_active(True)

    def test__on_response__all(self):
        self.dialog._all_radio.set_active(True)
        self.dialog.response(Gtk.ResponseType.OK)

    def test__on_response__current(self):
        self.dialog._current_radio.set_active(True)
        self.dialog.response(Gtk.ResponseType.OK)

    def test__on_response__selected(self):
        self.dialog._selected_radio.set_active(True)
        self.dialog.response(Gtk.ResponseType.OK)

    def test__on_shorten_check_toggled(self):
        self.dialog._shorten_check.set_active(True)
        self.dialog._shorten_check.set_active(False)
        self.dialog._shorten_check.set_active(True)
