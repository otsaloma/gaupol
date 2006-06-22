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


"""Dialogs for selecting character encodings."""


from gettext import gettext as _

import gobject
import gtk

from gaupol.base.util import enclib
from gaupol.gtk.util  import config, gtklib


class EncodingDialog(object):

    """Dialog for selecting a character encoding."""

    def __init__(self, parent):

        glade_xml = gtklib.get_glade_xml('encoding-dialog')
        self._dialog    = glade_xml.get_widget('dialog')
        self._tree_view = glade_xml.get_widget('tree_view')

        self._init_tree_view()
        self._init_sizes()
        self._dialog.set_transient_for(parent)
        self._dialog.set_default_response(gtk.RESPONSE_OK)

    def _init_sizes(self):
        """Initialize widget sizes."""

        width, height = gtklib.get_tree_view_size(self._tree_view)
        width  = width  + 52 + gtklib.EXTRA
        height = height + 84 + gtklib.EXTRA
        gtklib.resize_dialog(self._dialog, width, height, 0.5, 0.5)

    def _init_tree_view(self):
        """Initialize tree view."""

        store = gtk.ListStore(gobject.TYPE_STRING, gobject.TYPE_STRING)
        self._tree_view.set_model(store)

        selection = self._tree_view.get_selection()
        selection.set_mode(gtk.SELECTION_SINGLE)
        selection.unselect_all()

        tree_col = gtk.TreeViewColumn
        for i, column in enumerate([
            tree_col(_('Description'), gtk.CellRendererText(), text=0),
            tree_col(_('Encoding')   , gtk.CellRendererText(), text=1),
        ]):
            self._tree_view.append_column(column)
            column.set_resizable(True)
            column.set_clickable(True)
            column.set_sort_column_id(i)
        store.set_sort_column_id(0, gtk.SORT_ASCENDING)
        self._tree_view.columns_autosize()

        for entry in enclib.get_valid_encodings():
            store.append([entry[2], entry[1]])

    def destroy(self):
        """Destroy dialog."""

        self._dialog.destroy()

    def get_encoding(self):
        """
        Get selected encoding.

        Return name or None.
        """
        selection = self._tree_view.get_selection()
        store, rows = selection.get_selected_rows()
        if rows:
            return enclib.get_python_name(store[rows[0]][1])
        return None

    def run(self):
        """Run dialog."""

        self._dialog.show()
        self._tree_view.grab_focus()
        return self._dialog.run()


class AdvancedEncodingDialog(EncodingDialog):

    """Dialog for selecting character encodings."""

    def _init_tree_view(self):
        """Initialize tree view."""

        store = gtk.ListStore(
            gobject.TYPE_STRING,gobject.TYPE_STRING, gobject.TYPE_BOOLEAN)
        self._tree_view.set_model(store)

        selection = self._tree_view.get_selection()
        selection.set_mode(gtk.SELECTION_SINGLE)
        selection.unselect_all()

        tree_col = gtk.TreeViewColumn
        cr_toggle = gtk.CellRendererToggle()
        cr_toggle.connect('toggled', self._on_tree_view_cell_toggled)
        for i, column in enumerate([
            tree_col(_('Description') , gtk.CellRendererText(), text  =0),
            tree_col(_('Encoding')    , gtk.CellRendererText(), text  =1),
            tree_col(_('Show In Menu'), cr_toggle             , active=2),
        ]):
            self._tree_view.append_column(column)
            column.set_resizable(True)
            column.set_clickable(True)
            column.set_sort_column_id(i)
        store.set_sort_column_id(0, gtk.SORT_ASCENDING)
        self._tree_view.columns_autosize()

        visible = config.encoding.visibles
        for entry in enclib.get_valid_encodings():
            store.append([entry[2], entry[1], entry[0] in visible])

    def _on_tree_view_cell_toggled(self, cell_renderer, row):
        """Toggle visibility value."""

        store = self._tree_view.get_model()
        store[row][2] = not store[row][2]

    def get_visible_encodings(self):
        """Get encodings chosen to be visible."""

        visible = []
        store = self._tree_view.get_model()
        for row in range(len(store)):
            if store[row][2]:
                visible.append(enclib.get_python_name(store[row][1]))
        return visible
