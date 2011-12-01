# Copyright (C) 2009-2010 Osmo Salomaa
#
# This file is part of Gaupol.
#
# Gaupol is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# Gaupol is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# Gaupol. If not, see <http://www.gnu.org/licenses/>.

"""Cell renderer for float data with fixed precision."""

import aeidon
import glib
from gi.repository import Gtk

__all__ = ("FloatCellRenderer",)


class FloatCellRenderer(Gtk.CellRendererText):

    """Cell renderer for float data with fixed precision."""

    __gtype_name__ = "FloatCellRenderer"

    def __init__(self, format="{:.3f}"):
        """Initialize a :class:`FloatCellRenderer` object."""
        GObject.GObject.__init__(self)
        self._format = format
        self._text = ""
        aeidon.util.connect(self, self, "notify::text")

    def _on_notify_text(self, *args):
        """Cut decimals to fixed precision."""
        self._text = text = str(self.props.text)
        if not text: return
        has_comma = text.find(",") > 0
        text = text.replace(",", ".")
        text = self._format.format(float(text))
        text = (text.replace(".", ",") if has_comma else text)
        self.props.markup = glib.markup_escape_text(text)
