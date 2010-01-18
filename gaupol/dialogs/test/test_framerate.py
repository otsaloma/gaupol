# Copyright (C) 2005-2008 Osmo Salomaa
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
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# Gaupol. If not, see <http://www.gnu.org/licenses/>.

import gaupol
import gtk


class TestFramerateConversionDialog(gaupol.TestCase):

    def run__dialog(self):

        self.dialog.run()
        self.dialog.destroy()

    def setup_method(self, method):

        self.conf = gaupol.conf.framerate_convert
        self.application = self.new_application()
        args = (self.application.window, self.application)
        self.dialog = gaupol.FramerateConvertDialog(*args)
        self.dialog.show()

    def test__on_input_combo_changed(self):

        for framerate in aeidon.framerates:
            self.dialog._input_combo.set_active(framerate)

    def test__on_output_combo_changed(self):

        for framerate in aeidon.framerates:
            self.dialog._output_combo.set_active(framerate)

    def test__on_response(self):

        targets = gaupol.targets
        for target in (targets.CURRENT, targets.ALL):
            self.conf.target = target
            args = (self.application.window, self.application)
            self.dialog = gaupol.FramerateConvertDialog(*args)
            self.dialog._input_combo.set_active(0)
            self.dialog._output_combo.set_active(1)
            self.dialog.response(gtk.RESPONSE_OK)
