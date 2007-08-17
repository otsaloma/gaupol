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

"""Page with script, language and coutry based pattern selection."""

import gaupol.gtk
import gobject
import gtk
import pango
_ = gaupol.i18n._

from .page import TextAssistantPage


class LocalePage(TextAssistantPage):

    """Page with script, language and coutry based pattern selection."""

    __metaclass__ = gaupol.gtk.ContractualGObject

    def _filter_patterns(self, patterns):
        """Return a subset of patterns to show."""

        return patterns

    def _get_conf_domain_ensure(self, value):
        assert hasattr(value, "script")
        assert hasattr(value, "language")
        assert hasattr(value, "country")

    def _get_conf_domain(self):
        """Get the configuration domain for locale options."""

        raise NotImplementedError

    @gaupol.gtk.util.asserted_return
    def _get_country(self):
        """Get the selected country."""

        index = self._country_combo.get_active()
        store = self._country_combo.get_model()
        assert self._country_combo.props.sensitive
        assert index < (len(store) - 1)
        return store[index][0]

    @gaupol.gtk.util.asserted_return
    def _get_language(self):
        """Get the selected language."""

        index = self._language_combo.get_active()
        store = self._language_combo.get_model()
        assert self._language_combo.props.sensitive
        assert index < (len(store) - 1)
        return store[index][0]

    @gaupol.gtk.util.asserted_return
    def _get_script(self):
        """Get the selected script."""

        index = self._script_combo.get_active()
        store = self._script_combo.get_model()
        assert self._script_combo.props.sensitive
        assert index < (len(store) - 1)
        return store[index][0]

    def _init_combo(self, combo_box, items, active):
        """Initialize combo box and its values."""

        store = gtk.ListStore(*(gobject.TYPE_STRING,) * 2)
        combo_box.set_model(store)
        for code, name in items:
            store.append([code, name])
        if len(store) > 0:
            store.append([gaupol.gtk.COMBO_SEPARATOR, ""])
        store.append(["", _("Other")])
        view = combo_box.get_child()
        view.set_displayed_row(0)
        renderer = view.get_cell_renderers()[0]
        combo_box.set_attributes(renderer, text=1)
        function = gaupol.gtk.util.separate_combo
        combo_box.set_row_separator_func(function)
        for i in range(len(store)):
            if (store[i][0] == active) and active:
                return combo_box.set_active(i)
        combo_box.set_active(len(store) - 1)

    def _init_country_combo(self):
        """Initialize the country combo box."""

        combo_box = self._country_combo
        script = self._get_script()
        language = self._get_language()
        codes = self._manager.get_countries(script, language)
        items = [(x, gaupol.countries.code_to_name(x)) for x in codes]
        items.sort(key=lambda x: x[1])
        active = self._get_conf_domain().country
        self._init_combo(combo_box, items, active)

    def _init_language_combo(self):
        """Initialize the language combo box."""

        combo_box = self._language_combo
        script = self._get_script()
        codes = self._manager.get_languages(script)
        items = [(x, gaupol.languages.code_to_name(x)) for x in codes]
        items.sort(key=lambda x: x[1])
        active = self._get_conf_domain().language
        self._init_combo(combo_box, items, active)

    def _init_script_combo(self):
        """Initialize the script combo box."""

        combo_box = self._script_combo
        codes = self._manager.get_scripts()
        items = [(x, gaupol.scripts.code_to_name(x)) for x in codes]
        items.sort(key=lambda x: x[1])
        active = self._get_conf_domain().script
        self._init_combo(combo_box, items, active)

    def _init_signal_handlers(self):
        """Initialize signal handlers."""

        gaupol.gtk.util.connect(self, "_country_combo", "changed")
        gaupol.gtk.util.connect(self, "_language_combo", "changed")
        gaupol.gtk.util.connect(self, "_script_combo", "changed")

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

    def _on_country_combo_changed(self, combo_box):
        """Populate the tree view with the correct patterns."""

        country = self._get_country()
        domain = self._get_conf_domain()
        domain.country = country or ""
        self._populate_tree_view()

    def _on_language_combo_changed(self, combo_box):
        """Populate the tree view with the correct patterns."""

        language = self._get_language()
        sensitive = (language is not None)
        self._country_combo.set_sensitive(sensitive)
        self._country_label.set_sensitive(sensitive)
        domain = self._get_conf_domain()
        domain.language = language or ""
        self._populate_tree_view()

    def _on_script_combo_changed(self, combo_box):
        """Populate the tree view with the correct patterns."""

        script = self._get_script()
        sensitive = (script is not None)
        self._language_combo.set_sensitive(sensitive)
        self._language_label.set_sensitive(sensitive)
        language = self._get_language()
        sensitive = (sensitive and (language is not None))
        self._country_combo.set_sensitive(sensitive)
        self._country_label.set_sensitive(sensitive)
        domain = self._get_conf_domain()
        domain.script = script or ""
        self._populate_tree_view()

    def _on_tree_view_cell_toggled(self, renderer, row, store):
        """Toggle the check button value."""

        store[row][1] = not store[row][1]
        store[row][0].enabled = store[row][1]

    def _populate_tree_view(self):
        """Populate the tree view with the correct patterns."""

        self._tree_view.get_model().clear()
        script = self._get_script()
        language = self._get_language()
        country = self._get_country()
        codes = (script, language, country)
        patterns = self._manager.get_patterns(*codes)
        patterns = self._filter_patterns(patterns)
        store = self._tree_view.get_model()
        for pattern in patterns:
            name = pattern.get_name()
            name = gobject.markup_escape_text(name)
            description = pattern.get_description()
            description = gobject.markup_escape_text(description)
            markup = "<b>%s</b>\n%s" % (name, description)
            store.append([pattern, pattern.enabled, markup])
        self._tree_view.get_selection().unselect_all()
