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

from gaupol.gtk import cons
from gaupol.gtk.unittest import TestCase
from .. import posadjust


class _Test_PositionAdjustDialog(TestCase):

    # pylint: disable-msg=E1101

    def run(self):

        self.dialog.run()
        self.dialog.destroy()

    def test__adjust(self):

        self.dialog._adjust()

    def test__get_target(self):

        target = self.dialog._get_target()
        assert target in (cons.TARGET.SELECTED, cons.TARGET.CURRENT)

    def test__get_target_rows(self):

        rows = self.dialog._get_target_rows()
        if rows is not None:
            assert isinstance(rows, list)

    def test__on_response(self):

        self.dialog.response(gtk.RESPONSE_OK)


class TestFrameAdjustDialog(_Test_PositionAdjustDialog):

    def setup_method(self, method):

        self.application = self.get_application()
        parent = self.application.window
        self.dialog = posadjust.FrameAdjustDialog(parent, self.application)
        self.dialog.show()

    def test__get_adjust_method(self):

        method = self.dialog._get_adjust_method()
        assert callable(method)

    def test__get_first_point(self):

        row, frame = self.dialog._get_first_point()
        assert isinstance(row, int)
        assert isinstance(frame, int)

    def test__get_second_point(self):

        row, frame = self.dialog._get_second_point()
        assert isinstance(row, int)
        assert isinstance(frame, int)

    def test__on_sub_spin_1_value_changed(self):

        self.dialog._sub_spin_1.spin(gtk.SPIN_STEP_FORWARD)
        self.dialog._sub_spin_1.spin(gtk.SPIN_STEP_FORWARD)
        self.dialog._sub_spin_1.spin(gtk.SPIN_STEP_BACKWARD)
        self.dialog._sub_spin_1.spin(gtk.SPIN_STEP_BACKWARD)

    def test__on_sub_spin_2_value_changed(self):

        self.dialog._sub_spin_2.spin(gtk.SPIN_STEP_FORWARD)
        self.dialog._sub_spin_2.spin(gtk.SPIN_STEP_FORWARD)
        self.dialog._sub_spin_2.spin(gtk.SPIN_STEP_BACKWARD)
        self.dialog._sub_spin_2.spin(gtk.SPIN_STEP_BACKWARD)


class TestTimeAdjustDialog(_Test_PositionAdjustDialog):

    def setup_method(self, method):

        self.application = self.get_application()
        parent = self.application.window
        self.dialog = posadjust.TimeAdjustDialog(parent, self.application)
        self.dialog.show()

    def test__get_adjust_method(self):

        method = self.dialog._get_adjust_method()
        assert callable(method)

    def test__get_first_point(self):

        row, time = self.dialog._get_first_point()
        assert isinstance(row, int)
        assert isinstance(time, basestring)

    def test__get_second_point(self):

        row, time = self.dialog._get_second_point()
        assert isinstance(row, int)
        assert isinstance(time, basestring)

    def test__on_sub_spin_1_value_changed(self):

        self.dialog._sub_spin_1.spin(gtk.SPIN_STEP_FORWARD)
        self.dialog._sub_spin_1.spin(gtk.SPIN_STEP_FORWARD)
        self.dialog._sub_spin_1.spin(gtk.SPIN_STEP_BACKWARD)
        self.dialog._sub_spin_1.spin(gtk.SPIN_STEP_BACKWARD)

    def test__on_sub_spin_2_value_changed(self):

        self.dialog._sub_spin_2.spin(gtk.SPIN_STEP_FORWARD)
        self.dialog._sub_spin_2.spin(gtk.SPIN_STEP_FORWARD)
        self.dialog._sub_spin_2.spin(gtk.SPIN_STEP_BACKWARD)
        self.dialog._sub_spin_2.spin(gtk.SPIN_STEP_BACKWARD)
