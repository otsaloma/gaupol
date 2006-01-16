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

import gobject
import gtk

from gaupol.gtk.util import config, gtklib


class OutputWindow(gobject.GObject):

    """External application output window."""

    __gsignals__ = {
        'close-button-clicked': (
            gobject.SIGNAL_RUN_LAST,
            None,
            ()
        )
    }

    def __init__(self):

        gobject.GObject.__init__(self)

        glade_xml = gtklib.get_glade_xml('output-window.glade')
        self._window       = glade_xml.get_widget('window')
        self._text_view    = glade_xml.get_widget('text_view')
        self._close_button = glade_xml.get_widget('close_button')

        # Set window geometry.
        self._window.resize(*config.output_window.size)
        self._window.move(*config.output_window.position)
        if config.output_window.maximized:
            self._window.maximize()

        # Connect signals.
        self._window.connect('delete-event', self._on_window_delete_event)
        self._window.connect('window-state-event', self._on_window_state_event)
        self._close_button.connect('clicked', self._on_close_button_clicked)

        # Create text tags and marks.
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

    def _on_close_button_clicked(self, *args):
        """Emit signal that the close button has been clicked."""

        self.emit('close-button-clicked')

    def _on_window_delete_event(self, *args):
        """Emit signal that the close button has been clicked."""

        self.emit('close-button-clicked')

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
