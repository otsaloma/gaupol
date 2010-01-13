# Copyright (C) 2009 Osmo Salomaa
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

"""Cell renderer for float data with three decimals."""

import gaupol
import gobject
import gtk

__all__ = ("FloatCellRenderer",)


class FloatCellRenderer(gtk.CellRendererText):

    """Cell renderer for float data with three decimals."""

    __gtype_name__ = "FloatCellRenderer"

    def __init__(self):
        """Initialize a FloatCellRenderer object."""

        gtk.CellRendererText.__init__(self)
        self._text = ""
        aeidon.util.connect(self, self, "notify::text")

    def _on_notify_text(self, *args):
        """Set markup by adding line lengths to text."""

        self._text = text = unicode(self.props.text)
        if not text: return
        has_comma = text.find(",") > 0
        text = text.replace(",", ".")
        text = "%.3f" % float(text)
        if has_comma:
            text = text.replace(".", ",")
        self.props.markup = gobject.markup_escape_text(text)
