# Copyright (C) 2005-2007 Osmo Salomaa
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


import gtk

from gaupol.gtk.unittest import TestCase
from .. import spellcheck


class TestSpellCheckDialog(TestCase):

    def run(self):

        self.dialog.run()
        self.dialog.destroy()

    def setup_method(self, method):

        self.application = self.get_application()
        for page in self.application.pages:
            for i, text in enumerate(page.project.main_texts):
                page.project.main_texts[i] = text.replace("a", "x")
        parent = self.application.window
        self.dialog = spellcheck.SpellCheckDialog(parent, self.application)
        self.dialog.show()

    def test__get_target_pages(self):

        pages = self.dialog._get_target_pages()
        assert isinstance(pages, list)

    def test__on_add_button_clicked(self):

        pass

    def test__on_check_button_clicked(self):

        self.dialog._entry.set_text("test")
        self.dialog._check_button.emit("clicked")

    def test__on_edit_button_clicked(self):

        respond = lambda *args: gtk.RESPONSE_OK
        self.dialog.run_dialog = respond
        self.dialog._edit_button.emit("clicked")

    def test__on_entry_changed(self):

        self.dialog._entry.set_text("test")

    def test__on_ignore_all_button_clicked(self):

        self.dialog._ignore_button.emit("clicked")

    def test__on_ignore_button_clicked(self):

        self.dialog._ignore_all_button.emit("clicked")

    def test__on_join_back_button_clicked(self):

        pass

    def test__on_join_forward_button_clicked(self):

        pass

    def test__on_replace_all_button_clicked(self):

        self.dialog._replace_all_button.emit("clicked")

    def test__on_replace_button_clicked(self):

        self.dialog._replace_button.emit("clicked")

    def test__on_response(self):

        self.dialog.response(gtk.RESPONSE_CLOSE)

    def test__on_tree_view_selection_changed(self):

        pass

    def test__register_changes(self):

        self.dialog._register_changes()

    def test__set_done(self):

        self.dialog._set_done()

    def test__show_error_dialog(self):

        respond = lambda *args: gtk.RESPONSE_OK
        self.dialog.flash_dialog = respond
        self.dialog._show_error_dialog("test")

    def test__store_replacement(self):

        pass

    def test__write_replacements(self):

        pass

