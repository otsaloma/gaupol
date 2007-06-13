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


import gaupol.gtk
from gaupol.gtk import unittest


class TestViewAgent(unittest.TestCase):

    def setup_method(self, method):

        self.application = self.get_application()

    def test_on_framerate_combo_changed(self):

        for framerate in gaupol.gtk.FRAMERATE.members:
            self.application.framerate_combo.set_active(framerate)

    def test_on_output_window_notify_visible(self):

        self.application.on_output_window_notify_visible()

    def test_on_show_framerate_24_changed(self):

        for name in gaupol.gtk.FRAMERATE.actions:
            self.application.get_action(name).activate()

    def test_on_show_times_changed(self):

        for name in gaupol.gtk.MODE.actions:
            self.application.get_action(name).activate()

    def test_on_toggle_duration_column_toggled(self):

        name = gaupol.gtk.COLUMN.DURATION.action
        self.application.get_action(name).activate()
        self.application.get_action(name).activate()

    def test_on_toggle_end_column_toggled(self):

        name = gaupol.gtk.COLUMN.END.action
        self.application.get_action(name).activate()
        self.application.get_action(name).activate()

    def test_on_toggle_main_text_column_toggled(self):

        name = gaupol.gtk.COLUMN.MAIN_TEXT.action
        self.application.get_action(name).activate()
        self.application.get_action(name).activate()

    def test_on_toggle_main_toolbar_toggled(self):

        self.application.get_action("toggle_main_toolbar").activate()
        self.application.get_action("toggle_main_toolbar").activate()

    def test_on_toggle_number_column_toggled(self):

        name = gaupol.gtk.COLUMN.NUMBER.action
        self.application.get_action(name).activate()
        self.application.get_action(name).activate()

    def test_on_toggle_output_window_toggled(self):

        self.application.get_action("toggle_output_window").activate()
        self.application.get_action("toggle_output_window").activate()

    def test_on_toggle_start_column_toggled(self):

        name = gaupol.gtk.COLUMN.START.action
        self.application.get_action(name).activate()
        self.application.get_action(name).activate()

    def test_on_toggle_statusbar_activate(self):

        self.application.get_action("toggle_statusbar").activate()
        self.application.get_action("toggle_statusbar").activate()

    def test_on_toggle_translation_text_column_toggled(self):

        name = gaupol.gtk.COLUMN.TRAN_TEXT.action
        self.application.get_action(name).activate()
        self.application.get_action(name).activate()

    def test_on_toggle_video_toolbar_toggled(self):

        self.application.get_action("toggle_video_toolbar").activate()
        self.application.get_action("toggle_video_toolbar").activate()
