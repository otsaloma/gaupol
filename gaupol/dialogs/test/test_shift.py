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


class _TestPositionShiftDialog(gaupol.TestCase):

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
        gaupol.conf.position_shift.target = gaupol.targets.SELECTED
        self.dialog = self.dialog.__class__(self.application.window,
                                            self.application)

    def test__on_amount_spin_value_changed(self):
        self.dialog._amount_spin.spin(Gtk.SPIN_STEP_FORWARD)
        self.dialog._amount_spin.spin(Gtk.SPIN_STEP_FORWARD)
        self.dialog._amount_spin.spin(Gtk.SPIN_STEP_BACKWARD)
        self.dialog._amount_spin.spin(Gtk.SPIN_STEP_BACKWARD)

    def test__on_preview_button_clicked__0(self):
        self.dialog._amount_spin.spin(Gtk.SPIN_STEP_FORWARD)
        self.dialog._current_radio.set_active(True)
        self.dialog._preview_button.emit("clicked")

    def test__on_preview_button_clicked__selection(self):
        self.dialog._amount_spin.spin(Gtk.SPIN_STEP_FORWARD)
        self.dialog._selected_radio.set_active(True)
        self.dialog._preview_button.emit("clicked")

    def test__on_response__all(self):
        self.dialog._all_radio.set_active(True)
        self.dialog._amount_spin.spin(Gtk.SPIN_STEP_FORWARD)
        self.dialog.response(Gtk.ResponseType.OK)

    def test__on_response__current(self):
        self.dialog._current_radio.set_active(True)
        self.dialog._amount_spin.spin(Gtk.SPIN_STEP_FORWARD)
        self.dialog.response(Gtk.ResponseType.OK)

    def test__on_response__selected(self):
        self.dialog._selected_radio.set_active(True)
        self.dialog._amount_spin.spin(Gtk.SPIN_STEP_FORWARD)
        self.dialog.response(Gtk.ResponseType.OK)


class TestFrameShiftDialog(_TestPositionShiftDialog):

    def setup_method(self, method):
        _TestPositionShiftDialog.setup_method(self, method)
        self.dialog = gaupol.FrameShiftDialog(self.application.window,
                                              self.application)

        self.dialog.show()


class TestTimeShiftDialog(_TestPositionShiftDialog):

    def setup_method(self, method):
        _TestPositionShiftDialog.setup_method(self, method)
        self.dialog = gaupol.TimeShiftDialog(self.application.window,
                                             self.application)

        self.dialog.show()
