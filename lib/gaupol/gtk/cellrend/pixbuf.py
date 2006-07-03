# Copyright (C) 2006 Osmo Salomaa
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


"""Cell renderer for sub pictures."""


import os

import gobject
import gtk

from gaupol.gtk.cellrend.multiline import CellRendererMultiline
from gaupol.gtk.util               import conf


class CellRendererPixbuf(CellRendererMultiline):

    """Cell renderer for sub pictures."""

    __gproperties__ = {
        'directory': (
            gobject.TYPE_STRING,
            'directory',
            'directory',
            '',
            gobject.PARAM_READWRITE
        ),
        'pixbuf': (
            gobject.TYPE_STRING,
            'pixbuf',
            'pixbuf',
            '',
            gobject.PARAM_READWRITE
        ),
    }

    def __init__(self):

        CellRendererMultiline.__init__(self)

        self.directory = conf.srtx.directory
        self.pixbuf    = None

    def _set_pixbuf(self, text):
        """Set pixbuf based on text."""

        self.pixbuf = None
        if text.endswith('.txt'):
            text = text[:-4]
        path = os.path.join(self.directory, text)
        if os.path.isfile(path):
            try:
                pixbuf = gtk.gdk.pixbuf_new_from_file(path)
            except gobject.GError:
                print 'Failed to load image file "%s".' % text
                return
        else:
            return

        width = float(pixbuf.get_width())
        if width > conf.srtx.max_width:
            height = pixbuf.get_height()
            height = int((conf.srtx.max_width / width) * height)
            pixbuf = pixbuf.scale_simple(
                conf.srtx.max_width, height, gtk.gdk.INTERP_BILINEAR)
        self.pixbuf = pixbuf

    def do_set_property(self, prop, value):
        """Set value of property."""

        CellRendererMultiline.do_set_property(self, prop, value)

        if prop.name == 'text':
            self._set_pixbuf(value)

    def on_get_size(self, widget, cell_area):
        """Get cell size."""

        if self.pixbuf is None:
            return 0, 0, 0, 0
        return 0, 0, self.pixbuf.get_width(), self.pixbuf.get_height()

    def on_render(self, window, widget, bg_area, cell_area, exp_area, flags):
        """Render cell."""

        if self.pixbuf is None:
            return

        window.draw_pixbuf(
            None,
            self.pixbuf,
            0,
            0,
            cell_area.x,
            cell_area.y,
            self.pixbuf.get_width(),
            self.pixbuf.get_height(),
            gtk.gdk.RGB_DITHER_NORMAL,
            0,
            0
        )
