# Copyright (C) 2005-2008,2010 Osmo Salomaa
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

import aeidon
import gaupol
from gi.repository import Gtk

__all__ = ("MultiCloseDialog",)


class MultiCloseDialog(gaupol.BuilderDialog):

    """Dialog for warning when closing multiple documents."""

    _widgets = ("main_tree_view", "main_vbox", "tran_tree_view", "tran_vbox")

    def __init__(self, parent, application, pages):
        """Initialize a :class:`MultiCloseDialog` object."""
        gaupol.BuilderDialog.__init__(self, "multiclose-dialog.ui")
        self.application = application
        self.pages = tuple(pages)
        self._init_main_tree_view()
        self._init_tran_tree_view()
        self._init_sizes()
        self._dialog.set_transient_for(parent)
        self._dialog.set_default_response(Gtk.ResponseType.YES)

    def _init_main_tree_view(self):
        """Initialize the main tree view."""
        store = self._init_tree_view(self._main_tree_view)
        for page in [x for x in self.pages if x.project.main_changed]:
            store.append((page, True, page.get_main_basename()))
        self._main_vbox.props.visible = (len(store) > 0)

    def _init_sizes(self):
        """Initialize widget sizes."""
        if self._main_vbox.props.visible:
            gaupol.util.scale_to_content(self._main_tree_view,
                                         min_nlines=2,
                                         max_nchar=40,
                                         max_nlines=6)

        if self._tran_vbox.props.visible:
            gaupol.util.scale_to_content(self._tran_tree_view,
                                         min_nlines=2,
                                         max_nchar=40,
                                         max_nlines=6)

    def _init_tran_tree_view(self):
        """Initialize the translation tree view."""
        store = self._init_tree_view(self._tran_tree_view)
        for page in [x for x in self.pages if x.project.tran_changed]:
            store.append((page, True, page.get_translation_basename()))
        self._tran_vbox.props.visible = (len(store) > 0)

    def _init_tree_view(self, tree_view):
        """Initialize `tree_view` and return its model."""
        store = Gtk.ListStore(object, bool, str)
        tree_view.set_model(store)
        selection = tree_view.get_selection()
        selection.set_mode(Gtk.SelectionMode.SINGLE)
        renderer = Gtk.CellRendererToggle()
        renderer.props.activatable = True
        renderer.connect("toggled", self._on_tree_view_cell_toggled, store)
        column = Gtk.TreeViewColumn("", renderer, active=1)
        tree_view.append_column(column)
        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn("", renderer, text=2)
        tree_view.append_column(column)
        return store

    def _on_response(self, dialog, response):
        """Save the selected documents and close pages."""
        if response == Gtk.ResponseType.YES:
            list(map(self._save_and_close_page, self.pages))
        if response == Gtk.ResponseType.NO:
            list(map(lambda x: self.application.close(x, False), self.pages))

    def _on_tree_view_cell_toggled(self, renderer, row, store):
        """Toggle save document check button value."""
        store[row][1] = not store[row][1]
        store = self._main_tree_view.get_model()
        mains = [x for x in store if x[1]]
        store = self._tran_tree_view.get_model()
        trans = [x for x in store if x[1]]
        sensitive = bool(mains or trans)
        self.set_response_sensitive(Gtk.ResponseType.YES, sensitive)

    @aeidon.deco.silent(gaupol.Default)
    def _save_and_close_page(self, page):
        """Save the selected documents and close `page`."""
        store = self._main_tree_view.get_model()
        pages = [x for x in store if x[0] is page]
        if pages and pages[0][1]:
            self.application.save_main(page)
        store = self._tran_tree_view.get_model()
        pages = [x for x in store if x[0] is page]
        if pages and pages[0][1]:
            self.application.save_translation(page)
        self.application.close(page, False)
