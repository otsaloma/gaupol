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

    """Measurer of line lengths in various units."""

    def __init__(self):
        """Initialize a :class:`_Ruler` instance."""
        self._em_length = None
        self._label = Gtk.Label()
        self._update_em_length()

    def get_char_length(self, text, strip=False, floor=False):
        """Return length of `text` measured in characters."""
        text = aeidon.RE_ANY_TAG.sub("", text) if strip else text
        return len(text.replace("\n", " "))

    def get_em_length(self, text, strip=False, floor=False):
        """Return length of `text` measured in ems."""
        text = aeidon.RE_ANY_TAG.sub("", text) if strip else text
        self._label.set_text(text.replace("\n", " "))
        width = self._label.get_preferred_width()[1]
        length = width / self._em_length
        return int(length) if floor else length

    def _update_em_length(self):
        """Update the length of em based on font rendering."""
        text = "abcdefghijklmnopqrstuvwxyz"
        self._label.set_text(text)
        self._label.show()
        width = self._label.get_preferred_width()[1]
        # About 0.55 em per a-z average character.
        # https://bugzilla.gnome.org/show_bug.cgi?id=763589
        self._em_length = width / (0.55 * len(text))


_ruler = _Ruler()

def _on_text_view_draw(text_view, cairoc):
    """Calculate and show line lengths in text view margin."""
    text_buffer = text_view.get_buffer()
    start, end = text_buffer.get_bounds()
    text = text_buffer.get_text(start, end, False)
    if not text: return
    lengths = get_lengths(text)
    layout = Pango.Layout(text_view.get_pango_context())
    # XXX: Lines overlap if we don't set a spacing!?
    layout.set_spacing(2 * Pango.SCALE)
    layout.set_markup("\n".join(str(x) for x in lengths), -1)
    layout.set_alignment(Pango.Alignment.RIGHT)
    width = layout.get_pixel_size()[0]
    text_view.set_border_window_size(Gtk.TextWindowType.RIGHT, width + 6)
    x, y = text_view.window_to_buffer_coords(Gtk.TextWindowType.RIGHT, 2, 4)
    x += text_view.get_border_width()
    with aeidon.util.silent(AttributeError):
        # Top margin available since GTK 3.18.
        y += text_view.props.top_margin
    style = text_view.get_style_context()
    Gtk.render_layout(style, cairoc, x, y, layout)

def connect_text_view(text_view):
    """Connect `text_view` to show line lengths in its margin."""
    context = text_view.get_pango_context()
    layout = Pango.Layout(context)
    layout.set_text("8", -1)
    width = layout.get_pixel_size()[0]
    text_view.set_border_window_size(Gtk.TextWindowType.RIGHT, width + 6)
    handler_id = text_view.connect_after("draw", _on_text_view_draw)
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
    raise ValueError("Invalid length unit: {!r}"
                     .format(unit))

def get_lengths(text):
    """Return a sequence of floored line lengths without tags."""
    fun = get_length_function(gaupol.conf.editor.length_unit)
    return [fun(line, strip=True, floor=True) for line in text.split("\n")]
