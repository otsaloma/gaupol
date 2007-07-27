# Copyright (C) 2005-2007 Osmo Salomaa
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
# A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# Gaupol.  If not, see <http://www.gnu.org/licenses/>.

"""Dialogs for selecting character encodings."""

import gaupol.gtk
import gobject
import gtk
_ = gaupol.i18n._

from .glade import GladeDialog


class EncodingDialog(GladeDialog):

    """Dialog for selecting a character encoding."""

    __metaclass__ = gaupol.Contractual

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

        width, height = gaupol.gtk.util.get_tree_view_size(self._tree_view)
        width = width + 52 + gaupol.gtk.EXTRA
        height = height + 84 + gaupol.gtk.EXTRA
        gaupol.gtk.util.resize_dialog(self._dialog, width, height, 0.5)

    def _init_signal_handlers(self):
        """Initialize signal handlers."""

        respond = lambda *args: self.response(gtk.RESPONSE_OK)
        self._tree_view.connect("row-activated", respond)

    def _init_tree_view(self):
        """Initialize the tree view."""

        selection = self._tree_view.get_selection()
        selection.set_mode(gtk.SELECTION_SINGLE)
        store = gtk.ListStore(*(gobject.TYPE_STRING,) * 3)
        for item in gaupol.encodings.get_valid_encodings():
            store.append([item[0], item[2], item[1]])
        store.set_sort_column_id(1, gtk.SORT_ASCENDING)
        self._tree_view.set_model(store)

        renderer = gtk.CellRendererText()
        column = gtk.TreeViewColumn(_("Description"), renderer, text=1)
        column.set_clickable(True)
        column.set_sort_column_id(1)
        self._tree_view.append_column(column)

        renderer = gtk.CellRendererText()
        column = gtk.TreeViewColumn(_("Encoding"), renderer, text=2)
        column.set_clickable(True)
        column.set_sort_column_id(2)
        self._tree_view.append_column(column)

    def get_encoding_ensure(self, value):
        if value is not None:
            assert gaupol.encodings.is_valid_code(value)

    @gaupol.gtk.util.asserted_return
    def get_encoding(self):
        """Get the selected encoding or None."""

        selection = self._tree_view.get_selection()
        store, itr = selection.get_selected()
        assert itr is not None
        return store.get_value(itr, 0)


class AdvEncodingDialog(EncodingDialog):

    """Dialog for selecting character encodings."""

    def _init_tree_view(self):
        """Initialize the tree view."""

        selection = self._tree_view.get_selection()
        selection.set_mode(gtk.SELECTION_SINGLE)
        columns = (gobject.TYPE_STRING,) * 3 + (gobject.TYPE_BOOLEAN,)
        store = gtk.ListStore(*columns)
        visibles = gaupol.gtk.conf.encoding.visibles
        for item in gaupol.encodings.get_valid_encodings():
            store.append([item[0], item[2], item[1], item[0] in visibles])
        store.set_sort_column_id(1, gtk.SORT_ASCENDING)
        self._tree_view.set_model(store)

        renderer = gtk.CellRendererText()
        column = gtk.TreeViewColumn(_("Description"), renderer, text=1)
        column.set_clickable(True)
        column.set_sort_column_id(1)
        self._tree_view.append_column(column)

        renderer = gtk.CellRendererText()
        column = gtk.TreeViewColumn(_("Encoding"), renderer, text=2)
        column.set_clickable(True)
        column.set_sort_column_id(2)
        self._tree_view.append_column(column)

        def on_toggled(renderer, row):
            store[row][3] = not store[row][3]
        renderer = gtk.CellRendererToggle()
        renderer.connect("toggled", on_toggled)
        column = gtk.TreeViewColumn(_("Show in Menu"), renderer, active=3)
        column.set_sort_column_id(3)
        self._tree_view.append_column(column)

    def get_visible_encodings_ensure(self, value):
        for name in value:
            assert gaupol.encodings.is_valid_code(name)

    def get_visible_encodings(self):
        """Get encodings chosen to be visible."""

        store = self._tree_view.get_model()
        return [store[i][0] for i in range(len(store)) if store[i][3]]
