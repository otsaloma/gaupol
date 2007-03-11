# Copyright (C) 2005-2007 Osmo Salomaa
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

from gaupol.gtk import util
from gaupol.gtk.errors import Default
from .glade import GladeDialog


class MultiCloseDialog(GladeDialog):

    """Dialog for warning when closing multiple documents.

    Instance variables:

        _main_pages:     Pages with main documents to save
        _main_tree_view: gtk.TreeView
        _tran_pages:     Pages with translation documents to save
        _tran_tree_view: gtk.TreeView
        application:     Associated Application
    """

    def __init__(self, parent, application, pages):

        GladeDialog.__init__(self, "multiclose-dialog")
        self._main_tree_view = self._glade_xml.get_widget("main_tree_view")
        self._tran_tree_view = self._glade_xml.get_widget("tran_tree_view")

        self._main_pages = []
        self._tran_pages = []
        self.application = application

        self._init_data(pages)
        self._init_main_tree_view()
        self._init_tran_tree_view()
        self._init_signal_handlers()
        self._init_sizes()
        self._dialog.set_transient_for(parent)
        self._dialog.set_default_response(gtk.RESPONSE_YES)

    def _close_pages(self):
        """Close all handled pages."""

        pages = set(self._main_pages)
        pages.update(set(self._tran_pages))
        for page in pages:
            self.application.close(page, False)

    def _init_data(self, pages):
        """Initialize the page lists."""

        for page in pages:
            if page.project.main_changed:
                self._main_pages.append(page)
            if page.project.tran_active and page.project.tran_changed:
                self._tran_pages.append(page)

    def _init_main_tree_view(self):
        """Initialize the main tree view."""

        store = self._init_tree_view(self._main_tree_view)
        for page in self._main_pages:
            store.append([True, page.get_main_basename()])
        if len(store) == 0:
            self._glade_xml.get_widget("main_vbox").hide()

    def _init_signal_handlers(self):
        """Initialize signal handlers."""

        util.connect(self, self, "response")

    def _init_sizes(self):
        """Initialize widget sizes."""

        main_width   = 0
        main_height  = 0
        tran_width   = 0
        tran_height  = 0
        height_extra = 136
        get_size = util.get_tree_view_size
        if self._main_pages:
            main_width, main_height = get_size(self._main_tree_view)
            height_extra += 32
        if self._tran_pages:
            tran_width, tran_height = get_size(self._tran_tree_view)
            height_extra += 32

        width = max(main_width, tran_width) + 88 + util.EXTRA
        height = main_height + tran_height + height_extra + util.EXTRA
        util.resize_message_dialog(self._dialog, width, height)

    def _init_tran_tree_view(self):
        """Initialize the translation tree view."""

        store = self._init_tree_view(self._tran_tree_view)
        for page in self._tran_pages:
            store.append([True, page.get_translation_basename()])
        if len(store) == 0:
            self._glade_xml.get_widget("tran_vbox").hide()

    def _init_tree_view(self, tree_view):
        """Initialize tree view and return its list store."""

        tree_view.set_headers_visible(False)
        store = gtk.ListStore(gobject.TYPE_BOOLEAN, gobject.TYPE_STRING)
        tree_view.set_model(store)
        selection = tree_view.get_selection()
        selection.set_mode(gtk.SELECTION_SINGLE)
        selection.unselect_all()

        renderer = gtk.CellRendererToggle()
        renderer.props.activatable = True
        renderer.connect("toggled", self._on_tree_view_cell_toggled, store)
        column = gtk.TreeViewColumn("", renderer, active=0)
        tree_view.append_column(column)

        renderer = gtk.CellRendererText()
        column = gtk.TreeViewColumn("", renderer, text=1)
        tree_view.append_column(column)
        return store

    @util.ignore_exceptions(AssertionError)
    def _on_response(self, dialog, response):
        """Save the selected documents and close pages."""

        assert response == gtk.RESPONSE_YES
        try:
            self._save_documents()
        except Default:
            self.stop_emission("response")
            return self.response(gtk.RESPONSE_CANCEL)
        self._close_pages()

    def _on_tree_view_cell_toggled(self, renderer, row, store):
        """Toggle the save check button value."""

        store[row][0] = not store[row][0]
        store = self._main_tree_view.get_model()
        mains = list(x for x in range(len(store)) if store[x][0])
        store = self._tran_tree_view.get_model()
        trans = list(x for x in range(len(store)) if store[x][0])
        sensitive = bool(mains or trans)
        self._dialog.set_response_sensitive(gtk.RESPONSE_YES, sensitive)

    def _save_documents(self):
        """Save the selected documents.

        Raise Default if something goes wrong.
        """
        store = self._main_tree_view.get_model()
        for i in (x for x in range(len(store)) if store[x][0]):
            self.application.save_main(self._main_pages[i])

        store = self._tran_tree_view.get_model()
        for i in (x for x in range(len(store)) if store[x][0]):
            self.application.save_translation(self._tran_pages[i])
