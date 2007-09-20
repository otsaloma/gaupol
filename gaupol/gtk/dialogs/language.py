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

"""Dialog for configuring spell-check."""

import gaupol.gtk
import gobject
import gtk

from .glade import GladeDialog


class LanguageDialog(GladeDialog):

    """Dialog for configuring spell-check."""

    __metaclass__ = gaupol.Contractual

    def __init___require(self, parent):
        assert gaupol.gtk.util.enchant_available()

    def __init__(self, parent):

        GladeDialog.__init__(self, "language-dialog")
        get_widget = self._glade_xml.get_widget
        self._all_radio = get_widget("all_radio")
        self._current_radio = get_widget("current_radio")
        self._main_radio = get_widget("main_radio")
        self._tran_radio = get_widget("tran_radio")
        self._tree_view = get_widget("tree_view")

        self._init_tree_view()
        self._init_values()
        self._init_signal_handlers()
        self._init_sizes()
        self._dialog.set_transient_for(parent)
        self._dialog.set_default_response(gtk.RESPONSE_CLOSE)

    def _init_signal_handlers(self):
        """Initialize signal handlers."""

        on_column_toggled = lambda x, self: self._save_column()
        self._main_radio.connect("toggled", on_column_toggled, self)
        self._tran_radio.connect("toggled", on_column_toggled, self)
        on_target_toggled = lambda x, self: self._save_target()
        self._all_radio.connect("toggled", on_target_toggled, self)
        self._current_radio.connect("toggled", on_target_toggled, self)
        selection = self._tree_view.get_selection()
        callback = self._on_tree_view_selection_changed
        selection.connect("changed", callback)

    def _init_sizes(self):
        """Initialize widget sizes."""

        width, height = gaupol.gtk.util.get_tree_view_size(self._tree_view)
        width = width + 42 + gaupol.gtk.EXTRA
        height = height + 259 + gaupol.gtk.EXTRA
        gaupol.gtk.util.resize_dialog(self, width, height, 0.5)

    def _init_tree_view(self):
        """Initialize the tree view."""

        selection = self._tree_view.get_selection()
        selection.set_mode(gtk.SELECTION_SINGLE)
        store = gtk.ListStore(*(gobject.TYPE_STRING,) * 2)
        self._populate_store(store)
        store.set_sort_column_id(1, gtk.SORT_ASCENDING)
        self._tree_view.set_model(store)

        renderer = gtk.CellRendererText()
        column = gtk.TreeViewColumn("", renderer, text=1)
        column.set_sort_column_id(1)
        self._tree_view.append_column(column)

    def _init_values(self):
        """Initialize default values for widgets."""

        store = self._tree_view.get_model()
        selection = self._tree_view.get_selection()
        for i in range(len(store)):
            if store[i][0] == gaupol.gtk.conf.spell_check.language:
                selection.select_path(i)
        col = gaupol.gtk.conf.spell_check.column
        self._main_radio.set_active(col == gaupol.gtk.COLUMN.MAIN_TEXT)
        self._tran_radio.set_active(col == gaupol.gtk.COLUMN.TRAN_TEXT)
        target = gaupol.gtk.conf.spell_check.target
        self._all_radio.set_active(target == gaupol.gtk.TARGET.ALL)
        self._current_radio.set_active(target == gaupol.gtk.TARGET.CURRENT)

    @gaupol.gtk.util.asserted_return
    def _on_tree_view_selection_changed(self, selection):
        """Save the active language."""

        store, itr = selection.get_selected()
        assert itr is not None
        value = store.get_value(itr, 0)
        gaupol.gtk.conf.spell_check.language = value

    def _populate_store(self, store):
        """Add all available languages to the list store."""

        import enchant
        @gaupol.gtk.util.silent(enchant.Error)
        def append(locale):
            enchant.Dict(locale)
            name = gaupol.locales.code_to_name(locale)
            store.append([locale, name])
        for locale in gaupol.locales.locales:
            append(locale)

    def _save_column(self):
        """Save the active column."""

        if self._main_radio.get_active():
            col = gaupol.gtk.COLUMN.MAIN_TEXT
        elif self._tran_radio.get_active():
            col = gaupol.gtk.COLUMN.TRAN_TEXT
        gaupol.gtk.conf.spell_check.column = col

    def _save_target(self):
        """Save the active target."""

        if self._current_radio.get_active():
            target = gaupol.gtk.TARGET.CURRENT
        elif self._all_radio.get_active():
            target = gaupol.gtk.TARGET.ALL
        gaupol.gtk.conf.spell_check.target = target
