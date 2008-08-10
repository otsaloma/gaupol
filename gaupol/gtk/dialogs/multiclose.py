# Copyright (C) 2005-2008 Osmo Salomaa
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
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# Gaupol. If not, see <http://www.gnu.org/licenses/>.

"""Dialog for warning when closing multiple documents."""

import gaupol.gtk
import gtk

__all__ = ("MultiCloseDialog",)


class MultiCloseDialog(gaupol.gtk.GladeDialog):

    """Dialog for warning when closing multiple documents."""

    def __init__(self, parent, application, pages):

        gaupol.gtk.GladeDialog.__init__(self, "multiclose.glade")
        get_widget = self._glade_xml.get_widget
        self._main_tree_view = get_widget("main_tree_view")
        self._main_vbox = get_widget("main_vbox")
        self._tran_tree_view = get_widget("tran_tree_view")
        self._tran_vbox = get_widget("tran_vbox")
        self.application = application
        self.pages = pages

        self._init_main_tree_view()
        self._init_tran_tree_view()
        self._init_sizes()
        gaupol.util.connect(self, self, "response")
        self._dialog.set_transient_for(parent)
        self._dialog.set_default_response(gtk.RESPONSE_YES)

    def _init_main_tree_view(self):
        """Initialize the main tree view."""

        store = self._init_tree_view(self._main_tree_view)
        for page in (x for x in self.pages if x.project.main_changed):
            store.append((page, True, page.get_main_basename()))
        self._main_vbox.props.visible = (len(store) > 0)

    def _init_sizes(self):
        """Initialize widget sizes."""

        main_size = (0, 0)
        tran_size = (0, 0)
        height_extra = 136
        get_size = gaupol.gtk.util.get_tree_view_size
        if self._main_vbox.props.visible:
            main_size = get_size(self._main_tree_view)
            height_extra += 32
        if self._tran_vbox.props.visible:
            tran_size = get_size(self._tran_tree_view)
            height_extra += 32
        width = max(main_size[0], tran_size[0]) + 88 + gaupol.gtk.EXTRA
        height = main_size[1] + tran_size[1] + height_extra + gaupol.gtk.EXTRA
        gaupol.gtk.util.resize_message_dialog(self._dialog, width, height)

    def _init_tran_tree_view(self):
        """Initialize the translation tree view."""

        store = self._init_tree_view(self._tran_tree_view)
        for page in (x for x in self.pages if x.project.tran_changed):
            store.append((page, True, page.get_translation_basename()))
        self._tran_vbox.props.visible = (len(store) > 0)

    def _init_tree_view(self, tree_view):
        """Initialize tree view and return its list store model."""

        store = gtk.ListStore(object, bool, str)
        tree_view.set_model(store)
        selection = tree_view.get_selection()
        selection.set_mode(gtk.SELECTION_SINGLE)

        renderer = gtk.CellRendererToggle()
        renderer.props.activatable = True
        callback = self._on_tree_view_cell_toggled
        renderer.connect("toggled", callback, store)
        column = gtk.TreeViewColumn("", renderer, active=1)
        tree_view.append_column(column)

        renderer = gtk.CellRendererText()
        column = gtk.TreeViewColumn("", renderer, text=2)
        tree_view.append_column(column)
        return store

    def _on_response(self, dialog, response):
        """Save the selected documents and close pages."""

        if response == gtk.RESPONSE_YES:
            for page in self.pages:
                self._save_and_close_page(page)
        elif response == gtk.RESPONSE_NO:
            for page in self.pages:
                self.application.close_page(page, False)

    def _on_tree_view_cell_toggled(self, renderer, row, store):
        """Toggle the save check button value."""

        store[row][1] = not store[row][1]
        store = self._main_tree_view.get_model()
        mains = [x for x in store if x[1]]
        store = self._tran_tree_view.get_model()
        trans = [x for x in store if x[1]]
        sensitive = bool(mains or trans)
        self.set_response_sensitive(gtk.RESPONSE_YES, sensitive)

    @gaupol.deco.silent(gaupol.gtk.Default)
    def _save_and_close_page(self, page):
        """Save the selected documents and close page."""

        store = self._main_tree_view.get_model()
        pages = [x for x in store if x[0] is page]
        if pages and pages[0][1]:
            self.application.save_main_document(page)
        store = self._tran_tree_view.get_model()
        pages = [x for x in store if x[0] is page]
        if pages and pages[0][1]:
            self.application.save_translation_document(page)
        self.application.close_page(page, False)
