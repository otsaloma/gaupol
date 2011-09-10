# Copyright (C) 2005-2008,2010 Osmo Salomaa
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
from gi.repository import Gtk


class _TestPositionTransformDialog(gaupol.TestCase):

    def run__dialog(self):
        self.dialog.run()
        self.dialog.destroy()

    def setup_method(self, method):
        self.application = self.new_application()
        page = self.application.get_current_page()
        page.view.select_rows((1, 2, 3))
        gaupol.conf.preview.use_custom_command = True
        gaupol.conf.preview.custom_command = "echo"
        page.project.video_path = self.new_subrip_file()

    def test__init____no(self):
        # pylint: disable=W0201
        page = self.application.get_current_page()
        page.project.video_path = None
        page.project.main_file = None
        page.view.select_rows(())
        gaupol.conf.position_transform.target = gaupol.targets.SELECTED
        self.dialog = self.dialog.__class__(self.application.window,
                                            self.application)

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

    def test__on_response__current(self):
        self.dialog._current_radio.set_active(True)
        self.dialog.response(Gtk.ResponseType.OK)

    def test__on_response__selected(self):
        self.dialog._selected_radio.set_active(True)
        self.dialog.response(Gtk.ResponseType.OK)

    def test__on_subtitle_spin_1_value_changed(self):
        self.dialog._subtitle_spin_1.spin(Gtk.SPIN_STEP_FORWARD)
        self.dialog._subtitle_spin_1.spin(Gtk.SPIN_STEP_FORWARD)
        self.dialog._subtitle_spin_1.spin(Gtk.SPIN_STEP_BACKWARD)
        self.dialog._subtitle_spin_1.spin(Gtk.SPIN_STEP_BACKWARD)

    def test__on_subtitle_spin_2_value_changed(self):
        self.dialog._subtitle_spin_2.spin(Gtk.SPIN_STEP_FORWARD)
        self.dialog._subtitle_spin_2.spin(Gtk.SPIN_STEP_FORWARD)
        self.dialog._subtitle_spin_2.spin(Gtk.SPIN_STEP_BACKWARD)
        self.dialog._subtitle_spin_2.spin(Gtk.SPIN_STEP_BACKWARD)


class TestFrameTransformDialog(_TestPositionTransformDialog):

    def setup_method(self, method):
        _TestPositionTransformDialog.setup_method(self, method)
        self.dialog = gaupol.FrameTransformDialog(self.application.window,
                                                  self.application)

        self.dialog.show()


class TestTimeTransformDialog(_TestPositionTransformDialog):

    def setup_method(self, method):
        _TestPositionTransformDialog.setup_method(self, method)
        self.dialog = gaupol.TimeTransformDialog(self.application.window,
                                                 self.application)

        self.dialog.show()
