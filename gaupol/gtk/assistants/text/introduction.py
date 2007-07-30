# Copyright (C) 2007 Osmo Salomaa
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

"""Page for listing all text correction tasks."""

import gaupol.gtk
import gobject
import gtk
import pango
_ = gaupol.i18n._

from .page import TextAssistantPage


class IntroductionPage(TextAssistantPage):

    """Page for listing all text correction tasks."""

    def __init__(self):

        TextAssistantPage.__init__(self)
        self.page_title = _("Select Tasks and Target")
        self.page_type = gtk.ASSISTANT_PAGE_INTRO

        name = "text-assistant-introduction-page"
        self._glade_xml = gaupol.gtk.util.get_glade_xml(name)
        get_widget = self._glade_xml.get_widget
        self._all_radio = get_widget("all_radio")
        self._current_radio = get_widget("current_radio")
        self._main_radio = get_widget("main_radio")
        self._selected_radio = get_widget("selected_radio")
        self._tran_radio = get_widget("tran_radio")
        self._tree_view = get_widget("tree_view")
        get_widget("vbox").reparent(self)

        self._init_properties()
        self._init_tree_view()
        self._init_signal_handlers()

    def _get_column(self):
        """Get the selected column."""

        if self._main_radio.get_active():
            return gaupol.gtk.COLUMN.MAIN_TEXT
        if self._tran_radio.get_active():
            return gaupol.gtk.COLUMN.TRAN_TEXT
        raise ValueError

    def _get_target(self):
        """Get the selected target."""

        if self._selected_radio.get_active():
            return gaupol.gtk.TARGET.SELECTED
        if self._current_radio.get_active():
            return gaupol.gtk.TARGET.CURRENT
        if self._all_radio.get_active():
            return gaupol.gtk.TARGET.ALL
        raise ValueError

    def _init_signal_handlers(self):
        """Initialize signal handlers."""

        def save_column(*args):
            gaupol.gtk.conf.text_assistant.column = self._get_column()
        self._main_radio.connect("toggled", save_column)
        self._tran_radio.connect("toggled", save_column)
        def save_target(*args):
            gaupol.gtk.conf.text_assistant.target = self._get_target()
        self._selected_radio.connect("toggled", save_target)
        self._current_radio.connect("toggled", save_target)
        self._all_radio.connect("toggled", save_target)

    def _init_tree_view(self):
        """Initialize the tree view."""

        cols = (object, gobject.TYPE_BOOLEAN, gobject.TYPE_STRING)
        store = gtk.ListStore(*cols)
        self._tree_view.set_model(store)
        selection = self._tree_view.get_selection()
        selection.set_mode(gtk.SELECTION_SINGLE)

        renderer = gtk.CellRendererToggle()
        renderer.props.activatable = True
        renderer.props.xpad = 6
        callback = self._on_tree_view_cell_toggled
        renderer.connect("toggled", callback, store)
        column = gtk.TreeViewColumn("", renderer, active=1)
        self._tree_view.append_column(column)

        renderer = gtk.CellRendererText()
        renderer.props.ellipsize = pango.ELLIPSIZE_END
        column = gtk.TreeViewColumn("", renderer, markup=2)
        self._tree_view.append_column(column)

    def _on_tree_view_cell_toggled(self, renderer, row, store):
        """Toggle the check button value."""

        store[row][1] = not store[row][1]
        store[row][0].props.visible = store[row][1]
        pages = [x.handle for x in self.get_selected_pages()]
        gaupol.gtk.conf.text_assistant.pages = pages

    def get_selected_pages(self):
        """Get the selected content pages."""

        store = self._tree_view.get_model()
        return [x[0] for x in store if x[1]]

    def populate_tree_view(self, pages):
        """Populate the tree view with a list of tasks defined by pages."""

        store = self._tree_view.get_model()
        store.clear()
        domain = gaupol.gtk.conf.text_assistant
        for page in pages:
            markup = "<b>%s</b>\n%s" % (page.title, page.description)
            page.props.visible = page.handle in domain.pages
            store.append([page, page.handle in domain.pages, markup])
        self._tree_view.get_selection().unselect_all()
