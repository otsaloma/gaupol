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


class _TestPositionTransformDialog(gaupol.TestCase):

    def run__dialog(self):

        self.dialog.run()
        self.dialog.destroy()

    def setup_method(self, method):

        self.conf = gaupol.conf.position_transform
        self.application = self.new_application()
        page = self.application.get_current_page()
        page.view.select_rows((1, 2, 3))
        gaupol.conf.preview.use_custom_command = True
        gaupol.conf.preview.custom_command = "echo"
        page.project.video_path = self.new_subrip_file()

    def test__init_sensitivities(self):

        page = self.application.get_current_page()
        page.project.video_path = None
        page.project.main_file = None
        page.view.select_rows(())
        self.conf.target = gaupol.targets.SELECTED
        args = (self.application.window, self.application)
        self.dialog = self.dialog.__class__(*args)

    def test__on_preview_button_1_clicked(self):

        self.dialog._current_radio.set_active(True)
        self.dialog._preview_button_1.emit("clicked")
        self.dialog._selected_radio.set_active(True)
        self.dialog._preview_button_1.emit("clicked")

    def test__on_preview_button_2_clicked(self):

        self.dialog._current_radio.set_active(True)
        self.dialog._preview_button_2.emit("clicked")
        self.dialog._selected_radio.set_active(True)
        self.dialog._preview_button_2.emit("clicked")

    def test__on_response(self):

        targets = gaupol.targets
        for target in (targets.SELECTED, targets.CURRENT):
            self.conf.target = target
            args = (self.application.window, self.application)
            self.dialog = self.dialog.__class__(*args)
            self.dialog.show()
            self.dialog.response(gtk.RESPONSE_OK)

    def test__on_subtitle_spin_1_value_changed(self):

        spin_button = self.dialog._subtitle_spin_1
        spin_button.spin(gtk.SPIN_STEP_FORWARD)
        spin_button.spin(gtk.SPIN_STEP_FORWARD)
        spin_button.spin(gtk.SPIN_STEP_BACKWARD)
        spin_button.spin(gtk.SPIN_STEP_BACKWARD)

    def test__on_subtitle_spin_2_value_changed(self):

        spin_button = self.dialog._subtitle_spin_2
        spin_button.spin(gtk.SPIN_STEP_FORWARD)
        spin_button.spin(gtk.SPIN_STEP_FORWARD)
        spin_button.spin(gtk.SPIN_STEP_BACKWARD)
        spin_button.spin(gtk.SPIN_STEP_BACKWARD)


class TestFrameTransformDialog(_TestPositionTransformDialog):

    def setup_method(self, method):

        _TestPositionTransformDialog.setup_method(self, method)
        args = (self.application.window, self.application)
        self.dialog = gaupol.FrameTransformDialog(*args)
        self.dialog.show()


class TestTimeTransformDialog(_TestPositionTransformDialog):

    def setup_method(self, method):

        _TestPositionTransformDialog.setup_method(self, method)
        args = (self.application.window, self.application)
        self.dialog = gaupol.TimeTransformDialog(*args)
        self.dialog.show()
