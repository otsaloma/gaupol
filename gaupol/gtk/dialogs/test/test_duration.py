# Copyright (C) 2005-2007 Osmo Salomaa
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


import gaupol.gtk
import gtk

from gaupol.gtk import unittest
from .. import duration


class TestDurationAdjustDialog(unittest.TestCase):

    def run(self):

        self.dialog.run()
        self.dialog.destroy()

    def setup_method(self, method):

        self.application = self.get_application()
        args = (self.application.window, self.application)
        self.dialog = duration.DurationAdjustDialog(*args)

    def test__adjust_durations(self):

        self.dialog._adjust_durations()

    def test__get_target(self):

        TARGET = gaupol.gtk.TARGET
        target = self.dialog._get_target()
        assert target in (TARGET.SELECTED, TARGET.CURRENT)

    def test__on_gap_check_toggled(self):

        self.dialog._gap_check.emit("toggled")
        self.dialog._gap_check.emit("toggled")
        self.dialog._gap_check.emit("toggled")

    def test__on_lengthen_check_toggled(self):

        self.dialog._lengthen_check.emit("toggled")
        self.dialog._lengthen_check.emit("toggled")
        self.dialog._lengthen_check.emit("toggled")

    def test__on_max_check_toggled(self):

        self.dialog._max_check.emit("toggled")
        self.dialog._max_check.emit("toggled")
        self.dialog._max_check.emit("toggled")

    def test__on_min_check_toggled(self):

        self.dialog._min_check.emit("toggled")
        self.dialog._min_check.emit("toggled")
        self.dialog._min_check.emit("toggled")

    def test__on_response(self):

        self.dialog.response(gtk.RESPONSE_OK)

    def test__on_shorten_check_toggled(self):

        self.dialog._shorten_check.emit("toggled")
        self.dialog._shorten_check.emit("toggled")
        self.dialog._shorten_check.emit("toggled")
