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
from .. import shift


class _Test_PositionShiftDialog(unittest.TestCase):

    # pylint: disable-msg=E1101

    def run(self):

        self.dialog.run()
        self.dialog.destroy()

    def test__get_preview_row(self):

        page = self.application.get_current_page()
        row = self.dialog._get_preview_row()
        assert 0 <= row < len(page.project.subtitles)

    def test__get_target(self):

        TARGET = gaupol.gtk.TARGET
        target = self.dialog._get_target()
        assert target in (TARGET.SELECTED, TARGET.CURRENT)

    def test__on_response(self):

        self.dialog._amount_spin.spin(gtk.SPIN_STEP_FORWARD)
        self.dialog.response(gtk.RESPONSE_OK)

    def test__shift_positions(self):

        self.dialog._amount_spin.spin(gtk.SPIN_STEP_FORWARD)
        self.dialog._shift_positions()


class TestFrameShiftDialog(_Test_PositionShiftDialog):

    def setup_method(self, method):

        self.application = self.get_application()
        args = (self.application.window, self.application)
        self.dialog = shift.FrameShiftDialog(*args)

    def test__get_amount(self):

        self.dialog._get_amount()


class TestTimeShiftDialog(_Test_PositionShiftDialog):

    def setup_method(self, method):

        self.application = self.get_application()
        args = (self.application.window, self.application)
        self.dialog = shift.TimeShiftDialog(*args)

    def test__get_amount(self):

        self.dialog._get_amount()
