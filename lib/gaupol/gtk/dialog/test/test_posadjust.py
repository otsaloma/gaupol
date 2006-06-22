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
from gaupol.gtk.dialog.posadjust import FrameAdjustDialog
from gaupol.gtk.dialog.posadjust import TimeAdjustDialog
from gaupol.gtk.dialog.posadjust import _PositionAdjustDialog
from gaupol.gtk.page             import Page
from gaupol.gtk.util             import gtklib
from gaupol.test                 import Test


class _TestPositionAdjustDialog(Test):

    def test_get_target(self):

        self.dialog._current_radio.set_active(True)
        target = self.dialog.get_target()
        assert target == cons.Target.CURRENT

        self.dialog._selected_radio.set_active(True)
        target = self.dialog.get_target()
        assert target == cons.Target.SELECTED

    def test_signals(self):

        self.dialog._sub_spin_1.set_value(2)
        self.dialog._sub_spin_1.set_value(3)
        self.dialog._sub_spin_2.set_value(4)
        self.dialog._sub_spin_2.set_value(5)

    def test_run(self):

        gtklib.run(self.dialog)


class TestFrameAdjustDialog(_TestPositionAdjustDialog):

    def setup_method(self, method):

        self.page = Page()
        self.page.project = self.get_project()
        self.dialog = FrameAdjustDialog(gtk.Window(), self.page)

    def test_get_first_point(self):

        self.dialog._sub_spin_1.set_value(2)
        point = self.dialog.get_first_point()
        point == (2, self.page.project.frames[2])

    def test_get_second_point(self):

        self.dialog._sub_spin_2.set_value(2)
        point = self.dialog.get_second_point()
        point == (2, self.page.project.frames[2])


class TestTimeAdjustDialog(_TestPositionAdjustDialog):

    def setup_method(self, method):

        self.page = Page()
        self.page.project = self.get_project()
        self.dialog = TimeAdjustDialog(gtk.Window(), self.page)

    def test_get_first_point(self):

        self.dialog._sub_spin_1.set_value(2)
        point = self.dialog.get_first_point()
        point == (2, self.page.project.times[2])

    def test_get_second_point(self):

        self.dialog._sub_spin_2.set_value(2)
        point = self.dialog.get_second_point()
        point == (2, self.page.project.times[2])
