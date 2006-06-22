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


"""Dialog for warning when closing multiple documents."""


import gobject
import gtk

from gaupol.gtk.util import gtklib


class MultiCloseWarningDialog(object):

    """Dialog for warning when closing multiple documents."""

    def __init__(self, parent, pages):

        self._main_pages = []
        self._tran_pages = []

        glade_xml = gtklib.get_glade_xml('multiclose-dialog')
        self._dialog         = glade_xml.get_widget('dialog')
        self._main_tree_view = glade_xml.get_widget('main_tree_view')
        self._tran_tree_view = glade_xml.get_widget('tran_tree_view')

        self._init_data(pages)
        self._init_main_tree_view(glade_xml)
        self._init_tran_tree_view(glade_xml)
        self._init_sizes()
        self._dialog.set_transient_for(parent)
        self._dialog.set_default_response(gtk.RESPONSE_YES)

    def _init_data(self, pages):
        """Initialize page lists"""

        for page in pages:
            if page.project.main_changed:
                self._main_pages.append(page)
            if page.project.tran_active and page.project.tran_changed:
                self._tran_pages.append(page)

    def _init_main_tree_view(self, glade_xml):
        """Initialize main tree view."""

        store = self._init_tree_view(self._main_tree_view)
        for page in self._main_pages:
            store.append([True, page.get_main_basename()])
        if len(store) == 0:
            glade_xml.get_widget('main_vbox').hide()

    def _init_sizes(self):
        """Initialize widget sizes."""

        main_width   = 0
        main_height  = 0
        tran_width   = 0
        tran_height  = 0
        height_extra = 136

        get_size = gtklib.get_tree_view_size
        if self._main_pages:
            main_width, main_height = get_size(self._main_tree_view)
            height_extra += 32
        if self._tran_pages:
            tran_width, tran_height = get_size(self._tran_tree_view)
            height_extra += 32

        width = max(main_width, tran_width) + 88 + gtklib.EXTRA
        height = main_height + tran_height + 136 + gtklib.EXTRA
        gtklib.resize_message_dialog(self._dialog, width, height)

    def _init_tran_tree_view(self, glade_xml):
        """Initialize translation tree view."""

        store = self._init_tree_view(self._tran_tree_view)
        for page in self._tran_pages:
            store.append([True, page.get_translation_basename()])
        if len(store) == 0:
            glade_xml.get_widget('tran_vbox').hide()

    def _init_tree_view(self, tree_view):
        """
        Initialize tree view.

        Return store.
        """
        tree_view.columns_autosize()
        tree_view.set_headers_visible(False)
        store = gtk.ListStore(gobject.TYPE_BOOLEAN, gobject.TYPE_STRING)
        tree_view.set_model(store)

        selection = tree_view.get_selection()
        selection.set_mode(gtk.SELECTION_SINGLE)
        selection.unselect_all()

        cr_toggle = gtk.CellRendererToggle()
        cr_toggle.props.activatable = True
        cr_toggle.connect('toggled', self._on_tree_view_cell_toggled, store)
        column = gtk.TreeViewColumn('', cr_toggle, active=0)
        tree_view.append_column(column)
        column = gtk.TreeViewColumn('', gtk.CellRendererText(), text=1)
        tree_view.append_column(column)

        return store

    def _on_tree_view_cell_toggled(self, cell_renderer, row, store):
        """Toggle check value."""

        store[row][0] = not store[row][0]
        mains = self.get_main_pages()
        trans = self.get_translation_pages()
        sensitive = bool(mains or trans)
        self._dialog.set_response_sensitive(gtk.RESPONSE_YES, sensitive)

    def destroy(self):
        """Destroy dialog."""

        self._dialog.destroy()

    def get_main_pages(self):
        """Get pages, with main files to save."""

        pages = []
        store = self._main_tree_view.get_model()
        for i in range(len(store)):
            if store[i][0]:
                pages.append(self._main_pages[i])
        return pages

    def get_translation_pages(self):
        """Get pages, with translation files to save."""

        pages = []
        store = self._tran_tree_view.get_model()
        for i in range(len(store)):
            if store[i][0]:
                pages.append(self._tran_pages[i])
        return pages

    def run(self):
        """Run dialog."""

        self._dialog.show()
        return self._dialog.run()
