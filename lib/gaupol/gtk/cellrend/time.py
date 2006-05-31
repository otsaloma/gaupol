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


"""Cell renderer time data in format hh:mm:ss,sss."""


import gtk

from gaupol.gtk.cellrend.text import CellRendererText
from gaupol.gtk.entry.time    import EntryTime


class CellRendererTime(CellRendererText):

    """Cell renderer time data in format hh:mm:ss,sss."""

    def on_key_press_event(self, editor, event):
        """Cancel editing if Escape pressed."""

        keyname = gtk.gdk.keyval_name(event.keyval)
        if keyname == 'Escape':
            editor.remove_widget()
            self.emit('editing-canceled')
            return True

    def on_start_editing(self, event, widget, row, bg_area, cell_area, flags):
        """Initialize and return editor widget."""

        editor = EntryTime()
        editor.set_has_frame(False)
        editor.set_activates_default(True)
        editor.modify_font(self.font_desc)
        editor.set_text(self.text or u'')

        editor.connect('editing-done', self.on_editing_done, row)
        editor.connect('key-press-event', self.on_key_press_event)

        editor.grab_focus()
        editor.select_region(0, -1)
        editor.show()
        return editor
