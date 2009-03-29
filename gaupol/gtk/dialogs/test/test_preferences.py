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

import gaupol.gtk
import gtk


class Test_EditorPage(gaupol.gtk.TestCase):

    def setup_method(self, method):

        self.application = self.get_application()
        args = (self.application.window, self.application)
        self.dialog = gaupol.gtk.PreferencesDialog(*args)
        self.page = self.dialog._editor_page
        self.dialog.show()

    def test__on_default_font_check_toggled(self):

        self.page._default_font_check.set_active(True)
        self.page._default_font_check.set_active(False)
        self.page._default_font_check.set_active(True)

    def test__on_font_button_font_set(self):

        self.page._default_font_check.set_active(False)
        self.page._font_button.set_font_name("Serif 12")
        self.page._font_button.emit("font-set")

    def test__on_length_cell_check_toggled(self):

        self.page._length_cell_check.set_active(True)
        self.page._length_cell_check.set_active(False)
        self.page._length_cell_check.set_active(True)

    def test__on_length_combo_changed(self):

        self.page._length_combo.set_active(0)
        self.page._length_combo.set_active(1)

    def test__on_length_edit_check_toggled(self):

        self.page._length_edit_check.set_active(True)
        self.page._length_edit_check.set_active(False)
        self.page._length_edit_check.set_active(True)


class Test_ExtensionPage(gaupol.gtk.TestCase):

    def setup_method(self, method):

        self.application = self.get_application()
        args = (self.application.window, self.application)
        self.dialog = gaupol.gtk.PreferencesDialog(*args)
        self.page = self.dialog._extension_page
        self.dialog.show()

    def test__on_about_button_clicked(self):

        self.page.flash_dialog = lambda *args: gtk.RESPONSE_CLOSE
        selection = self.page._tree_view.get_selection()
        selection.select_path(0)
        self.page._about_button.clicked()

    def test__on_about_dialog_url_clicked(self):

        self.page._on_about_dialog_url_clicked(None, gaupol.HOMEPAGE_URL)

    def test__on_help_button_clicked(self):

        selection = self.page._tree_view.get_selection()
        selection.select_path(0)
        store = self.page._tree_view.get_model()
        module = store[0][0]
        column = self.page._tree_view.get_columns()[0]
        renderer = column.get_cell_renderers()[0]
        if not store[0][1]:
            renderer.emit("toggled", 0)
        if self.page.manager.has_help(module):
            self.page._help_button.clicked()

    def test__on_preferences_button_clicked(self):

        selection = self.page._tree_view.get_selection()
        selection.select_path(0)
        store = self.page._tree_view.get_model()
        module = store[0][0]
        column = self.page._tree_view.get_columns()[0]
        renderer = column.get_cell_renderers()[0]
        if not store[0][1]:
            renderer.emit("toggled", 0)
        if self.page.manager.has_preferences_dialog(module):
            self.page._preferences_button.clicked()

    def test__on_tree_view_cell_toggled(self):

        column = self.page._tree_view.get_columns()[0]
        renderer = column.get_cell_renderers()[0]
        renderer.emit("toggled", 0)
        renderer.emit("toggled", 0)
        renderer.emit("toggled", 0)

    def test__on_tree_view_selection_changed(self):

        selection = self.page._tree_view.get_selection()
        selection.unselect_all()
        selection.select_path(0)
        column = self.page._tree_view.get_columns()[0]
        renderer = column.get_cell_renderers()[0]
        renderer.emit("toggled", 0)
        selection.unselect_all()
        selection.select_path(0)


class Test_FilePage(gaupol.gtk.TestCase):

    def setup_method(self, method):

        self.application = self.get_application()
        args = (self.application.window, self.application)
        self.dialog = gaupol.gtk.PreferencesDialog(*args)
        self.page = self.dialog._file_page
        self.dialog.show()

    def test__on_add_button_clicked(self):

        responder = iter((gtk.RESPONSE_OK, gtk.RESPONSE_CANCEL))
        def run_dialog(dialog):
            selection = dialog._tree_view.get_selection()
            selection.select_path(0)
            return responder.next()
        self.page.run_dialog = run_dialog
        self.page._add_button.emit("clicked")
        self.page._add_button.emit("clicked")

    def test__on_auto_check_toggled(self):

        self.page._auto_check.set_active(True)
        self.page._auto_check.set_active(False)
        self.page._auto_check.set_active(True)

    def test__on_down_button_clicked(self):

        selection = self.page._tree_view.get_selection()
        selection.select_path(0)
        self.page._down_button.emit("clicked")

    def test__on_locale_check_toggled(self):

        self.page._locale_check.set_active(True)
        self.page._locale_check.set_active(False)
        self.page._locale_check.set_active(True)

    def test__on_remove_button_clicked(self):

        selection = self.page._tree_view.get_selection()
        selection.select_path(0)
        self.page._remove_button.emit("clicked")

    def test__on_up_button_clicked(self):

        selection = self.page._tree_view.get_selection()
        selection.select_path(1)
        self.page._up_button.emit("clicked")


class Test_PreviewPage(gaupol.gtk.TestCase):

    def setup_method(self, method):

        self.application = self.get_application()
        args = (self.application.window, self.application)
        self.dialog = gaupol.gtk.PreferencesDialog(*args)
        self.page = self.dialog._preview_page
        self.dialog.show()

    def test__init_values(self):

        gaupol.gtk.conf.preview.use_custom = False
        args = (self.application.window, self.application)
        self.dialog = gaupol.gtk.PreferencesDialog(*args)
        gaupol.gtk.conf.preview.use_custom = True
        args = (self.application.window, self.application)
        self.dialog = gaupol.gtk.PreferencesDialog(*args)

    def test__on_app_combo_changed(self):

        # pylint: disable-msg=W0631
        store = self.page._app_combo.get_model()
        for i in range(len(store) - 2):
            self.page._app_combo.set_active(i)
        self.page._app_combo.set_active(i + 2)

    def test__on_command_entry_changed(self):

        self.page._app_combo.set_active(0)
        self.page._command_entry.set_text("test")

    def test__on_force_utf_8_check_toggled(self):

        self.page._force_utf_8_check.set_active(True)
        self.page._force_utf_8_check.set_active(False)
        self.page._force_utf_8_check.set_active(True)

    def test__on_offset_spin_value_changed(self):

        self.page._offset_spin.set_value(13)
        self.page._offset_spin.set_value(-13)


class TestPreferencesDialog(gaupol.gtk.TestCase):

    def run__dialog(self):

        self.dialog.run()
        self.dialog.destroy()

    def setup_method(self, method):

        self.application = self.get_application()
        args = (self.application.window, self.application)
        self.dialog = gaupol.gtk.PreferencesDialog(*args)
        self.dialog.show()
