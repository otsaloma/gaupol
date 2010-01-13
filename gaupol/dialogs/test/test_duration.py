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


class TestDurationAdjustDialog(gaupol.TestCase):

    def run__dialog(self):

        self.dialog.run()
        self.dialog.destroy()

    def setup_method(self, method):

        self.conf = gaupol.conf.duration_adjust
        self.application = self.get_application()
        page = self.application.get_current_page()
        page.view.select_rows((1, 2, 3))
        args = (self.application.window, self.application)
        self.dialog = gaupol.DurationAdjustDialog(*args)
        self.dialog.show()

    def test__init_sensitivities(self):

        page = self.application.get_current_page()
        page.view.select_rows(())
        self.conf.target = gaupol.targets.SELECTED
        args = (self.application.window, self.application)
        self.dialog = gaupol.DurationAdjustDialog(*args)

    def test__on_gap_check_toggled(self):

        self.dialog._gap_check.set_active(True)
        self.dialog._gap_check.set_active(False)
        self.dialog._gap_check.set_active(True)

    def test__on_lengthen_check_toggled(self):

        self.dialog._lengthen_check.set_active(True)
        self.dialog._lengthen_check.set_active(False)
        self.dialog._lengthen_check.set_active(True)

    def test__on_max_check_toggled(self):

        self.dialog._max_check.set_active(True)
        self.dialog._max_check.set_active(False)
        self.dialog._max_check.set_active(True)

    def test__on_min_check_toggled(self):

        self.dialog._min_check.set_active(True)
        self.dialog._min_check.set_active(False)
        self.dialog._min_check.set_active(True)

    def test__on_response(self):

        for target in gaupol.targets:
            self.conf.target = target
            args = (self.application.window, self.application)
            self.dialog = gaupol.DurationAdjustDialog(*args)
            self.dialog.response(gtk.RESPONSE_OK)

    def test__on_shorten_check_toggled(self):

        self.dialog._shorten_check.set_active(True)
        self.dialog._shorten_check.set_active(False)
        self.dialog._shorten_check.set_active(True)
