# Copyright (C) 2005 Osmo Salomaa
#
# This file is part of Gaupol.
#
# Gaupol is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Gaupol is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Gaupol; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA


"""Custom cell renderer for text data."""


try:
    from psyco.classes import *
except ImportError:
    pass

import gobject
import gtk
import pango


class CellRendererText(gtk.GenericCellRenderer):

    """Custom cell renderer for text data."""

    __gtype_name__ = 'CellRendererText'

    __gproperties__ = {
        'font': (
            gobject.TYPE_STRING,
            'font',
            'font',
            '',
            gobject.PARAM_READWRITE
        ),
        'font_description': (
            gobject.TYPE_STRING,
            'font description',
            'font description',
            '',
            gobject.PARAM_READWRITE
        ),
        'text': (
            gobject.TYPE_STRING,
            'text',
            'text',
            '',
            gobject.PARAM_READWRITE
        ),
    }

    __gsignals__ = {
        'edited': (
            gobject.SIGNAL_RUN_LAST,
            gobject.TYPE_NONE,
            (gobject.TYPE_STRING, gobject.TYPE_INT)
        )
    }

    property_names = __gproperties__.keys()

    def __init__(self):

        gtk.GenericCellRenderer.__init__(self)

        self.font             = None
        self.font_description = None
        self.text             = None

        self.x_align   = 0
        self.y_align   = 0.5
        self.x_padding = 2
        self.y_padding = 2

    def do_get_property(self, prop):
        """Get value of property."""

        getattr(self, prop.name)

    def do_set_property(self, prop, value):
        """Set value of property."""

        setattr(self, prop.name, value)

    def _get_layout(self, widget):
        """Get a pango layout."""

        context = widget.get_pango_context()

        # Get the default font description.
        font_description = context.get_font_description()

        # Create custom font description and merge that with the default.
        custom_font_description = pango.FontDescription(self.font)
        font_description.merge(custom_font_description, True)

        layout = pango.Layout(context)
        layout.set_font_description(font_description)
        layout.set_text(self.text or u'')

        self.font_description = font_description
        return layout

    def on_editing_done(self, editor, row):
        """End editing."""

        self.emit('edited', editor.get_text(), int(row))

    def on_get_size(self, widget, cell_area):
        """
        Get size cell size.

        Return X offset, Y offset, width, height.
        """
        layout = self._get_layout(widget)
        width, height = layout.get_pixel_size()

        # With cell contents being left aligned, x-offset should equal
        # x-padding.
        x_offset = self.x_padding

        # With cell contents being center aligned vertically, the y-offset
        # needs to be calculated based on the actual content height.
        if cell_area is not None:
            y_offset = self.y_align * (cell_area.height - height)
            y_offset = max(int(round(y_offset, 0)), self.y_padding)
        else:
            y_offset = self.y_padding

        width  = width  + (self.x_padding * 2)
        height = height + (self.y_padding * 2)

        return x_offset, y_offset, width, height

    def on_render(self, window, widget, bg_area, cell_area, exp_area, flags):
        """Render cell."""

        x_offset, y_offset, width, height = self.get_size(widget, cell_area)
        layout = self._get_layout(widget)

        # Determine cell state.
        if flags & gtk.CELL_RENDERER_SELECTED:
            if widget.props.has_focus:
                state = gtk.STATE_SELECTED
            else:
                state = gtk.STATE_ACTIVE
        else:
            state = gtk.STATE_NORMAL

        widget.style.paint_layout(
            window, state, True, cell_area, widget, 'custom cell',
            cell_area.x + x_offset, cell_area.y + y_offset, layout
        )

    def set_editable(self, editable):
        """Set cell editability."""

        if editable:
            mode = gtk.CELL_RENDERER_MODE_EDITABLE
        else:
            mode = gtk.CELL_RENDERER_MODE_ACTIVATABLE

        self.props.mode = mode
