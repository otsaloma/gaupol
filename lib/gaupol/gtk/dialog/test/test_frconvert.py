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

from gaupol.gtk.dialog.frconvert import FramerateConvertDialog
from gaupol.gtk.util             import gtklib
from gaupol.test                 import Test


class TestFramerateConvertDialog(Test):

    def setup_method(self, method):

        self.dialog = FramerateConvertDialog(gtk.Window())

    def test_get_correct(self):

        self.dialog._correct_combo.set_active(0)
        assert self.dialog.get_correct() == 0
        self.dialog._correct_combo.set_active(1)
        assert self.dialog.get_correct() == 1

    def test_get_current(self):

        self.dialog._current_combo.set_active(0)
        assert self.dialog.get_current() == 0
        self.dialog._current_combo.set_active(1)
        assert self.dialog.get_current() == 1

    def test_run(self):

        gtklib.run(self.dialog)
