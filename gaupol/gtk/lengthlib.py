# Copyright (C) 2006-2007 Osmo Salomaa
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


"""Functions to calculate line lengths and to show them in widgets.

Module variables:

    _COUNTER: Instance of _Counter used
    RE_TAG:   Regular expression for a tag of any format
"""


from __future__ import division

import gtk
import pango
import re

from gaupol.gtk import conf, cons


RE_TAG = re.compile(r"(^[/\\_]|<.*?>|\{.*?\})")


class _Counter(object):

    """Line length counter.

    Instance variables:

        _layout:   pango.Layout used to determine pixel sizes
        em_length: Length of the letter 'M' in the current font used
    """

    def __init__(self):

        self._layout     = None
        self.em_length   = None
        self.get_lengths = None

        self._update_em_length()
        self._update_length_func()
        self._init_signal_handlers()

    def _init_signal_handlers(self):
        """Initialize signal handlers."""

        for option in ("font", "length_unit", "use_default_font"):
            conf.connect(self, "editor", option)

    def _on_conf_editor_notify_font(self, *args):
        """Update the length of em."""

        self._update_em_length()

    def _on_conf_editor_notify_length_unit(self, *args):
        """Update the length function used."""

        self._update_length_func()

    def _on_conf_editor_notify_use_default_font(self, *args):
        """Update the length of em."""

        self._update_em_length()

    def _update_em_length(self):
        """Update the length of em."""

        self._layout = gtk.Label().get_layout().copy()
        if not conf.editor.use_default_font:
            font_desc = pango.FontDescription(conf.editor.font)
            self._layout.set_font_description(font_desc)
        self._layout.set_text("M")
        self.em_length = self._layout.get_pixel_size()[0]

    def _update_length_func(self):
        """Update the length function used."""

        if conf.editor.length_unit == cons.LENGTH_UNIT.CHAR:
            self.get_lengths = self.get_char_lengths
        elif conf.editor.length_unit == cons.LENGTH_UNIT.EM:
            self.get_lengths = self.get_em_lengths

    def get_char_lengths(self, text, strip, floor):
        """Get a list of line lengths measured in characters."""

        if strip:
            text = RE_TAG.sub("", text)
        return [len(x) for x in text.split("\n")]

    def get_em_lengths(self, text, strip, floor):
        """Get a list of line lengths measured in ems."""

        if strip:
            text = RE_TAG.sub("", text)
        lengths = []
        for line in text.split("\n"):
            self._layout.set_text(line)
            length = self._layout.get_pixel_size()[0] / self.em_length
            if floor:
                length = int(length)
            lengths.append(length)
        return lengths


_COUNTER = _Counter()


def _on_text_view_expose_event(text_view, event):
    """Calculate and show line lengths in the margin."""

    text_buffer = text_view.get_buffer()
    text = text_buffer.get_text(*text_buffer.get_bounds())
    if not text:
        return
    lengths = get_lengths(text)
    layout = pango.Layout(text_view.get_pango_context())
    layout.set_markup("\n".join([str(x) for x in lengths]))
    layout.set_alignment(pango.ALIGN_RIGHT)

    width = layout.get_pixel_size()[0]
    text_view.set_border_window_size(gtk.TEXT_WINDOW_RIGHT, width + 4)
    y = -text_view.window_to_buffer_coords(gtk.TEXT_WINDOW_RIGHT, 2, 0)[1]
    window = text_view.get_window(gtk.TEXT_WINDOW_RIGHT)
    window.clear()
    text_view.style.paint_layout(
        window, gtk.STATE_NORMAL, True, None, text_view, None, 2, y, layout)

def connect_text_view(text_view):
    """Connect text view to show line lengths in the margin."""

    layout = pango.Layout(text_view.get_pango_context())
    layout.set_text("8")
    width = layout.get_pixel_size()[0]
    text_view.set_border_window_size(gtk.TEXT_WINDOW_RIGHT, width + 4)
    handler_id = text_view.connect("expose-event", _on_text_view_expose_event)
    text_view.set_data("lengthlib_handler_id", handler_id)
    return handler_id

def disconnect_text_view(text_view):
    """Disconnect text view from showing line lengths in the margin."""

    text_view.set_border_window_size(gtk.TEXT_WINDOW_RIGHT, 0)
    handler_id = text_view.get_data("lengthlib_handler_id")
    text_view.set_data("lengthlib_handler_id", None)
    return text_view.disconnect(handler_id)

def func(text):
    """Get the length (float) of text without stripping tags.

    This is suitable for use as liner length_func.
    """
    return sum(_COUNTER.get_lengths(text, False, False))

def get_lengths(text):
    """Get a list of floored line lengths without tags."""

    return _COUNTER.get_lengths(text, True, True)
