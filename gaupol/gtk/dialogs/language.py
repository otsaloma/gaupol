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


"""Dialog for configuring spell-check."""


import gobject
import gtk

try:
    import enchant
except Exception:
    pass

from gaupol import langlib
from gaupol.gtk import conf, const, util
from gaupol.gtk.index import *
from .glade import GladeDialog


class LanguageDialog(GladeDialog):

    """Dialog for configuring spell-check.

    Instance variables:

        _all_radio:     gtk.RadioButton, target all documents
        _current_radio: gtk.RadioButton, target current document
        _langs:         List of languages, er... locales
        _main_radio:    gtk.RadioButton, target main text column
        _tran_radio:    gtk.RadioButton, target translation text column
        _tree_view:     gtk.TreeView, languages
    """

    def __init__(self, parent):

        GladeDialog.__init__(self, "language-dialog")

        self._langs = []

        self._all_radio     = self._glade_xml.get_widget("all_radio")
        self._current_radio = self._glade_xml.get_widget("current_radio")
        self._main_radio    = self._glade_xml.get_widget("main_radio")
        self._tran_radio    = self._glade_xml.get_widget("tran_radio")
        self._tree_view     = self._glade_xml.get_widget("tree_view")

        self._init_langs()
        self._init_tree_view()
        self._init_data()
        self._init_signal_handlers()
        self._init_sizes()
        self._dialog.set_transient_for(parent)
        self._dialog.set_default_response(gtk.RESPONSE_CLOSE)

    def _init_data(self):
        """Initialize default values for widgets."""

        if conf.spell_check.lang in self._langs:
            row = self._langs.index(conf.spell_check.lang)
            self._tree_view.get_selection().select_path(row)

        col = conf.spell_check.col
        self._main_radio.set_active(col == MTXT)
        self._tran_radio.set_active(col == TTXT)

        target = conf.spell_check.target
        self._all_radio.set_active(target == const.TARGET.ALL)
        self._current_radio.set_active(target == const.TARGET.CURRENT)

    def _init_langs(self):
        """Initialize the list of available languages."""

        for locale in langlib.LOCALES:
            try:
                enchant.Dict(locale)
                self._langs.append(locale)
            except enchant.Error:
                pass
        self._langs.sort()

    def _init_signal_handlers(self):
        """Initialize signal handlers."""

        def on_target_toggled(*args):
            self._save_target()
        self._all_radio.connect("toggled", on_target_toggled)
        self._current_radio.connect("toggled", on_target_toggled)

        def on_column_toggled(*args):
            self._save_column()
        self._main_radio.connect("toggled", on_column_toggled)
        self._tran_radio.connect("toggled", on_column_toggled)

        selection = self._tree_view.get_selection()
        selection.connect("changed", self._on_tree_view_selection_changed)

    def _init_sizes(self):
        """Initialize widget sizes."""

        width, height = util.get_tree_view_size(self._tree_view)
        width = width + 42 + util.EXTRA
        height = height + 259 + util.EXTRA
        util.resize_dialog(self, width, height, 0.5, 0.5)

    def _init_tree_view(self):
        """Initialize the tree view."""

        self._tree_view.columns_autosize()
        selection = self._tree_view.get_selection()
        selection.set_mode(gtk.SELECTION_SINGLE)
        store = gtk.ListStore(gobject.TYPE_STRING)
        self._tree_view.set_model(store)
        column = gtk.TreeViewColumn("", gtk.CellRendererText(), text=0)
        self._tree_view.append_column(column)
        for lang in self._langs:
            store.append([langlib.get_long_name(lang)])

    @util.silent(AssertionError)
    def _on_tree_view_selection_changed(self, selection):
        """Save the language."""

        store, itr = selection.get_selected()
        assert itr is not None
        row = store.get_path(itr)[0]
        conf.spell_check.lang = self._langs[row]

    def _save_column(self):
        """Save the column."""

        main = self._main_radio.get_active()
        col = (MTXT if main else TTXT)
        conf.spell_check.col = col

    def _save_target(self):
        """Save the target."""

        each = self._all_radio.get_active()
        target = (const.TARGET.ALL if each else const.TARGET.CURRENT)
        conf.spell_check.target = target
