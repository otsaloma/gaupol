# Copyright (C) 2005-2006 Osmo Salomaa
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


import gtk

from gaupol.gtk                  import cons
from gaupol.gtk.dialog.duradjust import DurationAdjustDialog
from gaupol.gtk.util             import config, gtklib
from gaupol.test                 import Test


class TestDurationAdjustDialog(Test):

    def setup_method(self, method):

        self.dialog = DurationAdjustDialog(gtk.Window(), True)

    def test_get_gap(self):

        self.dialog._gap_spin.set_value(0.333)
        assert self.dialog.get_gap() == 0.333

    def test_get_lengthen(self):

        self.dialog._lengthen_check.set_active(True)
        assert self.dialog.get_lengthen() is True
        self.dialog._lengthen_check.set_active(False)
        assert self.dialog.get_lengthen() is False

    def test_get_maximum(self):

        self.dialog._max_spin.set_value(0.333)
        assert self.dialog.get_maximum() == 0.333

    def test_get_minimum(self):

        self.dialog._min_spin.set_value(0.333)
        assert self.dialog.get_minimum() == 0.333

    def test_get_optimal(self):

        self.dialog._optimal_spin.set_value(0.333)
        assert self.dialog.get_optimal() == 0.333

    def test_get_shorten(self):

        self.dialog._shorten_check.set_active(True)
        assert self.dialog.get_shorten() is True
        self.dialog._shorten_check.set_active(False)
        assert self.dialog.get_shorten() is False

    def test_get_target(self):

        self.dialog._all_radio.set_active(True)
        assert self.dialog.get_target() == cons.Target.ALL
        self.dialog._current_radio.set_active(True)
        assert self.dialog.get_target() == cons.Target.CURRENT
        self.dialog._selected_radio.set_active(True)
        assert self.dialog.get_target() == cons.Target.SELECTED

    def test_get_use_gap(self):

        self.dialog._gap_check.set_active(True)
        assert self.dialog.get_use_gap() is True
        self.dialog._gap_check.set_active(False)
        assert self.dialog.get_use_gap() is False

    def test_get_use_maximum(self):

        self.dialog._max_check.set_active(True)
        assert self.dialog.get_use_maximum() is True
        self.dialog._max_check.set_active(False)
        assert self.dialog.get_use_maximum() is False

    def test_get_use_minimum(self):

        self.dialog._min_check.set_active(True)
        assert self.dialog.get_use_minimum() is True
        self.dialog._min_check.set_active(False)
        assert self.dialog.get_use_minimum() is False

    def test_run(self):

        gtklib.run(self.dialog)
