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

"""Dialog for configuring spell-check."""

import aeidon
import gaupol

from aeidon.i18n   import _
from gi.repository import Gtk

__all__ = ("LanguageDialog",)


class LanguageDialog(gaupol.BuilderDialog):

    """Dialog for configuring spell-check."""

    _widgets = [
        "all_radio",
        "current_radio",
        "language_scroller",
        "language_title_label",
        "main_radio",
        "target_vbox",
        "tran_radio",
        "tree_view",
    ]

    def __init__(self, parent, show_target=True):
        """Initialize a :class:`LanguageDialog` instance."""
        gaupol.BuilderDialog.__init__(self, "language-dialog.ui")
        self._init_dialog(parent)
        self._init_visibilities(show_target)
        self._init_tree_view()
        self._init_values()
        gaupol.util.scale_to_content(self._tree_view,
                                     min_nchar=30,
                                     max_nchar=60,
                                     min_nlines=8,
                                     max_nlines=20)

    def _init_dialog(self, parent):
        """Initialize the dialog."""
        self.set_default_response(Gtk.ResponseType.CLOSE)
        self.set_transient_for(parent)
        self.set_modal(True)

    def _init_tree_view(self):
        """Initialize the tree view."""
        selection = self._tree_view.get_selection()
        selection.set_mode(Gtk.SelectionMode.SINGLE)
        selection.connect("changed", self._on_tree_view_selection_changed)
        store = Gtk.ListStore(str, str)
        self._populate_store(store)
        store.set_sort_column_id(1, Gtk.SortType.ASCENDING)
        self._tree_view.set_model(store)
        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn("", renderer, text=1)
        column.set_sort_column_id(1)
        self._tree_view.append_column(column)

    def _init_values(self):
        """Initialize default values for widgets."""
        language = gaupol.conf.spell_check.language
        field = gaupol.conf.spell_check.field
        target = gaupol.conf.spell_check.target
        store = self._tree_view.get_model()
        selection = self._tree_view.get_selection()
        for i in range(len(store)):
            if store[i][0] == language:
                selection.select_path(i)
        self._main_radio.set_active(field == gaupol.fields.MAIN_TEXT)
        self._tran_radio.set_active(field == gaupol.fields.TRAN_TEXT)
        self._all_radio.set_active(target == gaupol.targets.ALL)
        self._current_radio.set_active(target == gaupol.targets.CURRENT)

    def _init_visibilities(self, show_target):
        """Initialize visibilities of target widgets."""
        if not show_target:
            self._language_title_label.hide()
            self._target_vbox.hide()
            self._dialog.set_title(_("Set Language"))

    def _on_current_radio_toggled(self, radio_button):
        """Save the selected target."""
        gaupol.conf.spell_check.target = (
            gaupol.targets.CURRENT
            if radio_button.get_active()
            else gaupol.targets.ALL)

    def _on_main_radio_toggled(self, radio_button):
        """Save the selected field."""
        gaupol.conf.spell_check.field = (
            gaupol.fields.MAIN_TEXT
            if radio_button.get_active()
            else gaupol.fields.TRAN_TEXT)

    def _on_tree_view_selection_changed(self, selection):
        """Save the selected language."""
        store, itr = selection.get_selected()
        if itr is None: return
        value = store.get_value(itr, 0)
        gaupol.conf.spell_check.language = value

    def _populate_store(self, store):
        """Add all available languages to `store`."""
        locales = []
        with aeidon.util.silent(Exception):
            locales = aeidon.SpellChecker.list_languages()
        for locale in locales:
            with aeidon.util.silent(Exception):
                name = aeidon.locales.code_to_name(locale)
                store.append((locale, name))
