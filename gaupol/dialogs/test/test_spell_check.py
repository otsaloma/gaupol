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

import aeidon
import functools
import gaupol
import os

from gi.repository import Gtk


def while_errors(function):
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        while True:
            value = function(*args, **kwargs)
            # Break when no more errors left.
            if not args[0].dialog._grid.props.sensitive: break
        return value
    return wrapper


class TestSpellCheckDialog(gaupol.TestCase):

    def run__show_error_dialog(self):
        self.dialog._show_error_dialog("test")

    def run_dialog(self):
        self.dialog.run()
        self.dialog.destroy()

    def setup_method(self, method):
        gaupol.conf.editor.use_custom_font = True
        gaupol.conf.editor.custom_font = "monospace"
        gaupol.conf.spell_check.language = "en"
        self.application = self.new_application()
        for page in self.application.pages:
            for subtitle in page.project.subtitles:
                subtitle.main_text = subtitle.main_text.replace("a", "x")
                subtitle.tran_text = subtitle.tran_text.replace("a", "x")
            page.reload_view_all()
        self.dialog = gaupol.SpellCheckDialog(self.application.window,
                                              self.application)

        # Avoid adding words to either enchant's or a backend's
        # personal word list or gaupol's personal replacement list.
        self.dialog._checker.dict.add = lambda *args: None
        self._temp_dir = aeidon.temp.create_directory()
        self.dialog._personal_dir = self._temp_dir
        self.dialog.show()

    @aeidon.deco.monkey_patch(gaupol.util, "flash_dialog")
    def test___init____enchant_error(self):
        gaupol.util.flash_dialog = lambda *args: Gtk.ResponseType.OK
        gaupol.conf.spell_check.language = "wo"
        self.assert_raises(ValueError,
                           gaupol.SpellCheckDialog,
                           self.application.window,
                           self.application)

    def test___init____replacements(self):
        basename = "{}.repl".format(gaupol.conf.spell_check.language)
        path = os.path.join(self.dialog._personal_dir, basename)
        open(path, "w").write("a|b\nc|d\n")
        gaupol.SpellCheckDialog(self.application.window,
                                self.application)

    @while_errors
    def test__on_add_button_clicked(self):
        self.dialog._checker.dict.add = lambda *args: None
        self.dialog._add_button.emit("clicked")

    @aeidon.deco.monkey_patch(gaupol.util, "run_dialog")
    def test__on_edit_button_clicked(self):
        gaupol.util.run_dialog = lambda *args: Gtk.ResponseType.OK
        self.dialog._edit_button.emit("clicked")

    def test__on_entry_changed(self):
        self.dialog._entry.set_text("t")
        self.dialog._entry.set_text("te")
        self.dialog._entry.set_text("tes")
        self.dialog._entry.set_text("test")

    @while_errors
    def test__on_ignore_all_button_clicked(self):
        self.dialog._ignore_all_button.emit("clicked")

    @while_errors
    def test__on_ignore_button_clicked(self):
        self.dialog._ignore_button.emit("clicked")

    @while_errors
    def test__on_join_back_button_clicked(self):
        if self.dialog._join_back_button.props.sensitive:
            self.dialog._join_back_button.emit("clicked")
        else: self.dialog._ignore_button.emit("clicked")

    @while_errors
    def test__on_join_forward_button_clicked(self):
        if self.dialog._join_forward_button.props.sensitive:
            self.dialog._join_forward_button.emit("clicked")
        else: self.dialog._ignore_button.emit("clicked")

    @while_errors
    def test__on_replace_all_button_clicked(self):
        self.dialog._replace_all_button.emit("clicked")

    @while_errors
    def test__on_replace_button_clicked(self):
        self.dialog._replace_button.emit("clicked")

    def test__on_response(self):
        self.dialog._replace_button.emit("clicked")
        self.dialog.response(Gtk.ResponseType.CLOSE)

    def test__on_tree_view_selection_changed(self):
        store = self.dialog._tree_view.get_model()
        selection = self.dialog._tree_view.get_selection()
        for i in range(len(store)):
            selection.select_path(i)

    @aeidon.deco.monkey_patch(gaupol.util, "flash_dialog")
    def test__show_error_dialog(self):
        gaupol.util.flash_dialog = lambda *args: Gtk.ResponseType.OK
        self.dialog._show_error_dialog("test")
