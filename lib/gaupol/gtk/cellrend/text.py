# Copyright (C) 2005-2006 Osmo Salomaa
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


"""Base class for cell renderers for text data."""


import gobject
import gtk
import pango


class CellRendererText(gtk.GenericCellRenderer):

    """
    Base class for cell renderers for text data.

    Instance variables:

        font:      Font string, e.g. 'Sans 9'
        font_desc: pango.FontDescription
        text:      String

    """

    __gproperties__ = {
        'font': (
            gobject.TYPE_STRING,
            'font',
            'font',
            '',
            gobject.PARAM_READWRITE
        ),
        'font_desc': (
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

    def __init__(self):

        gtk.GenericCellRenderer.__init__(self)

        self.font      = None
        self.font_desc = None
        self.text      = None

    def _get_layout(self, widget):
        """Get Pango layout."""

        context = widget.get_pango_context()
        font_desc = context.get_font_description()
        custom_font_desc = pango.FontDescription(self.font)
        font_desc.merge(custom_font_desc, True)
        self.font_desc = font_desc

        layout = pango.Layout(context)
        layout.set_font_description(font_desc)
        layout.set_text(self.text or u'')
        return layout

    def do_get_property(self, prop):
        """Get value of property."""

        getattr(self, prop.name)

    def do_set_property(self, prop, value):
        """Set value of property."""

        setattr(self, prop.name, value)

    def on_editing_done(self, editor, row):
        """End editing."""

        self.emit('edited', editor.get_text(), int(row))

    def on_get_size(self, widget, cell_area):
        """
        Get cell size.

        Size calculation assumes left- and top-aligned content.
        Return X offset, Y offset, width, height.
        """
        layout = self._get_layout(widget)
        width, height = layout.get_pixel_size()
        return 2, 2, width + 4, height + 4

    def on_render(self, window, widget, bg_area, cell_area, exp_area, flags):
        """Render cell."""

        x_offset, y_offset = self.get_size(widget, cell_area)[:2]

        if flags & gtk.CELL_RENDERER_SELECTED:
            if widget.props.has_focus:
                state = gtk.STATE_SELECTED
            else:
                state = gtk.STATE_ACTIVE
        else:
            state = gtk.STATE_NORMAL

        widget.style.paint_layout(
            window,
            state,
            True,
            cell_area,
            widget,
            'text cell',
            cell_area.x + x_offset,
            cell_area.y + y_offset,
            self._get_layout(widget)
        )

    def on_start_editing(self, event, widget, row, bg_area, cell_area, flags):
        """Initialize and return editor widget."""

        raise NotImplementedError

    def set_editable(self, editable):
        """Set cell editability."""

        if editable:
            self.props.mode = gtk.CELL_RENDERER_MODE_EDITABLE
        else:
            self.props.mode = gtk.CELL_RENDERER_MODE_ACTIVATABLE
