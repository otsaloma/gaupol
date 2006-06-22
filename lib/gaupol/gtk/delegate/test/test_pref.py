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


from gaupol.gtk.app           import Application
from gaupol.gtk.delegate.pref import PreferencesDelegate
from gaupol.test              import Test


class TestPreferencesDelegate(Test):

    def setup_method(self, method):

        self.app = Application()
        self.app.open_main_files([self.get_subrip_path()])
        self.delegate = PreferencesDelegate(self.app)

    def teardown_method(self, method):

        self.app._window.destroy()

    def test_enforce_font(self):

        self.delegate._enforce_font('Serif 12')

    def test_enforce_undo_levels(self):

        self.delegate._enforce_undo_levels(33)
        self.delegate._enforce_undo_levels(0)

    def test_on_dialog_font_set(self):

        self.delegate._on_dialog_font_set(None, 'Serif 12')

    def test_on_dialog_limit_undo_toggled(self):

        self.delegate._on_dialog_limit_undo_toggled(None, True)
        self.delegate._on_dialog_limit_undo_toggled(None, False)
        self.delegate._on_dialog_limit_undo_toggled(None, True)

    def test_on_dialog_undo_levels_changed(self):

        self.delegate._on_dialog_undo_levels_changed(None, 33)
        self.delegate._on_dialog_undo_levels_changed(None, 0)

    def test_on_dialog_use_default_font_toggled(self):

        self.delegate._on_dialog_use_default_font_toggled(None, True)
        self.delegate._on_dialog_use_default_font_toggled(None, False)
        self.delegate._on_dialog_use_default_font_toggled(None, True)

    def test_on_edit_preferences_activate(self):

        self.app.on_edit_preferences_activate()
