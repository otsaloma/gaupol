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

"""Dialog for warning when closing multiple documents."""

import aeidon
import gaupol

from aeidon.i18n   import _
from gi.repository import GObject
from gi.repository import Gtk

__all__ = ("MultiCloseDialog",)


class MultiCloseDialog(Gtk.MessageDialog):

    """Dialog for warning when closing multiple documents."""

    def __init__(self, parent, application, pages):
        """Initialize a :class:`MultiCloseDialog` instance."""
        GObject.GObject.__init__(self,
                                 message_type=Gtk.MessageType.ERROR,
                                 text=_("Save changes to documents before closing?"),
                                 secondary_text=_("If you don't save, changes will be permanently lost."))

        self.application = application
        self._main_tree_view = Gtk.TreeView()
        self._main_vbox = gaupol.util.new_vbox(6)
        self.pages = tuple(pages)
        self._tran_tree_view = Gtk.TreeView()
        self._tran_vbox = gaupol.util.new_vbox(6)
        self._init_dialog(parent)
        self._init_main_tree_view()
        self._init_tran_tree_view()

    def _init_dialog(self, parent):
        """Initialize the dialog."""
        self.add_button(_("Close _Without Saving"), Gtk.ResponseType.NO)
        self.add_button(_("_Cancel"), Gtk.ResponseType.CANCEL)
        self.add_button(_("_Save"), Gtk.ResponseType.YES)
        self.set_default_response(Gtk.ResponseType.YES)
        self.set_transient_for(parent)
        self.set_modal(True)
        aeidon.util.connect(self, self, "response")

    def _init_main_tree_view(self):
        """Initialize the main tree view."""
        store = self._init_tree_view(self._main_tree_view)
        for page in (x for x in self.pages if x.project.main_changed):
            store.append((page, True, page.get_main_basename()))
        scroller = Gtk.ScrolledWindow()
        scroller.set_policy(*((Gtk.PolicyType.AUTOMATIC,)*2))
        scroller.set_shadow_type(Gtk.ShadowType.ETCHED_IN)
        scroller.add(self._main_tree_view)
        label = Gtk.Label(label=_("Select the _main documents you want to save:"))
        label.props.xalign = 0
        label.set_use_underline(True)
        label.set_mnemonic_widget(self._main_tree_view)
        gaupol.util.pack_start(self._main_vbox, label)
        gaupol.util.pack_start_expand(self._main_vbox, scroller)
        gaupol.util.pack_start_expand(self.get_message_area(), self._main_vbox)
        self._main_vbox.set_visible(len(store) > 0)
        if len(store) > 0:
            self._main_vbox.show_all()
            gaupol.util.scale_to_content(self._main_tree_view,
                                         min_nchar=30,
                                         max_nchar=60,
                                         min_nlines=2,
                                         max_nlines=6)

    def _init_tran_tree_view(self):
        """Initialize the translation tree view."""
        store = self._init_tree_view(self._tran_tree_view)
        for page in (x for x in self.pages if x.project.tran_changed):
            store.append((page, True, page.get_translation_basename()))
        scroller = Gtk.ScrolledWindow()
        scroller.set_policy(*((Gtk.PolicyType.AUTOMATIC,)*2))
        scroller.set_shadow_type(Gtk.ShadowType.ETCHED_IN)
        scroller.add(self._tran_tree_view)
        label = Gtk.Label(label=_("Select the _translation documents you want to save:"))
        label.props.xalign = 0
        label.set_use_underline(True)
        label.set_mnemonic_widget(self._tran_tree_view)
        gaupol.util.pack_start(self._tran_vbox, label)
        gaupol.util.pack_start_expand(self._tran_vbox, scroller)
        gaupol.util.pack_start_expand(self.get_message_area(), self._tran_vbox)
        self._tran_vbox.set_visible(len(store) > 0)
        if len(store) > 0:
            self._tran_vbox.show_all()
            gaupol.util.scale_to_content(self._tran_tree_view,
                                         min_nchar=30,
                                         max_nchar=60,
                                         min_nlines=2,
                                         max_nlines=6)

    def _init_tree_view(self, tree_view):
        """Initialize `tree_view` and return its model."""
        tree_view.set_headers_visible(False)
        tree_view.set_enable_search(False)
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
            for page in self.pages:
                self._save_and_close_page(page)
        if response == Gtk.ResponseType.NO:
            for page in self.pages:
                self.application.close(page, confirm=False)

    def _on_tree_view_cell_toggled(self, renderer, path, store):
        """Toggle save document check button value."""
        store[path][1] = not store[path][1]
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
        self.application.close(page, confirm=False)
