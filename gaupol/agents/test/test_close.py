# -*- coding: utf-8 -*-

# Copyright (C) 2005 Osmo Salomaa
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

import aeidon
import gaupol

from gi.repository import Gtk
from unittest.mock import patch


class TestCloseAgent(gaupol.TestCase):

    def run__confirm_close_both(self):
        page = self.application.get_current_page()
        page.project.remove_subtitles((0,))
        with aeidon.util.silent(gaupol.Default):
            self.application.close(page)

    def run__confirm_close_main(self):
        page = self.application.get_current_page()
        page.project.set_text(0, aeidon.documents.MAIN, "")
        with aeidon.util.silent(gaupol.Default):
            self.application.close(page)

    def run__confirm_close_translation(self):
        page = self.application.get_current_page()
        page.project.set_text(0, aeidon.documents.TRAN, "")
        with aeidon.util.silent(gaupol.Default):
            self.application.close(page)

    def setup_method(self, method):
        self.application = self.new_application()

    @patch("gaupol.util.flash_dialog", lambda *args: Gtk.ResponseType.CANCEL)
    @aeidon.deco.silent(gaupol.Default)
    def test_close(self):
        self.application.pages[-1].project.remove_subtitles((0,))
        self.application.close(self.application.pages[-1], confirm=True)

    @patch("gaupol.util.flash_dialog", lambda *args: Gtk.ResponseType.NO)
    @aeidon.deco.silent(gaupol.Default)
    def test_close_all(self):
        for page in self.application.pages:
            page.project.remove_subtitles((0,))
        self.application.close_all()
