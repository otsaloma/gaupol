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
from .. import posshift


class _Test_PositionShiftDialog(TestCase):

    # pylint: disable-msg=E1101

    def run(self):

        self.dialog.run()
        self.dialog.destroy()

    def test__get_preview_row(self):

        row = self.dialog._get_preview_row()
        assert isinstance(row, int)

    def test__get_target(self):

        target = self.dialog._get_target()
        assert target in (cons.TARGET.SELECTED, cons.TARGET.CURRENT)

    def test__get_target_rows(self):

        rows = self.dialog._get_target_rows()
        if rows is not None:
            assert isinstance(rows, list)

    def test__on_response(self):

        self.dialog.response(gtk.RESPONSE_OK)

    def test__shift(self):

        amount = self.dialog._get_amount()
        self.dialog._shift(amount)


class TestFrameShiftDialog(_Test_PositionShiftDialog):

    def setup_method(self, method):

        self.application = self.get_application()
        parent = self.application.window
        self.dialog = posshift.FrameShiftDialog(parent, self.application)
        self.dialog.show()

    def test__get_amount(self):

        amount = self.dialog._get_amount()
        assert isinstance(amount, int)

    def test__get_shift_method(self):

        method = self.dialog._get_shift_method()
        assert callable(method)


class TestTimeShiftDialog(_Test_PositionShiftDialog):

    def setup_method(self, method):

        self.application = self.get_application()
        parent = self.application.window
        self.dialog = posshift.TimeShiftDialog(parent, self.application)
        self.dialog.show()

    def test__get_amount(self):

        amount = self.dialog._get_amount()
        assert isinstance(amount, float)

    def test__get_shift_method(self):

        method = self.dialog._get_shift_method()
        assert callable(method)
