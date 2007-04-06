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


"""Output window."""


import gtk

from gaupol.gtk import conf, util
from gaupol.gtk.i18n import _


class OutputWindow(gtk.Window):

    """Output window.

    Instance variables:

        _close_button: gtk.Button
        _text_view:    gtk.TextView
    """

    def __init__(self):

        gtk.Window.__init__(self)

        self._close_button = None
        self._text_view    = None

        self.set_border_width(12)
        self.set_title(_("Output"))
        self._init_widgets()
        self._init_sizes()
        self._init_signal_handlers()
        self._init_keys()

    def _init_keys(self):
        """Initialize keyboard shortcuts."""

        # Add Ctrl+W as an accelerator to close the window.
        accel_group = gtk.AccelGroup()
        method = self._on_close_key_pressed
        accel_group.connect_group(
            119, gtk.gdk.CONTROL_MASK, gtk.ACCEL_MASK, method)
        self.add_accel_group(accel_group)

    def _init_signal_handlers(self):
        """Initialize signal handlers."""

        util.connect(self, "_close_button", "clicked")
        util.connect(self, self, "delete-event")
        util.connect(self, self, "notify::visible")
        util.connect(self, self, "window-state-event")

    def _init_sizes(self):
        """Initialize widget sizes."""

        self.resize(*conf.output_window.size)
        self.move(*conf.output_window.position)
        if conf.output_window.maximized:
            self.maximize()

    def _init_widgets(self):
        """Initialize widgets."""

        self._text_view = gtk.TextView()
        self._text_view.set_wrap_mode(gtk.WRAP_WORD)
        self._text_view.set_cursor_visible(False)
        self._text_view.set_editable(False)
        util.set_widget_font(self._text_view, "monospace")

        scroller = gtk.ScrolledWindow()
        scroller.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scroller.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        scroller.add(self._text_view)

        self._close_button = gtk.Button(stock=gtk.STOCK_CLOSE)
        button_box = gtk.HButtonBox()
        button_box.set_layout(gtk.BUTTONBOX_END)
        button_box.pack_start(self._close_button, False, False)

        vbox = gtk.VBox(spacing=12)
        vbox.pack_start(scroller, True, True)
        vbox.pack_start(button_box, False, False)
        vbox.show_all()
        self.add(vbox)

    def _on_close_button_clicked(self, *args):
        """Hide the window."""

        self._save_geometry()
        self.hide()

    def _on_close_key_pressed(self, *args):
        """Hide the window."""

        self._save_geometry()
        self.hide()

    def _on_delete_event(self, *args):
        """Hide the window."""

        self._save_geometry()
        self.hide()
        return True

    def _on_notify_visible(self, *args):
        """Save visibility."""

        conf.output_window.show = self.props.visible

    def _on_window_state_event(self, window, event):
        """Remember window maximization."""

        state = event.new_window_state
        maximized = bool(state & gtk.gdk.WINDOW_STATE_MAXIMIZED)
        conf.output_window.maximized = maximized

    @util.silent(AssertionError)
    def _save_geometry(self):
        """Save window geometry."""

        assert not conf.output_window.maximized
        conf.output_window.size = self.get_size()
        conf.output_window.position = self.get_position()

    def set_output(self, output):
        """Set output to the text view."""

        text_buffer = self._text_view.get_buffer()
        text_buffer.set_text(output)
        mark = text_buffer.get_insert()
        self._text_view.scroll_to_mark(mark, 0)
