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


"""Generic custom CellRenderer for cells containing text."""


try:
    from psyco.classes import *
except ImportError:
    pass

import gobject
import gtk
import pango


class CustomCellRenderer(gtk.GenericCellRenderer):

    """Generic custom CellRenderer for cells containing text."""

    __gproperties__ = {
        'font': (
            gobject.TYPE_STRING, 'font', 'font', '',
            gobject.PARAM_READWRITE
        ),
        'font_desc': (
            gobject.TYPE_STRING, 'font description', 'font description', '',
            gobject.PARAM_READWRITE
        ),
        'text': (
            gobject.TYPE_STRING, 'text', 'text', '',
            gobject.PARAM_READWRITE
        ),
    }
    
    __gsignals__ = {
        'edited': (
            gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE,
            (gobject.TYPE_STRING, gobject.TYPE_INT)
        )
    }

    property_names = __gproperties__.keys()

    def __init__(self):
    
        self.__gobject_init__()

        self.font      = None
        self.font_desc = None
        self.text      = None

    def do_get_property(self, property):
        """
        Get value of property.
        
        Raise AttributeError, if property does not exist.
        """
        name = property.name
        
        if name in self.property_names:
            return self.__dict__[name]
        else:
            raise AttributeError('No property named "%s".' % name)

    def do_set_property(self, property, value):
        """
        Set value of property.
        
        Raise AttributeError, if property does not exist.
        """
        name = property.name

        if name in self.property_names:
            self.__dict__[name] = value
        else:
            raise AttributeError('No property named "%s".' % name)
            
    def _get_layout(self, widget):
        """Get the Pango layout for the cell."""

        context = widget.get_pango_context()
        
        # Get the default font description.
        font_desc = context.get_font_description()

        # Create custom font description and merge that with the default.
        custom_font_desc = pango.FontDescription(self.font)
        font_desc.merge(custom_font_desc, True)

        layout = pango.Layout(context)
        layout.set_font_description(font_desc)

        # Do not wrap text.
        layout.set_width(-1)
        
        layout.set_text(self.text or '')

        self.font_desc = font_desc
        return layout

    def on_editing_done(self, editor, row):
        """End editing of the cell."""
        
        self.emit('edited', editor.get_text(), int(row))

    def on_get_size(self, widget, cell_area):
        """
        Get size of the cell.

        Return: X offset, Y offset, width, height
        """
        # The following size calculations have been tested so that the cell
        # should be the same size as a CellRendererText cell with same amount
        # of rows.

        xpad = 2
        ypad = 2
        
        xalign = 0
        yalign = 0.5

        layout = self._get_layout(widget)
        width, height = layout.get_pixel_size()

        if cell_area is not None:
        
            x_offset = xalign * (cell_area.width  - width )
            y_offset = yalign * (cell_area.height - height)

            # Offsets should be at least the size of padding.
            x_offset = max(x_offset, xpad)
            y_offset = max(y_offset, ypad)

            # Offsets should have integer values.
            x_offset = int(round(x_offset, 0))
            y_offset = int(round(y_offset, 0))

        else:
        
            x_offset = xpad
            y_offset = ypad

        width  = width  + (xpad * 2)
        height = height + (ypad * 2)

        return x_offset, y_offset, width, height

    def on_render(self, window, widget, bg_area, cell_area, exp_area, flags):
        """Render the cell."""
        
        x_offset, y_offset, width, height = self.get_size(widget, cell_area)
        layout = self._get_layout(widget)

        # Determine state of the cell.
        if flags & gtk.CELL_RENDERER_SELECTED:
            if widget.get_property('has-focus'):
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
        """Set editability of cell."""
        
        if editable:
            mode = gtk.CELL_RENDERER_MODE_EDITABLE
        else:
            mode = gtk.CELL_RENDERER_MODE_ACTIVATABLE
            
        self.set_property('mode', mode)


gobject.type_register(CustomCellRenderer)
