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


import gtk

from gaupol.gtk.output import OutputWindow
from gaupol.test       import Test


class TestOutputWindow(Test):

    def setup_method(self, method):

        self.window = OutputWindow()
        self.window.show()

    def teardown_method(self, method):

        self.window._window.destroy()

    def test_get_position(self):

        position = self.window.get_position()
        assert isinstance(position[0], int)
        assert isinstance(position[1], int)

    def test_get_size(self):

        position = self.window.get_size()
        assert isinstance(position[0], int)
        assert isinstance(position[1], int)

    def test_get_visible(self):

        visible = self.window.get_visible()
        assert isinstance(visible, bool)

    def test_hide_and_show(self):

        self.window.hide()
        visible = self.window.get_visible()
        assert visible is False

        self.window.show()
        visible = self.window.get_visible()
        assert visible is True

    def test_set_output(self):

        self.window.set_output('test')
        text_buffer = self.window._text_view.get_buffer()
        start, end = text_buffer.get_bounds()
        output = text_buffer.get_text(start, end)
        assert output == 'test'

    def test_signals(self):

        self.window._on_close_button_clicked()
        self.window._on_close_key_pressed()
        self.window._on_window_delete_event()

        self.window._window.maximize()
        self.window._window.unmaximize()
