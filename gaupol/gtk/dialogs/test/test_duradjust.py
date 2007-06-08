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


import gtk

from gaupol.gtk import const
from gaupol.gtk import unittest
from .. import duradjust


class TestDurationAdjustDialog(unittest.TestCase):

    def run(self):

        self.dialog.run()
        self.dialog.destroy()

    def setup_method(self, method):

        self.application = self.get_application()
        parent = self.application.window
        self.dialog = duradjust.DurationAdjustDialog(parent, self.application)
        self.dialog.show()

    def test__adjust(self):

        self.dialog._adjust()

    def test__get_target(self):

        target = self.dialog._get_target()
        assert target in (gaupol.gtk.TARGET.SELECTED, gaupol.gtk.TARGET.CURRENT)

    def test__get_target_pages(self):

        pages = self.dialog._get_target_pages()
        assert isinstance(pages, list)

    def test__get_target_rows(self):

        rows = self.dialog._get_target_rows()
        if rows is not None:
            assert isinstance(rows, list)

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
