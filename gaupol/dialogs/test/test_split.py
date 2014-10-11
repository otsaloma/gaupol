# -*- coding: utf-8 -*-

# Copyright (C) 2006 Osmo Salomaa
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import gaupol

from gi.repository import Gtk


class TestSplitDialog(gaupol.TestCase):

    def run_dialog(self):
        self.dialog.run()
        self.dialog.destroy()

    def setup_method(self, method):
        self.application = self.new_application()
        self.dialog = gaupol.SplitDialog(
            self.application.window, self.application)
        self.dialog.show()

    def test__on_response(self):
        npages = len(self.application.pages)
        self.dialog.show()
        self.dialog._subtitle_spin.set_value(5)
        self.dialog.response(Gtk.ResponseType.OK)
        assert len(self.application.pages) == npages + 1
