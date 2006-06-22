# Copyright (C) 2005-2006 Osmo Salomaa
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


from gaupol.gtk.dialog.pref import PreferencesDialog
from gaupol.test            import Test


class TestPreferencesDialog(Test):

    def setup_method(self, method):

        self.dialog = PreferencesDialog()

    def test_show(self):

        self.dialog.show()
        self.dialog._dialog.run()
        self.dialog._dialog.destroy()

    def test_boolean_signals(self):

        for check_button in (
            self.dialog._editor._default_font_check,
            self.dialog._editor._unlimit_undo_check,
            self.dialog._file._auto_check,
            self.dialog._file._locale_check,
        ):
            check_button.set_active(True)
            check_button.set_active(False)
            check_button.set_active(True)

    def test_editor_signals(self):

        self.dialog._editor._font_button.set_font_name('Sans 10')
        self.dialog._editor._undo_limit_spin.set_value(33)

    def test_file_signals(self):

        tree_view = self.dialog._file._tree_view
        self.dialog._file._add_button.emit('clicked')
        tree_view.set_cursor(0)
        self.dialog._file._down_button.emit('clicked')
        tree_view.set_cursor(1)
        self.dialog._file._up_button.emit('clicked')
        self.dialog._file._remove_button.emit('clicked')

    def test_preview_signals(self):

        self.dialog._preview._app_combo.set_active(0)
        self.dialog._preview._app_combo.set_active(1)
        self.dialog._preview._app_combo.set_active(3)
        self.dialog._preview._command_entry.set_text('test')
        self.dialog._preview._offset_spin.set_value(3.3)
