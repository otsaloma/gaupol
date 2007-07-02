# Copyright (C) 2005-2007 Osmo Salomaa
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
from .. import transform


class _Test_PositionTransformDialog(unittest.TestCase):

    # pylint: disable-msg=E1101

    def run(self):

        self.dialog.run()
        self.dialog.destroy()

    def test__get_target(self):

        TARGET = gaupol.gtk.TARGET
        target = self.dialog._get_target()
        assert target in (TARGET.SELECTED, TARGET.CURRENT)

    def test__on_response(self):

        self.dialog.response(gtk.RESPONSE_OK)

    def test__transform_positions(self):

        self.dialog._transform_positions()


class TestFrameTransformDialog(_Test_PositionTransformDialog):

    def setup_method(self, method):

        self.application = self.get_application()
        args = (self.application.window, self.application)
        self.dialog = transform.FrameTransformDialog(*args)

    def test__get_first_point(self):

        self.dialog._get_first_point()

    def test__get_second_point(self):

        self.dialog._get_second_point()

    def test__on_subtitle_spin_1_value_changed(self):

        self.dialog._subtitle_spin_1.spin(gtk.SPIN_STEP_FORWARD)
        self.dialog._subtitle_spin_1.spin(gtk.SPIN_STEP_FORWARD)
        self.dialog._subtitle_spin_1.spin(gtk.SPIN_STEP_BACKWARD)
        self.dialog._subtitle_spin_1.spin(gtk.SPIN_STEP_BACKWARD)

    def test__on_subtitle_spin_2_value_changed(self):

        self.dialog._subtitle_spin_2.spin(gtk.SPIN_STEP_FORWARD)
        self.dialog._subtitle_spin_2.spin(gtk.SPIN_STEP_FORWARD)
        self.dialog._subtitle_spin_2.spin(gtk.SPIN_STEP_BACKWARD)
        self.dialog._subtitle_spin_2.spin(gtk.SPIN_STEP_BACKWARD)


class TestTimeTransformDialog(_Test_PositionTransformDialog):

    def setup_method(self, method):

        self.application = self.get_application()
        args = (self.application.window, self.application)
        self.dialog = transform.TimeTransformDialog(*args)

    def test__get_first_point(self):

        self.dialog._get_first_point()

    def test__get_second_point(self):

        self.dialog._get_second_point()

    def test__on_subtitle_spin_1_value_changed(self):

        self.dialog._subtitle_spin_1.spin(gtk.SPIN_STEP_FORWARD)
        self.dialog._subtitle_spin_1.spin(gtk.SPIN_STEP_FORWARD)
        self.dialog._subtitle_spin_1.spin(gtk.SPIN_STEP_BACKWARD)
        self.dialog._subtitle_spin_1.spin(gtk.SPIN_STEP_BACKWARD)

    def test__on_subtitle_spin_2_value_changed(self):

        self.dialog._subtitle_spin_2.spin(gtk.SPIN_STEP_FORWARD)
        self.dialog._subtitle_spin_2.spin(gtk.SPIN_STEP_FORWARD)
        self.dialog._subtitle_spin_2.spin(gtk.SPIN_STEP_BACKWARD)
        self.dialog._subtitle_spin_2.spin(gtk.SPIN_STEP_BACKWARD)
