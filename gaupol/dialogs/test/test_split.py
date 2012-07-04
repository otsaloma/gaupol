# -*- coding: utf-8-unix -*-

# Copyright (C) 2006-2008,2010 Osmo Salomaa
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


class TestSplitDialog(gaupol.TestCase):

    def run_dialog(self):
        self.dialog.run()
        self.dialog.destroy()

    def setup_method(self, method):
        self.application = self.new_application()
        self.dialog = gaupol.SplitDialog(self.application.window,
                                         self.application)

        self.dialog.show()

    def test__on_response__frame_negative(self):
        page = gaupol.Page()
        page.project.open_main(self.new_microdvd_file(), "ascii")
        self.application.add_page(page)
        self.dialog = gaupol.SplitDialog(self.application.window,
                                         self.application)

        self.dialog.show()
        self.dialog._subtitle_spin.set_value(2)
        self.dialog.response(Gtk.ResponseType.OK)

    def test__on_response__frame_positive(self):
        page = gaupol.Page()
        page.project.open_main(self.new_microdvd_file(), "ascii")
        self.application.add_page(page)
        self.dialog = gaupol.SplitDialog(self.application.window,
                                         self.application)

        self.dialog.show()
        self.dialog._subtitle_spin.set_value(5)
        self.dialog.response(Gtk.ResponseType.OK)

    def test__on_response__time_negative(self):
        page = gaupol.Page()
        page.project.open_main(self.new_subrip_file(), "ascii")
        self.application.add_page(page)
        self.dialog = gaupol.SplitDialog(self.application.window,
                                         self.application)

        self.dialog.show()
        self.dialog._subtitle_spin.set_value(2)
        self.dialog.response(Gtk.ResponseType.OK)

    def test__on_response__time_positive(self):
        page = gaupol.Page()
        page.project.open_main(self.new_subrip_file(), "ascii")
        self.application.add_page(page)
        self.dialog = gaupol.SplitDialog(self.application.window,
                                         self.application)

        self.dialog.show()
        self.dialog._subtitle_spin.set_value(5)
        self.dialog.response(Gtk.ResponseType.OK)
