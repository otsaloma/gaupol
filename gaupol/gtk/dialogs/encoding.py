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


import gobject
import gtk

from gaupol import enclib
from gaupol.gtk import conf, util
from gaupol.gtk.i18n import _
from .glade import GladeDialog


class EncodingDialog(GladeDialog):

    """Dialog for selecting a character encoding.

    Instance variables:

        _tree_view: gtk.TreeView
    """

    def __init__(self, parent):

        GladeDialog.__init__(self, "encoding-dialog")

        self._tree_view = self._glade_xml.get_widget("tree_view")

        self._init_tree_view()
        self._init_signal_handlers()
        self._init_sizes()
        self._dialog.set_transient_for(parent)
        self._dialog.set_default_response(gtk.RESPONSE_OK)

    def _init_sizes(self):
        """Initialize widget sizes."""

        width, height = util.get_tree_view_size(self._tree_view)
        width = width + 52 + util.EXTRA
        height = height + 84 + util.EXTRA
        util.resize_dialog(self._dialog, width, height, 0.5, 0.5)

    def _init_signal_handlers(self):
        """Initialize signal handlers."""

        def respond(*args):
            self.response(gtk.RESPONSE_OK)
        self._tree_view.connect("row-activated", respond)

    def _init_tree_view(self):
        """Initialize the tree view."""

        self._tree_view.columns_autosize()
        selection = self._tree_view.get_selection()
        selection.set_mode(gtk.SELECTION_SINGLE)
        store = gtk.ListStore(*(gobject.TYPE_STRING,) * 2)
        self._tree_view.set_model(store)

        renderer = gtk.CellRendererText()
        column = gtk.TreeViewColumn(_("Description"), renderer, text=0)
        self._tree_view.append_column(column)

        renderer = gtk.CellRendererText()
        column = gtk.TreeViewColumn(_("Encoding"), renderer, text=1)
        self._tree_view.append_column(column)

        for i, column in enumerate(self._tree_view.get_columns()):
            column.set_resizable(True)
            column.set_clickable(True)
            column.set_sort_column_id(i)

        store.set_sort_column_id(0, gtk.SORT_ASCENDING)
        for item in enclib.get_valid_encodings():
            store.append([item[2], item[1]])

    def get_encoding(self):
        """Get the selected encoding or None."""

        selection = self._tree_view.get_selection()
        store, itr = selection.get_selected()
        if itr is not None:
            row = store.get_path(itr)[0]
            return enclib.get_python_name(store[row][1])
        return None


class AdvEncodingDialog(EncodingDialog):

    """Dialog for selecting character encodings."""

    def _init_tree_view(self):
        """Initialize the tree view."""

        self._tree_view.columns_autosize()
        selection = self._tree_view.get_selection()
        selection.set_mode(gtk.SELECTION_SINGLE)
        columns = (gobject.TYPE_STRING,) * 2 + (gobject.TYPE_BOOLEAN,)
        store = gtk.ListStore(*columns)
        self._tree_view.set_model(store)

        renderer = gtk.CellRendererText()
        column = gtk.TreeViewColumn(_("Description"), renderer, text=0)
        self._tree_view.append_column(column)

        renderer = gtk.CellRendererText()
        column = gtk.TreeViewColumn(_("Encoding"), renderer, text=1)
        self._tree_view.append_column(column)

        def on_toggled(renderer, row):
            store[row][2] = not store[row][2]
        renderer = gtk.CellRendererToggle()
        renderer.connect("toggled", on_toggled)
        column = gtk.TreeViewColumn(_("Show in Menu"), renderer, active=2)
        self._tree_view.append_column(column)

        for i, column in enumerate(self._tree_view.get_columns()):
            column.set_resizable(True)
            column.set_clickable(True)
            column.set_sort_column_id(i)

        store.set_sort_column_id(0, gtk.SORT_ASCENDING)
        visibles = conf.encoding.visibles
        for item in enclib.get_valid_encodings():
            store.append([item[2], item[1], item[0] in visibles])

    def get_visible_encodings(self):
        """Get encodings chosen to be visible."""

        visibles = []
        store = self._tree_view.get_model()
        for i in range(len(store)):
            if store[i][2]:
                visibles.append(enclib.get_python_name(store[i][1]))
        return visibles
