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


class TestSearchDialog(gaupol.TestCase):

    def run_dialog(self):
        self.dialog.run()
        self.dialog.destroy()

    def run__show_regex_error_dialog_pattern(self):
        self.dialog._show_regex_error_dialog_pattern("test")

    def run__show_regex_error_dialog_replacement(self):
        self.dialog._show_regex_error_dialog_replacement("test")

    def setup_method(self, method):
        self.application = self.new_application()
        self.dialog = gaupol.SearchDialog(
            self.application.window, self.application)
        self.dialog.show()

    def test_next(self):
        self.dialog._regex_check.set_active(True)
        for char in "aeiouy":
            self.dialog._pattern_entry.set_text(char)
            self.dialog.next()
            self.dialog.next()

    def test__on_application_page_changed(self):
        # Ensure that editing obsolete data is not possible.
        # https://bugzilla.gnome.org/show_bug.cgi?id=572676
        self.dialog._pattern_entry.set_text("a")
        self.dialog.next()
        page = self.application.get_current_page()
        page.project.remove_subtitles((self.dialog._match_row,))
        assert not self.dialog._text_view.get_sensitive()
        assert not self.dialog._replace_button.get_sensitive()

    def test__on_response(self):
        self.dialog.response(Gtk.ResponseType.HELP)

    def test_previous(self):
        self.dialog._regex_check.set_active(True)
        for char in "aeiouy":
            self.dialog._pattern_entry.set_text(char)
            self.dialog.previous()
            self.dialog.previous()

    def test_replace(self):
        self.dialog._regex_check.set_active(True)
        for char in "aeiouy":
            self.dialog._pattern_entry.set_text(char)
            self.dialog._replacement_entry.set_text("x")
            self.dialog.next()
            self.dialog.replace()
            self.dialog.replace()

    def test_replace_all(self):
        self.dialog._regex_check.set_active(True)
        self.dialog._pattern_entry.set_text("^")
        self.dialog._replacement_entry.set_text("-")
        self.dialog.replace_all()
