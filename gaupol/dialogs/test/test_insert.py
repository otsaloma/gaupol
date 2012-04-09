# -*- coding: utf-8-unix -*-

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


class TestInsertDialog(gaupol.TestCase):

    def run__dialog(self):
        self.dialog.run()
        self.dialog.destroy()

    def setup_method(self, method):
        self.application = self.new_application()
        page = self.application.get_current_page()
        page.view.select_rows((2,))
        self.dialog = gaupol.InsertDialog(self.application.window,
                                          self.application)

        self.dialog.show()

    def test__on_response(self):
        self.dialog.response(Gtk.ResponseType.OK)

    def test__on_response__no_subtitles(self):
        page = self.application.get_current_page()
        page.project.remove_subtitles(list(range(len(page.project.subtitles))))
        self.dialog.response(Gtk.ResponseType.OK)
