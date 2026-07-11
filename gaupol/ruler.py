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
# along with this program. If not, see <https://www.gnu.org/licenses/>.

"""Functions to calculate line lengths and to show them in widgets."""

import aeidon
import gaupol

from gi.repository import GObject
from gi.repository import Graphene
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
        width = self._label.measure(Gtk.Orientation.HORIZONTAL, -1).natural
        length = width / self._em_length
        return int(length) if floor else length

    def _update_em_length(self):
        """Update the length of em based on font rendering."""
        text = "abcdefghijklmnopqrstuvwxyz"
        self._label.set_text(text)
        width = self._label.measure(Gtk.Orientation.HORIZONTAL, -1).natural
        # About 0.55 em per a-z average character.
        # https://bugzilla.gnome.org/show_bug.cgi?id=763589
        self._em_length = width / (0.55 * len(text))

_ruler = _Ruler()

class _Margin(Gtk.Widget):

    """Widget that shows line lengths in a text view's right gutter."""

    def __init__(self, text_view):
        """Initialize a :class:`_Margin` instance."""
        GObject.GObject.__init__(self)
        self._handlers = []
        self._text_view = text_view
        self._vadjustment = None
        text_buffer = text_view.get_buffer()
        handler_id = text_buffer.connect("changed", self._on_buffer_changed)
        self._handlers.append((text_buffer, handler_id))
        handler_id = text_view.connect(
            "notify::vadjustment", self._on_notify_vadjustment)
        self._handlers.append((text_view, handler_id))
        self._on_notify_vadjustment()
        self._update_width()

    def disconnect_all(self):
        """Disconnect all signal handlers connected to other objects."""
        for obj, handler_id in self._handlers:
            obj.disconnect(handler_id)
        self._handlers = []
        if self._vadjustment is not None:
            self._vadjustment.disconnect(self._vadjustment_handler)
            self._vadjustment = None

    def do_snapshot(self, snapshot):
        """Draw line lengths aligned with the text view's lines."""
        text_view = self._text_view
        text_buffer = text_view.get_buffer()
        start, end = text_buffer.get_bounds()
        text = text_buffer.get_text(start, end, False)
        if not text: return
        lengths = get_lengths(text)
        color = self.get_color()
        layout = Pango.Layout(text_view.get_pango_context())
        width = self.get_width()
        for i in range(len(lengths)):
            ok, itr = text_buffer.get_iter_at_line(i)
            if not ok: break
            location = text_view.get_iter_location(itr)
            y = text_view.buffer_to_window_coords(
                Gtk.TextWindowType.RIGHT, 0, location.y)[1]
            layout.set_text(str(lengths[i]), -1)
            point = Graphene.Point()
            point.init(width - layout.get_pixel_size()[0] - 4, y)
            snapshot.save()
            snapshot.translate(point)
            snapshot.append_layout(layout, color)
            snapshot.restore()

    def _on_buffer_changed(self, *args):
        """Update width and redraw when text changes."""
        self._update_width()
        self.queue_draw()

    def _on_notify_vadjustment(self, *args):
        """Redraw on scrolling, also if the adjustment is replaced."""
        if self._vadjustment is not None:
            self._vadjustment.disconnect(self._vadjustment_handler)
        self._vadjustment = self._text_view.get_vadjustment()
        if self._vadjustment is None: return
        self._vadjustment_handler = self._vadjustment.connect(
            "value-changed", lambda *args: self.queue_draw())

    def _update_width(self):
        """Request enough width for the widest line length."""
        text_buffer = self._text_view.get_buffer()
        start, end = text_buffer.get_bounds()
        text = text_buffer.get_text(start, end, False)
        layout = Pango.Layout(self._text_view.get_pango_context())
        layout.set_text(str(max(get_lengths(text))), -1)
        self.set_size_request(layout.get_pixel_size()[0] + 6, -1)

def connect_text_view(text_view):
    """Connect `text_view` to show line lengths in its margin."""
    if hasattr(text_view, "gaupol_ruler_margin"): return
    margin = _Margin(text_view)
    text_view.set_gutter(Gtk.TextWindowType.RIGHT, margin)
    text_view.gaupol_ruler_margin = margin

def disconnect_text_view(text_view):
    """Disconnect `text_view` from showing line lengths in its margin."""
    if not hasattr(text_view, "gaupol_ruler_margin"): return
    text_view.gaupol_ruler_margin.disconnect_all()
    del text_view.gaupol_ruler_margin
    text_view.set_gutter(Gtk.TextWindowType.RIGHT, None)

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
