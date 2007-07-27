# Copyright (C) 2005-2007 Osmo Salomaa
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
# A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# Gaupol.  If not, see <http://www.gnu.org/licenses/>.

import gaupol.gtk
import gtk

from gaupol.gtk import unittest
from .. import spellcheck


class TestSpellCheckDialog(unittest.TestCase):

    def run(self):

        self.dialog.run()
        self.dialog.destroy()

    def run__show_error_dialog(self):

        self.dialog._show_error_dialog("test")

    def setup_method(self, method):

        self.application = self.get_application()
        for page in self.application.pages:
            for i, subtitle in enumerate(page.project.subtitles):
                text = subtitle.main_text.replace("a", "x")
                page.project.set_text(i, gaupol.gtk.DOCUMENT.MAIN, text)
                text = subtitle.tran_text.replace("a", "x")
                page.project.set_text(i, gaupol.gtk.DOCUMENT.TRAN, text)
        parent = self.application.window
        self.dialog = spellcheck.SpellCheckDialog(parent, self.application)

    def test__on_edit_button_clicked(self):

        respond = lambda *args: gtk.RESPONSE_OK
        self.dialog.run_dialog = respond
        self.dialog._edit_button.emit("clicked")

    def test__on_entry_changed(self):

        self.dialog._entry.set_text("t")
        self.dialog._entry.set_text("te")
        self.dialog._entry.set_text("tes")
        self.dialog._entry.set_text("test")

    def test__on_ignore_all_button_clicked(self):

        self.dialog._ignore_button.emit("clicked")

    def test__on_ignore_button_clicked(self):

        self.dialog._ignore_all_button.emit("clicked")

    def test__on_replace_all_button_clicked(self):

        self.dialog._replace_all_button.emit("clicked")

    def test__on_replace_button_clicked(self):

        self.dialog._replace_button.emit("clicked")

    def test__on_response(self):

        self.dialog.response(gtk.RESPONSE_CLOSE)

    def test__on_tree_view_selection_changed(self):

        store = self.dialog._tree_view.get_model()
        selection = self.dialog._tree_view.get_selection()
        for i in range(len(store)):
            selection.select_path(i)

    def test__show_error_dialog(self):

        respond = lambda *args: gtk.RESPONSE_OK
        self.dialog.flash_dialog = respond
        self.dialog._show_error_dialog("test")
