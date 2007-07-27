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
from .. import framerate


class TestFramerateConversionDialog(unittest.TestCase):

    def run(self):

        self.dialog.run()
        self.dialog.destroy()

    def setup_method(self, method):

        self.application = self.get_application()
        args = (self.application.window, self.application)
        self.dialog = framerate.FramerateConvertDialog(*args)

    def test__convert_framerates(self):

        self.dialog._input_combo.set_active(0)
        self.dialog._output_combo.set_active(1)
        self.dialog._convert_framerates()

    def test__get_target(self):

        TARGET = gaupol.gtk.TARGET
        target = self.dialog._get_target()
        assert target in (TARGET.SELECTED, TARGET.CURRENT)

    def test__on_input_combo_changed(self):

        self.dialog._input_combo.set_active(0)
        self.dialog._input_combo.set_active(1)
        self.dialog._input_combo.set_active(2)

    def test__on_output_combo_changed(self):

        self.dialog._output_combo.set_active(0)
        self.dialog._output_combo.set_active(1)
        self.dialog._output_combo.set_active(2)

    def test__on_response(self):

        self.dialog._input_combo.set_active(0)
        self.dialog._output_combo.set_active(1)
        self.dialog.response(gtk.RESPONSE_OK)
