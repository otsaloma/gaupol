# -*- coding: utf-8 -*-

# Copyright (C) 2005 Osmo Salomaa
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""Window for standard output from external applications."""

import aeidon
import gaupol

from aeidon.i18n   import _
from gi.repository import Gdk
from gi.repository import GObject
from gi.repository import Gtk

__all__ = ("OutputWindow",)


class OutputWindow(Gtk.Window):

    """Window for standard output from external applications."""

    def __init__(self, parent):
        """Initialize an :class:`OutputWindow` instance."""
        GObject.GObject.__init__(self)
        self._text_view = None
        self.set_title(_("Output"))
        self._init_widgets()
        self._init_sizes(parent)
        self._init_signal_handlers()
        self._init_keys()

    def _init_keys(self):
        """Initialize keyboard shortcuts."""
        accel_group = Gtk.AccelGroup()
        accel_group.connect(Gdk.KEY_w,
                            Gdk.ModifierType.CONTROL_MASK,
                            Gtk.AccelFlags.MASK,
                            self._on_close_key_pressed)

        self.add_accel_group(accel_group)

    def _init_signal_handlers(self):
        """Initialize signal handlers."""
        aeidon.util.connect(self, self, "delete-event")

    def _init_sizes(self, parent):
        """Initialize widget sizes."""
        width, height = gaupol.conf.output_window.size
        self.resize(width, height)
        with aeidon.util.silent(Exception):
            pwidth, pheight = parent.get_size()
            px, py  = parent.get_position()
            xoffset = pwidth/2 - width/2
            yoffset = pheight/2 - height/2
            self.move(px + xoffset, py + yoffset)

    def _init_widgets(self):
        """Initialize all contained widgets."""
        self._text_view = Gtk.TextView()
        self._text_view.set_wrap_mode(Gtk.WrapMode.WORD)
        self._text_view.set_cursor_visible(False)
        self._text_view.set_editable(False)
        self._text_view.set_left_margin(6)
        self._text_view.set_right_margin(6)
        self._text_view.set_pixels_below_lines(1)
        gaupol.util.set_widget_font(self._text_view, "monospace")
        scroller = Gtk.ScrolledWindow()
        scroller.set_policy(*((Gtk.PolicyType.AUTOMATIC,)*2))
        scroller.set_shadow_type(Gtk.ShadowType.ETCHED_IN)
        scroller.add(self._text_view)
        scroller.show_all()
        self.add(scroller)

    def _on_close_button_clicked(self, *args):
        """Hide window."""
        self.save_geometry()
        self.hide()

    def _on_close_key_pressed(self, *args):
        """Hide window."""
        self.save_geometry()
        self.hide()

    def _on_delete_event(self, *args):
        """Hide window."""
        self.save_geometry()
        self.hide()
        return True

    def save_geometry(self):
        """Save window size."""
        with aeidon.util.silent(AttributeError):
            # is_maximized was added in GTK+ 3.12.
            if self.is_maximized(): return
        gaupol.conf.output_window.size = list(self.get_size())

    def set_output(self, output):
        """Display `output` in text view."""
        text_buffer = self._text_view.get_buffer()
        text_buffer.set_text(output)
        mark = text_buffer.get_insert()
        self._text_view.scroll_to_mark(mark=mark,
                                       within_margin=0,
                                       use_align=False,
                                       xalign=0.5,
                                       yalign=0.5)
