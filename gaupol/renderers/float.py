# -*- coding: utf-8 -*-

# Copyright (C) 2009 Osmo Salomaa
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

"""Cell renderer for float data with fixed precision."""

import aeidon
import gaupol
import re

from gi.repository import GLib
from gi.repository import GObject
from gi.repository import Gtk

__all__ = ("FloatCellRenderer",)


class FloatCellRenderer(Gtk.CellRendererText):

    """Cell renderer for float data with fixed precision."""

    __gtype_name__ = "FloatCellRenderer"

    def __init__(self, format="{:.3f}"):
        """Initialize a :class:`FloatCellRenderer` instance."""
        GObject.GObject.__init__(self)
        self._format = format
        aeidon.util.connect(self, self, "notify::text")
        aeidon.util.connect(self, self, "edited")
        aeidon.util.connect(self, self, "editing-started")

    def _on_edited(self, renderer, path, text):
        """Check `text` for validity before sending onwards."""
        if re.match(r"^[+-]?(\d+[,.]?\d*|\d*[,.]?\d+)$", text) is None:
            renderer.stop_emission("edited")
            renderer.stop_editing(True)

    def _on_editing_started(self, renderer, editor, path):
        """Set `editor` to use same font as `self`."""
        gaupol.style.use_font(editor, "custom")

    def _on_notify_text(self, *args):
        """Cut decimals to fixed precision."""
        # Since GTK 3.6, the notify::text signal seems to get
        # emitted insanely often even if text hasn't changed at
        # all. Let's try to keep this callback as fast as possible.
        self.props.markup = self._text_to_markup(self.props.text)

    @aeidon.deco.memoize(1000)
    def _text_to_markup(self, text):
        """Return `text` renderer as markup for display."""
        if not text: return ""
        has_comma = text.find(",") > 0
        if has_comma:
            text = text.replace(",", ".")
        text = self._format.format(float(text))
        if has_comma:
            text = text.replace(".", ",")
        return GLib.markup_escape_text(text)
