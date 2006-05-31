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


"""Dialog for warning when trying to close multiple documents."""


try:
    from psyco.classes import *
except ImportError:
    pass

import gobject
import gtk

from gaupol.gtk.cons import *
from gaupol.gtk.util  import gtklib


PAGE, NAME = 0, 1
SAVE       = 0


class MultiCloseWarningDialog(object):

    """
    Dialog for warning when trying to close multiple documents.

    Will be displayed when quitting, or when closing a tab with at least two
    documents open with unsaved changes.
    """

    def __init__(self, parent, pages):

        glade_xml = gtklib.get_glade_xml('multiclose-dialog')

        self._dialog    = glade_xml.get_widget('dialog')
        self._main_view = glade_xml.get_widget('main_tree_view')
        self._tran_view = glade_xml.get_widget('translation_tree_view')

        # Lists of tuples (page, basename)
        self._main_data = []
        self._tran_data = []

        self._init_data(pages)
        self._init_main_view(glade_xml)
        self._init_tran_view(glade_xml)
        self._init_sizes()

        self._dialog.set_transient_for(parent)
        self._dialog.set_default_response(gtk.RESPONSE_YES)

    def _init_data(self, pages):
        """Initialize document lists"""

        # List pages with unsaved changes.
        for page in pages:
            if page.project.main_changed:
                self._main_data.append((page, page.get_main_basename()))
            if page.project.tran_active and page.project.tran_changed:
                self._tran_data.append((page, page.get_translation_basename()))

    def _init_main_view(self, glade_xml):
        """Initialize the list of main documents."""

        view, store = self._init_view(self._main_view)
        for page, basename in self._main_data:
            store.append([True, basename])

        if len(store) == 0:
            glade_xml.get_widget('main_label').hide()
            glade_xml.get_widget('main_scrolled_window').hide()

    def _init_sizes(self):
        """Initialize widget sizes."""

        main_width   = 0
        main_height  = 0
        tran_width   = 0
        tran_height  = 0
        height_extra = 136

        # Get desired sizes for scrolled windows.
        size = gtklib.get_tree_view_size
        if self._main_data:
            main_width, main_height = size(self._main_view)
            height_extra += 32
        if self._tran_data:
            tran_width, tran_height = size(self._tran_view)
            height_extra += 32

        # Get desired dialog size.
        width  = max(main_width, tran_width) + 88 + gtklib.EXTRA
        height = main_height + tran_height + height_extra + gtklib.EXTRA
        gtklib.resize_message_dialog(self._dialog, width, height)

    def _init_tran_view(self, glade_xml):
        """Initialize the list of translation documents."""

        view, store = self._init_view(self._tran_view)
        for page, basename in self._tran_data:
            store.append([True, basename])

        if len(store) == 0:
            glade_xml.get_widget('translation_label').hide()
            glade_xml.get_widget('translation_scrolled_window').hide()

    def _init_view(self, view):
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
        cell_renderer_0.props.activatable = True
        cell_renderer_0.connect('toggled', self._on_view_cell_toggled, store)
        cell_renderer_1 = gtk.CellRendererText()

        tree_view_column_0 = gtk.TreeViewColumn('', cell_renderer_0, active=0)
        tree_view_column_1 = gtk.TreeViewColumn('', cell_renderer_1,   text=1)
        view.append_column(tree_view_column_0)
        view.append_column(tree_view_column_1)

        return view, store

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


if __name__ == '__main__':

    from gaupol.gtk.page import Page
    from gaupol.test     import Test

    class TestMultiCloseWarningDialog(Test):

        def __init__(self):

            Test.__init__(self)

            page_1 = Page()
            page_1.project = self.get_project()
            page_1.project.remove_subtitles([1])

            page_2 = Page()
            page_2.project = self.get_project()
            page_2.project.remove_subtitles([1])

            self.pages  = [page_1, page_2]
            self.dialog = MultiCloseWarningDialog(gtk.Window(), self.pages)

        def test_get_main_pages_to_save(self):

            pages = self.dialog.get_main_pages_to_save()
            assert pages == self.pages

        def test_get_translation_pages_to_save(self):

            pages = self.dialog.get_translation_pages_to_save()
            assert pages == self.pages

        def test_signals(self):

            selection = self.dialog._main_view.get_selection()
            selection.unselect_all()
            selection.select_path(0)
            selection.select_path(1)

            selection = self.dialog._tran_view.get_selection()
            selection.unselect_all()
            selection.select_path(0)
            selection.select_path(1)

    TestMultiCloseWarningDialog().run()
