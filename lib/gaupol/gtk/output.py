# Copyright (C) 2005 Osmo Salomaa
#
# This file is part of Gaupol.
#
# Gaupol is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Gaupol is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Gaupol; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA


"""External application output window."""


try:
    from psyco.classes import *
except ImportError:
    pass

from gettext import gettext as _

import gobject
import gtk

from gaupol.gtk.util import config


class OutputWindow(gobject.GObject):

    """External application output window."""

    __gsignals__ = {
        'close': (
            gobject.SIGNAL_RUN_LAST,
            None,
            ()
        )
    }

    def __init__(self):

        gobject.GObject.__init__(self)

        self._close_button = None
        self._text_view    = None
        self._window       = None

        # Text buffer end mark
        self._end_mark = None

        self._init_gui()
        self._init_sizes()
        self._init_keys()
        self._init_signals()
        self._init_text_tags()

    def _init_gui(self):
        """Initialize GUI widgets."""

        self._close_button = gtk.Button(stock=gtk.STOCK_CLOSE)
        button_box = gtk.HButtonBox()
        button_box.set_layout(gtk.BUTTONBOX_END)
        button_box.pack_start(self._close_button, False, False)

        self._text_view = gtk.TextView()
        self._text_view.set_wrap_mode(gtk.WRAP_WORD)
        scrolled_window = gtk.ScrolledWindow()
        scrolled_window.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scrolled_window.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        scrolled_window.add(self._text_view)

        vbox = gtk.VBox(spacing=12)
        vbox.pack_start(scrolled_window, True, True)
        vbox.pack_start(button_box, False, False)

        self._window = gtk.Window()
        self._window.set_border_width(12)
        self._window.set_title(_('Output'))
        self._window.add(vbox)

    def _init_sizes(self):
        """Initialize widget sizes."""

        self._window.resize(*config.output_window.size)
        self._window.move(*config.output_window.position)
        if config.output_window.maximized:
            self._window.maximize()

    def _init_keys(self):
        """Initialize keyboard shortcuts."""

        # Add Ctrl+W as an accelerator to close the window.
        accel_group = gtk.AccelGroup()
        accel_group.connect_group(
            119,
            gtk.gdk.CONTROL_MASK,
            gtk.ACCEL_MASK,
            self._on_close_requested
        )
        self._window.add_accel_group(accel_group)

    def _init_signals(self):
        """Initialize signals."""

        self._window.connect('delete-event', self._on_window_delete_event)
        self._window.connect('window-state-event', self._on_window_state_event)
        self._close_button.connect('clicked', self._on_close_requested)

    def _init_text_tags(self):
        """Initialize text tags."""

        text_buffer = self._text_view.get_buffer()
        text_buffer.create_tag('code', family='monospace')
        end_iter = text_buffer.get_end_iter()
        self._end_mark = text_buffer.create_mark('end', end_iter, True)

    def get_position(self):
        """Return the window position."""

        return self._window.get_position()

    def get_size(self):
        """Return the window size."""

        return self._window.get_size()

    def get_visible(self):
        """Return True if window is visible."""

        return self._window.props.visible

    def hide(self, *args):
        """Hide the window."""

        self._window.hide()

    def _on_close_requested(self, *args):
        """Emit signal that the window needs to be closed."""

        self.emit('close')

    def _on_window_delete_event(self, *args):
        """Emit signal that the close button has been clicked."""

        self.emit('close')

        # Prevent window destruction.
        return True

    def _on_window_state_event(self, window, event):
        """Remember whether window is maximized or not."""

        state = event.new_window_state
        maximized = bool(state & gtk.gdk.WINDOW_STATE_MAXIMIZED)
        config.output_window.maximized = maximized

    def scroll_down(self):
        """Scroll to the bottom of the text view."""

        text_buffer = self._text_view.get_buffer()
        end_iter = text_buffer.get_end_iter()
        text_buffer.move_mark(self._end_mark, end_iter)
        self._text_view.scroll_mark_onscreen(self._end_mark)

    def set_output(self, output):
        """Set output to the text view."""

        text_buffer = self._text_view.get_buffer()
        text_buffer.set_text('')
        end_iter = text_buffer.get_end_iter()
        text_buffer.insert_with_tags_by_name(end_iter, output, 'code')

        self.scroll_down()
        self._close_button.grab_focus()

    def show(self):
        """Show the window."""

        self.scroll_down()
        self._close_button.grab_focus()
        self._window.show_all()


if __name__ == '__main__':

    from gaupol.test import Test

    class TestOutputWindow(Test):

        def test_all(self):

            output_window = OutputWindow()
            output_window.get_position()
            output_window.get_size()
            output_window.get_visible()
            output_window.hide()
            output_window.scroll_down()
            output_window.set_output('foo')
            output_window.show()
            output_window._window.destroy()

    TestOutputWindow().run()
