# -*- coding: utf-8 -*-

# Copyright (C) 2005 Osmo Salomaa
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""Dialogs for selecting character encodings."""

import aeidon
import gaupol

from aeidon.i18n   import _
from gi.repository import GObject
from gi.repository import Gtk

__all__ = ("EncodingDialog", "MenuEncodingDialog")


class EncodingDialog(Gtk.Dialog):

    """Dialog for selecting a character encoding."""

    def __init__(self, parent):
        """Initialize an :class:`EncodingDialog` instance."""
        GObject.GObject.__init__(self, use_header_bar=True)
        self._tree_view = Gtk.TreeView()
        self._init_dialog(parent)
        self._init_tree_view()
        gaupol.util.scale_to_content(self._tree_view,
                                     min_nchar=50,
                                     max_nchar=100,
                                     min_nlines=10,
                                     max_nlines=18)

    def get_encoding(self):
        """Return the selected encoding or ``None``."""
        selection = self._tree_view.get_selection()
        store, itr = selection.get_selected()
        if itr is None: return
        return store.get_value(itr, 0)

    def _init_dialog(self, parent):
        """Initialize the dialog."""
        self.add_button(_("_Cancel"), Gtk.ResponseType.CANCEL)
        self.add_button(_("_OK"), Gtk.ResponseType.OK)
        self.set_default_response(Gtk.ResponseType.OK)
        self.set_transient_for(parent)
        self.set_modal(True)
        self.set_title(_("Character Encodings"))

    def _init_tree_view(self):
        """Initialize the character encoding tree view."""
        scroller = Gtk.ScrolledWindow()
        scroller.set_policy(*((Gtk.PolicyType.AUTOMATIC,)*2))
        scroller.set_shadow_type(Gtk.ShadowType.NONE)
        scroller.add(self._tree_view)
        box = self.get_content_area()
        gaupol.util.pack_start_expand(box, scroller)
        box.show_all()
        selection = self._tree_view.get_selection()
        selection.set_mode(Gtk.SelectionMode.SINGLE)
        store = Gtk.ListStore(str, str, str)
        for item in aeidon.encodings.get_valid():
            store.append((item[0], item[2], item[1]))
        store.set_sort_column_id(1, Gtk.SortType.ASCENDING)
        self._tree_view.set_model(store)
        column = Gtk.TreeViewColumn(_("Description"),
                                    Gtk.CellRendererText(),
                                    text=1)

        column.set_clickable(True)
        column.set_sort_column_id(1)
        self._tree_view.append_column(column)
        column = Gtk.TreeViewColumn(_("Encoding"),
                                    Gtk.CellRendererText(),
                                    text=2)

        column.set_clickable(True)
        column.set_sort_column_id(2)
        self._tree_view.append_column(column)
        aeidon.util.connect(self, "_tree_view", "row-activated")

    def _on_tree_view_row_activated(self, *args):
        """Send response to select activated character encoding."""
        self.response(Gtk.ResponseType.OK)


class MenuEncodingDialog(EncodingDialog):

    """Dialog for selecting character encodings."""

    def get_visible_encodings(self):
        """Return encodings chosen to be visible."""
        store = self._tree_view.get_model()
        return [store[i][0] for i in range(len(store)) if store[i][3]]

    def _init_tree_view(self):
        """Initialize the character encoding tree view."""
        scroller = Gtk.ScrolledWindow()
        scroller.set_policy(*((Gtk.PolicyType.AUTOMATIC,)*2))
        scroller.set_shadow_type(Gtk.ShadowType.NONE)
        scroller.add(self._tree_view)
        box = self.get_content_area()
        gaupol.util.pack_start_expand(box, scroller)
        box.show_all()
        selection = self._tree_view.get_selection()
        selection.set_mode(Gtk.SelectionMode.SINGLE)
        store = Gtk.ListStore(str, str, str, bool)
        visible = gaupol.conf.encoding.visible
        for item in aeidon.encodings.get_valid():
            store.append((item[0], item[2], item[1], item[0] in visible))
        store.set_sort_column_id(1, Gtk.SortType.ASCENDING)
        self._tree_view.set_model(store)
        column = Gtk.TreeViewColumn(_("Description"),
                                    Gtk.CellRendererText(),
                                    text=1)

        column.set_clickable(True)
        column.set_sort_column_id(1)
        self._tree_view.append_column(column)
        column = Gtk.TreeViewColumn(_("Encoding"),
                                    Gtk.CellRendererText(),
                                    text=2)

        column.set_clickable(True)
        column.set_sort_column_id(2)
        self._tree_view.append_column(column)
        renderer = Gtk.CellRendererToggle()
        renderer.connect("toggled", self._on_tree_view_cell_toggled)
        column = Gtk.TreeViewColumn(_("Show in Menu"),
                                    renderer,
                                    active=3)

        column.set_sort_column_id(3)
        self._tree_view.append_column(column)
        aeidon.util.connect(self, "_tree_view", "row-activated")

    def _on_tree_view_cell_toggled(self, renderer, path):
        """Toggle the value of the "Show in Menu" column."""
        store = self._tree_view.get_model()
        store[path][3] = not store[path][3]
