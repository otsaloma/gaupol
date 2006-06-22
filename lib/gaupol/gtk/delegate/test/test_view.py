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


from gaupol.gtk     import cons
from gaupol.gtk.app import Application
from gaupol.test    import Test


class TestViewDelegate(Test):

    def setup_method(self, method):

        self.app = Application()
        self.app.open_main_files([self.get_subrip_path()])

    def teardown_method(self, method):

        Test.teardown_method(self, method)
        self.app._window.destroy()

    def test_on_framerate_combo_changed(self):

        for i in range(len(cons.Framerate.values)):
            self.app._framerate_combo.set_active(i)
        for i in range(len(cons.Framerate.values)):
            self.app._framerate_combo.set_active(i)

    def test_on_toggle_column_activate(self):

        for path in cons.Column.uim_paths:
            self.app._uim.get_action(path).activate()
        for path in cons.Column.uim_paths:
            self.app._uim.get_action(path).activate()

    def test_on_toggle_edit_mode_activate(self):

        for path in cons.Mode.uim_paths:
            self.app._uim.get_action(path).activate()
        for path in cons.Mode.uim_paths:
            self.app._uim.get_action(path).activate()

    def test_on_toggle_framerate_activate(self):

        for path in cons.Framerate.uim_paths:
            self.app._uim.get_action(path).activate()
        for path in cons.Framerate.uim_paths:
            self.app._uim.get_action(path).activate()

    def test_on_toggle_main_toolbar_activate(self):

        path = '/ui/menubar/view/main_toolbar'
        self.app._uim.get_action(path).activate()
        self.app._uim.get_action(path).activate()

    def test_on_toggle_output_window_activate(self):

        path = '/ui/menubar/view/output_window'
        self.app._uim.get_action(path).activate()
        self.app._uim.get_action(path).activate()

    def test_on_toggle_statusbar_activate(self):

        path = '/ui/menubar/view/statusbar'
        self.app._uim.get_action(path).activate()
        self.app._uim.get_action(path).activate()

    def test_on_toggle_video_toolbar_activate(self):

        path = '/ui/menubar/view/video_toolbar'
        self.app._uim.get_action(path).activate()
        self.app._uim.get_action(path).activate()
