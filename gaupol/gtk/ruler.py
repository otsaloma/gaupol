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


"""Functions to calculate line lengths and to show them in widgets."""


from __future__ import division

import gaupol.gtk
import gtk
import pango
import re


class _Ruler(object):

    """Measurer of line lengths in various units.

    Instance variables:
     * _em_length: Point size of the font used in pango units
     * _layout: pango.Layout used for text length calculations
    """

    _re_tag = re.compile(r"(^[/\\_]|<.*?>|\{.*?\})")

    # pylint: disable-msg=W0231
    def __init__(self):

        self._em_length = None
        self._layout = None
        self.get_lengths = None

        self._update_em_length()
        self._update_length_func()
        self._init_signal_handlers()

    def _init_signal_handlers(self):
        """Initialize signal handlers."""

        gaupol.gtk.conf.connect(self, "editor", "length_unit")

    def _on_conf_editor_notify_length_unit(self, *args):
        """Update the length function used."""

        self._update_length_func()

    def _update_em_length(self):
        """Update the length of em based on font description size."""

        self._layout = gtk.Label().get_layout().copy()
        font_desc = self._layout.get_context().get_font_description()
        custom_font_desc = pango.FontDescription("sans")
        font_desc.merge(custom_font_desc, True)
        self._layout.set_font_description(font_desc)
        self._em_length = font_desc.get_size()

    def _update_length_func(self):
        """Update the length function used."""

        length_unit = gaupol.gtk.conf.editor.length_unit
        if length_unit == gaupol.gtk.LENGTH_UNIT.CHAR:
            self.get_lengths = self.get_char_lengths
        elif length_unit == gaupol.gtk.LENGTH_UNIT.EM:
            self.get_lengths = self.get_em_lengths

    def get_char_lengths(self, text, strip, floor):
        """Get a list of line lengths measured in characters."""

        text = (self._re_tag.sub("", text) if strip else text)
        return [len(x) for x in text.split("\n")]

    def get_em_lengths(self, text, strip, floor):
        """Get a list of line lengths measured in ems."""

        lengths = []
        text = (self._re_tag.sub("", text) if strip else text)
        for line in text.split("\n"):
            self._layout.set_text(line)
            length = self._layout.get_size()[0] / self._em_length
            length = (int(length) if floor else length)
            lengths.append(length)
        return lengths


_ruler = _Ruler()

@gaupol.util.asserted_return
def _on_text_view_expose_event(text_view, event):
    """Calculate and show line lengths in the margin."""

    text_buffer = text_view.get_buffer()
    bounds = text_buffer.get_bounds()
    text = text_buffer.get_text(*bounds)
    assert text
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

    context = text_view.get_pango_context()
    layout = pango.Layout(context)
    layout.set_text("8")
    width = layout.get_pixel_size()[0]
    text_view.set_border_window_size(gtk.TEXT_WINDOW_RIGHT, width + 4)
    handler_id = text_view.connect("expose-event", _on_text_view_expose_event)
    text_view.set_data("lengthlib_handler_id", handler_id)
    return handler_id

def disconnect_text_view_require(text_view):
    assert text_view.get_data("lengthlib_handler_id") is not None

@gaupol.util.contractual
def disconnect_text_view(text_view):
    """Disconnect text view from showing line lengths in the margin."""

    text_view.set_border_window_size(gtk.TEXT_WINDOW_RIGHT, 0)
    handler_id = text_view.get_data("lengthlib_handler_id")
    text_view.set_data("lengthlib_handler_id", None)
    return text_view.disconnect(handler_id)

def func(text):
    """Get the length of text (as float) without stripping tags."""

    return sum(_ruler.get_lengths(text, False, False))

def get_lengths(text):
    """Get a list of floored line lengths without tags."""

    return _ruler.get_lengths(text, True, True)
