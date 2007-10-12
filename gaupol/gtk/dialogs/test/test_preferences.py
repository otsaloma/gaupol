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

import gtk

from gaupol.gtk import unittest
from .. import preferences


class TestEditorPage(unittest.TestCase):

    def setup_method(self, method):

        self.dialog = preferences.PreferencesDialog()
        self.page = self.dialog._editor_page

    def test__on_default_font_check_toggled(self):

        self.page._default_font_check.emit("toggled")
        self.page._default_font_check.emit("toggled")

    def test__on_font_button_font_set(self):

        self.page._default_font_check.set_active(False)
        self.page._font_button.set_font_name("Serif 12")

    def test__on_length_cell_check_toggled(self):

        self.page._length_cell_check.emit("toggled")
        self.page._length_cell_check.emit("toggled")

    def test__on_length_combo_changed(self):

        self.page._length_combo.set_active(0)
        self.page._length_combo.set_active(1)

    def test__on_length_edit_check_toggled(self):

        self.page._length_edit_check.emit("toggled")
        self.page._length_edit_check.emit("toggled")


class TestFilePage(unittest.TestCase):

    def setup_method(self, method):

        self.dialog = preferences.PreferencesDialog()
        self.page = self.dialog._file_page

    def test__on_add_button_clicked(self):

        responder = iter((gtk.RESPONSE_OK, gtk.RESPONSE_CANCEL))
        def run_dialog(dialog):
            selection = dialog._tree_view.get_selection()
            selection.select_path(0)
            return responder.next()
        self.page.run_dialog = run_dialog
        self.page._on_add_button_clicked()
        self.page._on_add_button_clicked()

    def test__on_auto_check_toggled(self):

        self.page._auto_check.emit("toggled")
        self.page._auto_check.emit("toggled")

    def test__on_down_button_clicked(self):

        selection = self.page._tree_view.get_selection()
        selection.select_path(0)
        self.page._on_down_button_clicked()

    def test__on_locale_check_toggled(self):

        self.page._locale_check.emit("toggled")
        self.page._locale_check.emit("toggled")

    def test__on_remove_button_clicked(self):

        selection = self.page._tree_view.get_selection()
        selection.select_path(0)
        self.page._on_remove_button_clicked()

    def test__on_up_button_clicked(self):

        selection = self.page._tree_view.get_selection()
        selection.select_path(1)
        self.page._on_up_button_clicked()


class TestPreviewPage(unittest.TestCase):

    def setup_method(self, method):

        self.dialog = preferences.PreferencesDialog()
        self.page = self.dialog._preview_page

    def test__on_app_combo_changed(self):

        # pylint: disable-msg=W0631
        store = self.page._app_combo.get_model()
        indices = range(len(store) - 2)
        for index in indices:
            self.page._app_combo.set_active(index)
        self.page._app_combo.set_active(index + 2)

    def test__on_command_entry_changed(self):

        self.page._app_combo.set_active(0)
        self.page._command_entry.set_text("test")

    def test__on_offset_spin_value_changed(self):

        self.page._offset_spin.set_value(13)
        self.page._offset_spin.set_value(-13)


class TestPreferencesDialog(unittest.TestCase):

    def run(self):

        self.dialog.run()
        self.dialog.destroy()

    def setup_method(self, method):

        self.dialog = preferences.PreferencesDialog()

    def test___init__(self):

        pass
