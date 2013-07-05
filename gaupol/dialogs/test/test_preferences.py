# -*- coding: utf-8 -*-

# Copyright (C) 2005-2008,2010,2012-2013 Osmo Salomaa
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
import gaupol

from gi.repository import Gdk
from gi.repository import Gtk


class TestEditorPage(gaupol.TestCase):

    def setup_method(self, method):
        self.application = self.new_application()
        self.dialog = gaupol.PreferencesDialog(self.application.window,
                                               self.application)

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

    def test__on_spell_check_check_toggled(self):
        self.page._spell_check_check.set_active(True)
        self.page._spell_check_check.set_active(False)
        self.page._spell_check_check.set_active(True)


class TestExtensionPage(gaupol.TestCase):

    def setup_method(self, method):
        self.application = self.new_application()
        self.dialog = gaupol.PreferencesDialog(self.application.window,
                                               self.application)

        self.page = self.dialog._extension_page
        self.dialog.show()

    @aeidon.deco.monkey_patch(gaupol.util, "flash_dialog")
    def test__on_about_button_clicked(self):
        gaupol.util.flash_dialog = lambda *args: Gtk.ResponseType.CLOSE
        selection = self.page._tree_view.get_selection()
        path = gaupol.util.tree_row_to_path(0)
        selection.select_path(path)
        self.page._about_button.emit("clicked")

    def test__on_tree_view_cell_toggled(self):
        column = self.page._tree_view.get_columns()[0]
        renderer = column.get_cells()[0]
        renderer.emit("toggled", 0)
        renderer.emit("toggled", 0)
        renderer.emit("toggled", 0)

    def test__on_tree_view_selection_changed(self):
        selection = self.page._tree_view.get_selection()
        selection.unselect_all()
        path = gaupol.util.tree_row_to_path(0)
        selection.select_path(path)
        column = self.page._tree_view.get_columns()[0]
        renderer = column.get_cells()[0]
        renderer.emit("toggled", 0)
        selection.unselect_all()
        selection.select_path(path)


class TestFilePage(gaupol.TestCase):

    def setup_method(self, method):
        self.application = self.new_application()
        self.dialog = gaupol.PreferencesDialog(self.application.window,
                                               self.application)

        self.page = self.dialog._file_page
        self.dialog.show()

    @aeidon.deco.monkey_patch(gaupol.util, "run_dialog")
    def test__on_add_button_clicked(self):
        def run_dialog(dialog):
            selection = dialog._tree_view.get_selection()
            path = gaupol.util.tree_row_to_path(0)
            selection.select_path(path)
            return Gtk.ResponseType.OK
        gaupol.util.run_dialog = run_dialog
        self.page._add_button.emit("clicked")

    def test__on_auto_check_toggled(self):
        self.page._auto_check.set_active(True)
        self.page._auto_check.set_active(False)
        self.page._auto_check.set_active(True)

    def test__on_down_button_clicked(self):
        selection = self.page._tree_view.get_selection()
        path = gaupol.util.tree_row_to_path(0)
        selection.select_path(path)
        self.page._down_button.emit("clicked")

    def test__on_locale_check_toggled(self):
        self.page._locale_check.set_active(True)
        self.page._locale_check.set_active(False)
        self.page._locale_check.set_active(True)

    def test__on_remove_button_clicked(self):
        selection = self.page._tree_view.get_selection()
        path = gaupol.util.tree_row_to_path(0)
        selection.select_path(path)
        self.page._remove_button.emit("clicked")

    def test__on_up_button_clicked(self):
        selection = self.page._tree_view.get_selection()
        path = gaupol.util.tree_row_to_path(1)
        selection.select_path(path)
        self.page._up_button.emit("clicked")


class TestPreviewPage(gaupol.TestCase):

    def setup_method(self, method):
        self.application = self.new_application()
        self.dialog = gaupol.PreferencesDialog(self.application.window,
                                               self.application)

        self.page = self.dialog._preview_page
        self.dialog.show()

    def test__init____use_built_in(self):
        gaupol.conf.preview.use_custom_command = False
        self.dialog = gaupol.PreferencesDialog(self.application.window,
                                               self.application)

    def test__init____use_custom(self):
        gaupol.conf.preview.use_custom_command = True
        self.dialog = gaupol.PreferencesDialog(self.application.window,
                                               self.application)

    def test__on_app_combo_changed(self):
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


class TestVideoPage(gaupol.TestCase):

    def setup_method(self, method):
        self.application = self.new_application()
        self.dialog = gaupol.PreferencesDialog(self.application.window,
                                               self.application)

        self.page = self.dialog._video_page
        self.dialog.show()

    def test__on_subtitle_bg_check_toggled(self):
        self.page._subtitle_bg_check.set_active(True)
        self.page._subtitle_bg_check.set_active(False)
        self.page._subtitle_bg_check.set_active(True)

    def test__on_subtitle_color_button_color_set(self):
        color = Gdk.RGBA(red=1.0, green=0.0, blue=0.0)
        self.page._subtitle_color_button.set_rgba(color)
        self.page._subtitle_color_button.emit("color-set")

    def test__on_subtitle_font_button_font_set(self):
        self.page._subtitle_font_button.set_font_name("Serif 12")
        self.page._subtitle_font_button.emit("font-set")

    def test__on_time_bg_check_toggled(self):
        self.page._time_bg_check.set_active(True)
        self.page._time_bg_check.set_active(False)
        self.page._time_bg_check.set_active(True)

    def test__on_time_color_button_color_set(self):
        color = Gdk.RGBA(red=1.0, green=0.0, blue=0.0)
        self.page._time_color_button.set_rgba(color)
        self.page._time_color_button.emit("color-set")

    def test__on_time_font_button_font_set(self):
        self.page._time_font_button.set_font_name("Serif 12")
        self.page._time_font_button.emit("font-set")


class TestPreferencesDialog(gaupol.TestCase):

    def run_dialog(self):
        self.dialog.run()
        self.dialog.destroy()

    def setup_method(self, method):
        self.application = self.new_application()
        self.dialog = gaupol.PreferencesDialog(self.application.window,
                                               self.application)

        self.dialog.show()
