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

import gaupol.gtk
import gtk


class _TestPositionShiftDialog(gaupol.gtk.TestCase):

    # pylint: disable-msg=E1101,W0201

    def run__dialog(self):

        self.dialog.run()
        self.dialog.destroy()

    def setup_method(self, method):

        self.conf = gaupol.gtk.conf.position_shift
        self.application = self.get_application()
        page = self.application.get_current_page()
        page.view.select_rows((1, 2, 3))
        gaupol.gtk.conf.preview.use_custom = True
        gaupol.gtk.conf.preview.custom_command = "echo"
        page.project.video_path = self.get_subrip_path()

    def test__init_values(self):

        page = self.application.get_current_page()
        page.project.video_path = None
        page.project.main_file = None
        page.view.select_rows(())
        self.conf.target = gaupol.gtk.targets.SELECTED
        args = (self.application.window, self.application)
        self.dialog = self.dialog.__class__(*args)

    def test__on_preview_button_clicked(self):

        self.dialog._amount_spin.spin(gtk.SPIN_STEP_FORWARD)
        self.dialog._current_radio.set_active(True)
        self.dialog._preview_button.emit("clicked")
        self.dialog._selected_radio.set_active(True)
        self.dialog._preview_button.emit("clicked")

    def test__on_response(self):

        for target in gaupol.gtk.targets:
            self.conf.target = target
            args = (self.application.window, self.application)
            self.dialog = self.dialog.__class__(*args)
            self.dialog.show()
            self.dialog._amount_spin.spin(gtk.SPIN_STEP_FORWARD)
            self.dialog.response(gtk.RESPONSE_OK)


class TestFrameShiftDialog(_TestPositionShiftDialog):

    def setup_method(self, method):

        _TestPositionShiftDialog.setup_method(self, method)
        args = (self.application.window, self.application)
        self.dialog = gaupol.gtk.FrameShiftDialog(*args)
        self.dialog.show()


class TestTimeShiftDialog(_TestPositionShiftDialog):

    def setup_method(self, method):

        _TestPositionShiftDialog.setup_method(self, method)
        args = (self.application.window, self.application)
        self.dialog = gaupol.gtk.TimeShiftDialog(*args)
        self.dialog.show()
