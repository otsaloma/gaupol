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


"""Warning dialog for warning when trying to close multiple documents."""


try:
    from psyco.classes import *
except ImportError:
    pass

import gobject
import gtk

from gaupol.constants import Document
from gaupol.gtk.util  import gui


PAGE, NAME = 0, 1
SAVE       = 0


class MultiCloseWarningDialog(object):

    """
    Warning dialog for warning when trying to close multiple documents.

    Will be displayed when quitting, or when closing a tab with at least two
    documents open with unsaved changes.
    """

    def __init__(self, parent, pages):

        glade_xml = gui.get_glade_xml('multiclose-dialog.glade')

        # Widgets
        self._dialog    = glade_xml.get_widget('dialog')
        self._main_view = glade_xml.get_widget('main_tree_view')
        self._tran_view = glade_xml.get_widget('translation_tree_view')

        self._dialog.set_transient_for(parent)
        self._dialog.set_default_response(gtk.RESPONSE_YES)

        # Lists of tuples (page, basename)
        self._main_data = []
        self._tran_data = []

        # List pages with unsaved changes.
        for page in pages:
            if page.project.main_changed:
                self._main_data.append((page, page.get_main_basename()))
            if page.project.tran_active and page.project.tran_changed:
                self._tran_data.append((page, page.get_translation_basename()))

        self._init_main_view(glade_xml)
        self._init_translation_view(glade_xml)

    def _init_main_view(self, glade_xml):
        """Initialize the list of main documents."""

        view = self._main_view
        label = glade_xml.get_widget('main_label')
        label.set_mnemonic_widget(view)
        view, store = self._init_view(view, Document.MAIN)

        # Insert data.
        for page, basename in self._main_data:
            store.append([True, basename])

        self._init_view_size(view)

        if len(store) == 0:
            glade_xml.get_widget('main_label').hide()
            glade_xml.get_widget('main_scrolled_window').hide()

    def _init_translation_view(self, glade_xml):
        """Initialize the list of translation documents."""

        view = self._tran_view
        label = glade_xml.get_widget('translation_label')
        label.set_mnemonic_widget(view)
        view, store = self._init_view(view, Document.TRAN)

        # Insert data.
        for page, basename in self._tran_data:
            store.append([True, basename])

        self._init_view_size(view)

        if len(store) == 0:
            glade_xml.get_widget('translation_label').hide()
            glade_xml.get_widget('translation_scrolled_window').hide()

    def _init_view(self, tree_view, document_type):
        """
        Initialize a document list.

        Return view, store.
        """
        view.columns_autosize()
        view.set_headers_visible(False)

        store = gtk.ListStore(gobject.TYPE_BOOLEAN, gobject.TYPE_STRING)
        view.set_model(store)

        selection = view.get_selection()
        selection.set_mode(gtk.SELECTION_SINGLE)
        selection.unselect_all()

        cell_renderer_0 = gtk.CellRendererToggle()
        cell_renderer_1 = gtk.CellRendererText()

        cell_renderer_0.props.activatable = True
        method = self._on_view_cell_toggled
        cell_renderer_0.connect('toggled', method, store)

        tree_view_column_0 = gtk.TreeViewColumn('', cell_renderer_0, active=0)
        tree_view_column_1 = gtk.TreeViewColumn('', cell_renderer_1,   text=1)

        view.append_column(tree_view_column_0)
        view.append_column(tree_view_column_1)

        return view, store

    def _init_view_size(self, view):
        """Set a sensible size document list."""

        # 24 pixels are added to account for possible scroll bar.
        width, height = view.size_request()
        width  = min(150, width  + 24)
        height = min(126, height + 24)
        view.set_size_request(width, height)

    def destroy(self):
        """Destroy the dialog."""

        self._dialog.destroy()

    def get_main_pages_to_save(self):
        """Get pages, whose main files were chosen to be saved."""

        store = self._main_view.get_model()
        pages = []

        for i in range(len(store)):
            if store[i][SAVE]:
                pages.append(self._main_data[i][PAGE])

        return pages

    def get_translation_pages_to_save(self):
        """Get pages, whose translation files were chosen to be saved."""

        store = self._tran_view.get_model()
        pages = []

        for i in range(len(store)):
            if store[i][SAVE]:
                pages.append(self._tran_data[i][PAGE])

        return pages

    def _on_view_cell_toggled(self, cell_renderer, row, store):
        """Toggle the value on the check button column."""

        store[row][SAVE] = not store[row][SAVE]

        mains = self.get_main_pages_to_save()
        trans = self.get_translation_pages_to_save()

        sensitive = bool(mains or trans)
        self._dialog.set_response_sensitive(gtk.RESPONSE_YES, sensitive)

    def run(self):
        """Run the dialog."""

        self._main_view.grab_focus()
        self._dialog.show()
        return self._dialog.run()
