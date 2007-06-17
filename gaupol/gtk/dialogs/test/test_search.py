# Copyright (C) 2006-2007 Osmo Salomaa
#
# This file is part of Gaupol.
#
# Gaupol is free software; you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.
#
# Gaupol is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# Gaupol; if not, write to the Free Software Foundation, Inc., 51 Franklin
# Street, Fifth Floor, Boston, MA 02110-1301, USA.


import functools
import gaupol.gtk
import gtk

from gaupol.gtk import unittest
from .. import search


class TestSearchDialog(unittest.TestCase):

    def run(self):

        self.dialog.run()
        self.dialog.destroy()

    def run__show_regex_error_dialog_pattern(self):

        self.dialog = search.SearchDialog(self.get_application())
        self.dialog._show_regex_error_dialog_pattern("test")

    def run__show_regex_error_dialog_replacement(self):

        self.dialog = search.SearchDialog(self.get_application())
        self.dialog._show_regex_error_dialog_replacement("test")

    @gaupol.gtk.util.asserted_return
    def setup_method(self, method):

        assert not hasattr(self, "application")
        self.application = self.get_application()
        self.dialog = search.SearchDialog(self.application)
        self.dialog.show()
        respond = lambda *args: gtk.RESPONSE_DELETE_EVENT
        self.dialog.flash_dialog = respond
        self.dialog.run_dialog = respond

    def test__on_ignore_case_check_toggled(self):

        self.dialog._ignore_case_check.set_active(True)
        self.dialog._ignore_case_check.set_active(False)

    def test__on_next_button_clicked(self):

        self.dialog._pattern_entry.set_text("a")
        self.dialog._on_next_button_clicked()

    def test__on_pattern_entry_changed(self):

        self.dialog._pattern_entry.set_text("a")
        self.dialog._pattern_entry.set_text("")

    def test__on_previous_button_clicked(self):

        self.dialog._pattern_entry.set_text("a")
        self.dialog._on_previous_button_clicked()

    def test__on_regex_check_toggled(self):

        self.dialog._regex_check.set_active(True)
        self.dialog._regex_check.set_active(False)

    def test__on_replace_all_button_clicked(self):

        self.dialog._pattern_entry.set_text("e")
        self.dialog._replacement_entry.set_text("x")
        self.dialog._on_replace_all_button_clicked()

    def test__on_replace_button_clicked(self):

        self.dialog._pattern_entry.set_text("a")
        self.dialog._replacement_entry.set_text("x")
        self.dialog._next_button.emit("clicked")
        self.dialog._on_replace_button_clicked()

    def test__on_response(self):

        self.dialog.response(gtk.RESPONSE_HELP)

    def test__on_show(self):

        self.dialog.show()

    def test__on_text_view_focus_out_event(self):

        self.dialog._pattern_entry.set_text("a")
        self.dialog._on_next_button_clicked()
        self.dialog._on_next_button_clicked()

    def test__show_regex_error_dialog_pattern(self):

        self.dialog._show_regex_error_dialog_pattern("test")

    def test__show_regex_error_dialog_replacement(self):

        self.dialog._show_regex_error_dialog_replacement("test")

    def test_next(self):

        self.dialog._regex_check.set_active(True)
        self.dialog._pattern_entry.set_text("^")
        for i in range(10):
            self.dialog.next()

    def test_previous(self):

        self.dialog._regex_check.set_active(True)
        self.dialog._pattern_entry.set_text("$")
        for i in range(10):
            self.dialog.previous()

    def test_replace(self):

        self.dialog._regex_check.set_active(True)
        self.dialog._pattern_entry.set_text(" ")
        self.dialog._replacement_entry.set_text(".")
        self.dialog.next()
        for i in range(10):
            self.dialog.replace()

    def test_replace_all(self):

        self.dialog._regex_check.set_active(True)
        self.dialog._pattern_entry.set_text("^")
        self.dialog._replacement_entry.set_text("-")
        self.dialog.replace_all()
