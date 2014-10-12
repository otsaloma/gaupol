# -*- coding: utf-8 -*-

# Copyright (C) 2006 Osmo Salomaa
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

"""Functions to calculate line lengths and to show them in widgets."""

import aeidon
import gaupol

from gi.repository import Gtk
from gi.repository import Pango


class _Ruler:

    """
    Measurer of line lengths in various units.

    The "sans" font (whatever it happens to be) is used for size calculations
    in em units, as subtitles are commonly shown in a some sans serif font.
    This is an approximation, but should be far more accurate than using
    characters, at least in Latin and other variable width character scripts.
    """

    def __init__(self):
        """Initialize a :class:`_Ruler` instance."""
        self._em_length = None
        self._layout = None
        self._length_unit = None
        self._update_em_length()
        self._update_length_unit()
        gaupol.conf.connect_notify("editor", "length_unit", self)

    def get_char_length(self, text, strip=False, floor=False):
        """Return length of `text` measured in characters."""
        text = (aeidon.RE_ANY_TAG.sub("", text) if strip else text)
        return len(text.replace("\n", " "))

    def get_char_lengths(self, text, strip=False, floor=False):
        """Return line lengths of `text` measured in characters."""
        text = (aeidon.RE_ANY_TAG.sub("", text) if strip else text)
        return tuple(len(x) for x in text.split("\n"))

    def get_em_length(self, text, strip=False, floor=False):
        """Return length of `text` measured in ems."""
        text = (aeidon.RE_ANY_TAG.sub("", text) if strip else text)
        text = text.replace("\n", " ")
        self._layout.set_text(text, -1)
        length = self._layout.get_size()[0] / self._em_length
        return (int(length) if floor else length)

    def get_em_lengths(self, text, strip=False, floor=False):
        """Return line lengths of `text` measured in ems."""
        text = (aeidon.RE_ANY_TAG.sub("", text) if strip else text)
        lengths = []
        for line in text.split("\n"):
            self._layout.set_text(line, -1)
            length = self._layout.get_size()[0] / self._em_length
            lengths.append(int(length) if floor else length)
        return tuple(lengths)

    def get_lengths(self, text, strip=False, floor=False):
        """Return line lengths of `text` measured in default units."""
        if self._length_unit == gaupol.length_units.CHAR:
            return self.get_char_lengths(text, strip, floor)
        if self._length_unit == gaupol.length_units.EM:
            return self.get_em_lengths(text, strip, floor)
        raise ValueError("Invalid length unit: {}"
                         .format(repr(self._length_unit)))

    def _on_conf_editor_notify_length_unit(self, *args):
        """Update the length function used."""
        self._update_length_unit()

    def _update_em_length(self):
        """Update the length of em based on font description size."""
        self._layout = Gtk.Label().get_layout().copy()
        font_desc = self._layout.get_context().get_font_description()
        font_desc.merge(Pango.FontDescription("sans"), True)
        self._layout.set_font_description(font_desc)
        self._em_length = font_desc.get_size()

    def _update_length_unit(self):
        """Update the length function used."""
        self._length_unit = gaupol.conf.editor.length_unit


_ruler = _Ruler()

def _on_text_view_draw(text_view, cairoc):
    """Calculate and show line lengths in text view margin."""
    # XXX: This doesn't seem to work with GTK+ 3.14.
    text_buffer = text_view.get_buffer()
    start, end = text_buffer.get_bounds()
    text = text_buffer.get_text(start, end, False)
    if not text: return
    lengths = get_lengths(text)
    layout = Pango.Layout(text_view.get_pango_context())
    layout.set_markup("\n".join(str(x) for x in lengths), -1)
    layout.set_alignment(Pango.Alignment.RIGHT)
    width = layout.get_pixel_size()[0]
    text_view.set_border_window_size(Gtk.TextWindowType.RIGHT, width+6)
    x, y = text_view.window_to_buffer_coords(Gtk.TextWindowType.RIGHT, 2, 4)
    x += text_view.get_border_width()
    style = text_view.get_style_context()
    Gtk.render_layout(style, cairoc, x, y, layout)

def connect_text_view(text_view):
    """Connect `text_view` to show line lengths in its margin."""
    context = text_view.get_pango_context()
    layout = Pango.Layout(context)
    layout.set_text("8", -1)
    width = layout.get_pixel_size()[0]
    text_view.set_border_window_size(Gtk.TextWindowType.RIGHT, width+6)
    handler_id = text_view.connect("draw", _on_text_view_draw)
    text_view.gaupol_ruler_handler_id = handler_id
    return handler_id

def disconnect_text_view(text_view):
    """Disconnect `text_view` from showing line lengths in its margin."""
    text_view.set_border_window_size(Gtk.TextWindowType.RIGHT, 0)
    if not hasattr(text_view, "gaupol_ruler_handler_id"): return
    handler_id = text_view.gaupol_ruler_handler_id
    del text_view.gaupol_ruler_handler_id
    return text_view.disconnect(handler_id)

def get_length_function(unit):
    """Return a function that returns text length in `unit`."""
    if unit == gaupol.length_units.CHAR:
        return _ruler.get_char_length
    if unit == gaupol.length_units.EM:
        return _ruler.get_em_length
    raise ValueError("Invalid length unit: {}"
                     .format(repr(unit)))

def get_lengths(text):
    """Return a sequence of floored line lengths without tags."""
    return _ruler.get_lengths(text, strip=True, floor=True)
