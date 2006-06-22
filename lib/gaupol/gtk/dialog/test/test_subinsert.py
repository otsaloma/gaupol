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

from gaupol.gtk.dialog.subinsert import SubtitleInsertDialog
from gaupol.gtk.util             import gtklib
from gaupol.test                 import Test


class TestSubtitleInsertDialog(Test):

    def setup_method(self, method):

        self.dialog = SubtitleInsertDialog(gtk.Window(), self.get_project())

    def test_get_above(self):

        self.dialog._position_combo.set_active(0)
        assert self.dialog.get_above() is True
        self.dialog._position_combo.set_active(1)
        assert self.dialog.get_above() is False

    def test_get_amount(self):

        self.dialog._amount_spin.set_value(333)
        assert self.dialog.get_amount() == 333

    def test_run(self):

        gtklib.run(self.dialog)
