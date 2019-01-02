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


class TestOpenAgent(gaupol.TestCase):

    def run__show_encoding_error_dialog(self):
        self.delegate._show_encoding_error_dialog("test")

    def run__show_format_error_dialog(self):
        self.delegate._show_format_error_dialog("test")

    def run__show_io_error_dialog(self):
        self.delegate._show_io_error_dialog("test", "test")

    def run__show_parse_error_dialog(self):
        self.delegate._show_parse_error_dialog("test", aeidon.formats.SUBRIP)

    @aeidon.deco.silent(gaupol.Default)
    def run__show_size_warning_dialog(self):
        self.delegate._show_size_warning_dialog("test", 2)

    @aeidon.deco.silent(gaupol.Default)
    def run__show_sort_warning_dialog(self):
        self.delegate._show_sort_warning_dialog("test", 3)

    @aeidon.deco.silent(gaupol.Default)
    def run__show_translation_warning_dialog(self):
        page = self.application.get_current_page()
        self.delegate._show_translation_warning_dialog(page)

    def setup_method(self, method):
        self.application = self.new_application()
        self.delegate = self.application.open_main.__self__

    def test_add_to_recent_files(self):
        self.application.add_to_recent_files(self.new_subrip_file(),
                                             aeidon.formats.SUBRIP,
                                             aeidon.documents.MAIN)

    def test_append_file(self):
        page = self.application.get_current_page()
        n = len(page.project.subtitles)
        self.application.append_file(self.new_subrip_file())
        assert len(page.project.subtitles) > n

    def test__on_new_project_activate(self):
        n = len(self.application.pages)
        self.application.get_action("new-project").activate()
        assert len(self.application.pages) == n + 1

    @patch("gaupol.util.flash_dialog", lambda *args: Gtk.ResponseType.OK)
    def test__on_split_project_activate(self):
        page = self.application.get_current_page()
        page.view.select_rows((3,))
        self.application.get_action("split-project").activate()

    def test_open_main(self):
        n = len(self.application.pages)
        path = self.new_subrip_file()
        self.application.open_main(path)
        assert len(self.application.pages) == n + 1

    def test_open_translation(self):
        path = self.new_subrip_file()
        self.application.open_translation(path)
