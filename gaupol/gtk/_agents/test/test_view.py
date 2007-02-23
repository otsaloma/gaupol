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


from gaupol.gtk import cons
from gaupol.gtk.index import *
from gaupol.gtk.unittest import TestCase


class TestViewAgent(TestCase):

    def setup_method(self, method):

        self.application = self.get_application()

    def test_on_framerate_combo_changed(self):

        for framerate in cons.FRAMERATE.members:
            self.application.framerate_combo.set_active(framerate)

    def test_on_output_window_notify_visible(self):

        self.application.on_output_window_notify_visible()

    def test_on_show_columns_menu_activate(self):

        self.application.on_show_columns_menu_activate()

    def test_on_show_framerate_23_976_activate(self):

        for path in cons.FRAMERATE.uim_paths:
            self.application.uim.get_action(path).activate()

    def test_on_show_framerate_menu_activate(self):

        self.application.on_show_framerate_menu_activate()

    def test_on_show_times_activate(self):

        for path in cons.MODE.uim_paths:
            self.application.uim.get_action(path).activate()

    def test_on_toggle_duration_column_activate(self):

        self.application.uim.get_action(DURN.uim_path).activate()
        self.application.uim.get_action(DURN.uim_path).activate()

    def test_on_toggle_hide_column_activate(self):

        self.application.uim.get_action(HIDE.uim_path).activate()
        self.application.uim.get_action(HIDE.uim_path).activate()

    def test_on_toggle_main_text_column_activate(self):

        self.application.uim.get_action(MTXT.uim_path).activate()
        self.application.uim.get_action(MTXT.uim_path).activate()

    def test_on_toggle_main_toolbar_activate(self):

        path = "/ui/menubar/view/main_toolbar"
        action = self.application.uim.get_action(path)
        action.activate()
        action.activate()

    def test_on_toggle_number_column_activate(self):

        self.application.uim.get_action(NO.uim_path).activate()
        self.application.uim.get_action(NO.uim_path).activate()

    def test_on_toggle_output_window_activate(self):

        path = "/ui/menubar/view/output_window"
        action = self.application.uim.get_action(path)
        action.activate()
        action.activate()

    def test_on_toggle_show_column_activate(self):

        self.application.uim.get_action(SHOW.uim_path).activate()
        self.application.uim.get_action(SHOW.uim_path).activate()

    def test_on_toggle_statusbar_activate(self):

        path = "/ui/menubar/view/statusbar"
        action = self.application.uim.get_action(path)
        action.activate()
        action.activate()

    def test_on_toggle_translation_text_column_activate(self):

        self.application.uim.get_action(TTXT.uim_path).activate()
        self.application.uim.get_action(TTXT.uim_path).activate()

    def test_on_toggle_video_toolbar_activate(self):

        path = "/ui/menubar/view/video_toolbar"
        action = self.application.uim.get_action(path)
        action.activate()
        action.activate()
