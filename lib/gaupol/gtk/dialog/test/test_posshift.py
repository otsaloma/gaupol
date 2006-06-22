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

from gaupol.gtk                 import cons
from gaupol.gtk.dialog.posshift import FrameShiftDialog
from gaupol.gtk.dialog.posshift import TimeShiftDialog
from gaupol.gtk.dialog.posshift import _PositionShiftDialog
from gaupol.gtk.page            import Page
from gaupol.gtk.util            import gtklib
from gaupol.test                import Test


class _TestPositionShiftDialog(Test):

    def test_get_target(self):

        self.dialog._current_radio.set_active(True)
        assert self.dialog.get_target() == cons.Target.CURRENT
        self.dialog._selected_radio.set_active(True)
        assert self.dialog.get_target() == cons.Target.SELECTED

    def test_run(self):

        gtklib.run(self.dialog)


class TestFrameShiftDialog(_TestPositionShiftDialog):

    def setup_method(self, method):

        self.page = Page()
        self.page.project = self.get_project()
        self.dialog = FrameShiftDialog(gtk.Window(), self.page)

    def test_get_amount(self):

        self.dialog._amount_spin.set_value(300)
        assert self.dialog.get_amount() == 300


class TestTimeShiftDialog(_TestPositionShiftDialog):

    def setup_method(self, method):

        self.page = Page()
        self.page.project = self.get_project()
        self.dialog = TimeShiftDialog(gtk.Window(), self.page)

    def test_get_amount(self):

        self.dialog._amount_spin.set_value(300.333)
        assert self.dialog.get_amount() == 300.333
