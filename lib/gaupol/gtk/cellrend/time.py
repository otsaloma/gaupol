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


"""Cell renderer time data in format hh:mm:ss,sss."""


try:
    from psyco.classes import *
except ImportError:
    pass

import re

import gtk

from gaupol.gtk.cellrend.text import CellRendererText
from gaupol.gtk.entries.time  import TimeEntry


class CellRendererTime(CellRendererText):

    """Cell renderer time data in format hh:mm:ss,sss."""

    def __init__(self, *args):

        CellRendererText.__init__(self, *args)

    def _on_key_press_event(self, editor, event):
        """Cancel editing if Escape pressed."""

        keyname = gtk.gdk.keyval_name(event.keyval)

        if keyname == 'Escape':
            editor.remove_widget()
            self.emit('editing-canceled')
            return True

    def on_start_editing(self, event, widget, row, bg_area, cell_area, flags):
        """Initialize and return editor widget."""

        editor = TimeEntry()
        editor.set_has_frame(False)
        editor.set_activates_default(True)
        editor.set_size_request(-1, cell_area.height)
        editor.modify_font(self.font_description)
        editor.set_text(self.text or u'')

        editor.connect('editing-done', self.on_editing_done, row)
        editor.connect('key-press-event', self._on_key_press_event)

        editor.grab_focus()
        editor.select_region(0, -1)
        editor.show()
        return editor


if __name__ == '__main__':

    import gobject
    from gaupol.test import Test

    class TestCellRendererInteger(Test):

        def test_init(self):

            tree_view = gtk.TreeView()
            tree_view.set_headers_visible(False)
            store = gtk.ListStore(gobject.TYPE_STRING)
            store.append(['00:01:22,333'])
            tree_view.set_model(store)

            cell_renderer = CellRendererTime()
            cell_renderer.set_editable(True)
            tree_view_column = gtk.TreeViewColumn('', cell_renderer, text=0)
            tree_view.append_column(tree_view_column)

            window = gtk.Window()
            window.connect('delete-event', gtk.main_quit)
            window.set_position(gtk.WIN_POS_CENTER)
            window.set_default_size(200, 50)
            window.add(tree_view)
            window.show_all()
            gtk.main()

    TestCellRendererInteger().run()
