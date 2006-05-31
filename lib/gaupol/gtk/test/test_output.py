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


from gaupol.gtk.output import OutputWindow
from gaupol.test       import Test


import gtk


class TestOutputWindow(Test):

    def setup_method(self, method):

        self.output_window = OutputWindow()
        self.output_window.show()

    def teardown_method(self, method):

        self.output_window._window.destroy()

    def test_get_position(self):

        position = self.output_window.get_position()
        assert isinstance(position[0], int)
        assert isinstance(position[1], int)

    def test_get_size(self):

        position = self.output_window.get_size()
        assert isinstance(position[0], int)
        assert isinstance(position[1], int)

    def test_get_visible(self):

        visible = self.output_window.get_visible()
        assert isinstance(visible, bool)

    def test_hide_and_show(self):

        self.output_window.hide()
        visible = self.output_window.get_visible()
        assert visible is False

        self.output_window.show()
        visible = self.output_window.get_visible()
        assert visible is True

    def test_set_output(self):

        self.output_window.set_output('test')
        text_buffer = self.output_window._text_view.get_buffer()
        start, end = text_buffer.get_bounds()
        output = text_buffer.get_text(start, end)
        assert output == 'test'

    def test_signals(self):

        self.count = 0
        def on_close(output_window):
            assert isinstance(output_window, OutputWindow)
            self.count += 1

        self.output_window.connect('close', on_close)
        self.output_window._close_button.emit('clicked')

        event = gtk.gdk.Event(gtk.gdk.NOTHING)
        self.output_window._window.emit('delete-event', event)
        assert self.count == 2

        self.output_window._window.maximize()
        self.output_window._window.unmaximize()
