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
import os


class TestSpellCheckDialog(gaupol.TestCase):

    def run__dialog(self):

        self.dialog.run()
        self.dialog.destroy()

    def run__show_error_dialog(self):

        self.dialog._show_error_dialog("test")

    def setup_method(self, method):

        gaupol.conf.editor.use_custom_font = True
        gaupol.conf.editor.custom_font = "sans"
        self.application = self.get_application()
        for page in self.application.pages:
            for i, subtitle in enumerate(page.project.subtitles):
                text = subtitle.main_text.replace("a", "x")
                page.project.set_text(i, aeidon.documents.MAIN, text)
                text = subtitle.tran_text.replace("a", "x")
                page.project.set_text(i, aeidon.documents.TRAN, text)
        self._temp_dir = aeidon.temp.create_directory()
        gaupol.SpellCheckDialog._personal_dir = self._temp_dir
        args = (self.application.window, self.application)
        self.dialog = gaupol.SpellCheckDialog(*args)
        self.dialog.show()

    def teardown_method(self, method):

        aeidon.temp.remove_directory(self._temp_dir)
        gaupol.TestCase.teardown_method(self, method)

    def test__init_checker__enchant_error(self):

        gaupol.conf.spell_check.language = "wo"
        cls = gaupol.SpellCheckDialog
        respond = lambda *args: gtk.RESPONSE_OK
        cls.flash_dialog = respond
        args = (self.application.window, self.application)
        self.raises(ValueError, cls, *args)

    def test__init_checker__io_error(self):

        os.chmod(self._temp_dir, 0000)
        args = (self.application.window, self.application)
        self.dialog = gaupol.SpellCheckDialog(*args)
        os.chmod(self._temp_dir, 0777)

    def test__init_replacements(self):

        basename = "%s.repl" % gaupol.conf.spell_check.language
        path = os.path.join(self.dialog._personal_dir, basename)
        open(path, "w").write("a|b\nc|d\n")
        args = (self.application.window, self.application)
        self.dialog = gaupol.SpellCheckDialog(*args)

    def test__on_add_button_clicked(self):

        while True:
            if not self.dialog._table.props.sensitive: break
            self.dialog._add_button.emit("clicked")

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

        while True:
            if not self.dialog._table.props.sensitive: break
            self.dialog._ignore_all_button.emit("clicked")

    def test__on_ignore_button_clicked(self):

        while True:
            if not self.dialog._table.props.sensitive: break
            self.dialog._ignore_button.emit("clicked")

    def test__on_join_back_button_clicked(self):

        while True:
            if not self.dialog._table.props.sensitive: break
            if self.dialog._join_back_button.props.sensitive:
                self.dialog._join_back_button.emit("clicked")
            else: self.dialog._ignore_button.emit("clicked")

    def test__on_join_forward_button_clicked(self):

        while True:
            if not self.dialog._table.props.sensitive: break
            if self.dialog._join_forward_button.props.sensitive:
                self.dialog._join_forward_button.emit("clicked")
            else: self.dialog._ignore_button.emit("clicked")

    def test__on_replace_all_button_clicked(self):

        while True:
            if not self.dialog._table.props.sensitive: break
            self.dialog._replace_all_button.emit("clicked")

    def test__on_replace_button_clicked(self):

        while True:
            if not self.dialog._table.props.sensitive: break
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

    def test__write_replacements(self):

        for i in range(self.dialog._max_replacemnts + 1):
            self.dialog._replacements.append(("a", "b"))
        self.dialog._write_replacements()

    def test__write_replacements__io_error(self):

        os.chmod(self._temp_dir, 0000)
        self.test__on_replace_button_clicked()
        self.dialog.response(gtk.RESPONSE_CLOSE)
        os.chmod(self._temp_dir, 0777)
