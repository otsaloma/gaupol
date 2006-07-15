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


"""Output window."""


from gettext import gettext as _

import gobject
import gtk

from gaupol.gtk.util import conf, gtklib


class OutputWindow(gobject.GObject):

    """Output window."""

    __gsignals__ = {
        'closed': (
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

        self._init_widgets()
        self._init_sizes()
        self._init_signals()
        self._init_keys()

    def _init_sizes(self):
        """Initialize widget sizes."""

        self._window.resize(*conf.output_window.size)
        self._window.move(*conf.output_window.position)
        if conf.output_window.maximized:
            self._window.maximize()

    def _init_keys(self):
        """Initialize keyboard shortcuts."""

        # Add Ctrl+W as an accelerator to close the window.
        accel_group = gtk.AccelGroup()
        accel_group.connect_group(
            119,
            gtk.gdk.CONTROL_MASK,
            gtk.ACCEL_MASK,
            self._on_close_key_pressed
        )
        self._window.add_accel_group(accel_group)

    def _init_signals(self):
        """Initialize signals."""

        gtklib.connect(self, '_close_button', 'clicked'           )
        gtklib.connect(self, '_window'      , 'delete-event'      )
        gtklib.connect(self, '_window'      , 'window-state-event')

    def _init_widgets(self):
        """Initialize widgets."""

        self._text_view = gtk.TextView()
        self._text_view.set_wrap_mode(gtk.WRAP_WORD)
        self._text_view.set_cursor_visible(False)
        self._text_view.set_editable(False)
        gtklib.set_widget_font(self._text_view, 'monospace')

        scrolled_window = gtk.ScrolledWindow()
        scrolled_window.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scrolled_window.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        scrolled_window.add(self._text_view)

        self._close_button = gtk.Button(stock=gtk.STOCK_CLOSE)
        button_box = gtk.HButtonBox()
        button_box.set_layout(gtk.BUTTONBOX_END)
        button_box.pack_start(self._close_button, False, False)

        vbox = gtk.VBox(spacing=12)
        vbox.pack_start(scrolled_window, True, True)
        vbox.pack_start(button_box, False, False)

        self._window = gtk.Window()
        self._window.set_border_width(12)
        self._window.set_title(_('Output'))
        self._window.add(vbox)

    def _on_close_button_clicked(self, *args):
        """Emit closed signal."""

        self._save_geometry()
        self.emit('closed')

    def _on_close_key_pressed(self, *args):
        """Emit closed signal."""

        self._save_geometry()
        self.emit('closed')

    def _on_window_delete_event(self, *args):
        """Emit closed signal."""

        self._save_geometry()
        self.emit('closed')
        return True

    def _on_window_window_state_event(self, window, event):
        """Remember window maximization."""

        state = event.new_window_state
        maximized = bool(state & gtk.gdk.WINDOW_STATE_MAXIMIZED)
        conf.output_window.maximized = maximized

    def _save_geometry(self):
        """Save window geometry."""

        if not conf.output_window.maximized:
            conf.output_window.size = list(self.get_size())
            conf.output_window.position = list(self.get_position())

    def get_position(self):
        """Get window position."""

        return self._window.get_position()

    def get_size(self):
        """Get window size."""

        return self._window.get_size()

    def get_visible(self):
        """Get window visibility."""

        return self._window.props.visible

    def hide(self):
        """Hide window."""

        self._window.hide()

    def show(self):
        """Show window."""

        self._text_view.grab_focus()
        self._window.show_all()

    def set_output(self, output):
        """Set output to text view."""

        text_buffer = self._text_view.get_buffer()
        text_buffer.set_text(output)
        mark = text_buffer.get_insert()
        self._text_view.scroll_to_mark(mark, 0)
