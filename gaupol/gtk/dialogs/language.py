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

"""Dialog for configuring spell-check."""

import gaupol.gtk
import gtk
_ = gaupol.i18n._

__all__ = ("LanguageDialog",)


class LanguageDialog(gaupol.gtk.GladeDialog):

    """Dialog for configuring spell-check."""

    __metaclass__ = gaupol.Contractual

    def __init___require(self, parent, show_target=True):
        assert gaupol.util.enchant_available()

    def __init__(self, parent, show_target=True):
        """Initialize a LanguageDialog object."""

        gaupol.gtk.GladeDialog.__init__(self, "language.glade")
        get_widget = self._glade_xml.get_widget
        self._all_radio = get_widget("all_radio")
        self._current_radio = get_widget("current_radio")
        self._main_radio = get_widget("main_radio")
        self._tran_radio = get_widget("tran_radio")
        self._tree_view = get_widget("tree_view")
        self.conf = gaupol.gtk.conf.spell_check

        self._init_visibilities(show_target)
        self._init_tree_view()
        self._init_values()
        self._init_signal_handlers()
        self._init_sizes()
        self._dialog.set_transient_for(parent)
        self._dialog.set_default_response(gtk.RESPONSE_CLOSE)

    def _init_signal_handlers(self):
        """Initialize signal handlers."""

        on_field_toggled = lambda x, self: self._save_field()
        self._main_radio.connect("toggled", on_field_toggled, self)
        self._tran_radio.connect("toggled", on_field_toggled, self)
        on_target_toggled = lambda x, self: self._save_target()
        self._all_radio.connect("toggled", on_target_toggled, self)
        self._current_radio.connect("toggled", on_target_toggled, self)
        selection = self._tree_view.get_selection()
        callback = self._on_tree_view_selection_changed
        selection.connect("changed", callback)

    def _init_sizes(self):
        """Initialize widget sizes."""

        width = gaupol.gtk.util.get_tree_view_size(self._tree_view)[0]
        width = width + gaupol.gtk.EXTRA
        width = min(width, int(0.5 * gtk.gdk.screen_width()))
        height = gtk.Label("X\n" * 11).size_request()[1]
        height = height + gaupol.gtk.EXTRA
        height = min(height, int(0.5 * gtk.gdk.screen_height()))
        self._tree_view.set_size_request(width, height)

    def _init_tree_view(self):
        """Initialize the tree view."""

        selection = self._tree_view.get_selection()
        selection.set_mode(gtk.SELECTION_SINGLE)
        store = gtk.ListStore(str, str)
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
            if store[i][0] == self.conf.language:
                selection.select_path(i)
        fields = gaupol.gtk.fields
        self._main_radio.set_active(self.conf.field == fields.MAIN_TEXT)
        self._tran_radio.set_active(self.conf.field == fields.TRAN_TEXT)
        targets = gaupol.gtk.targets
        self._all_radio.set_active(self.conf.target == targets.ALL)
        self._current_radio.set_active(self.conf.target == targets.CURRENT)

    def _init_visibilities(self, show_target):
        """Initialize visibilities of target widgets."""

        if show_target: return
        get_widget = self._glade_xml.get_widget
        get_widget("language_title_label").hide()
        get_widget("target_vbox").hide()
        get_widget("language_alignment").set_padding(0, 0, 0, 0)
        self._dialog.set_title(_("Set Language"))

    def _on_tree_view_selection_changed(self, selection):
        """Save the active language."""

        store, itr = selection.get_selected()
        if itr is None: return
        value = store.get_value(itr, 0)
        self.conf.language = value

    def _populate_store(self, store):
        """Add all available languages to the list store."""

        import enchant
        try: locales = list(enchant.list_languages())
        except enchant.Error: locales = []
        for locale in set(locales):
            try: enchant.Dict(locale).check("1")
            except enchant.Error: continue
            try: name = gaupol.locales.code_to_name(locale)
            except LookupError: name = locale
            store.append((locale, name))

    def _save_field(self):
        """Save the active field."""

        if self._main_radio.get_active():
            field = gaupol.gtk.fields.MAIN_TEXT
        elif self._tran_radio.get_active():
            field = gaupol.gtk.fields.TRAN_TEXT
        self.conf.field = field

    def _save_target(self):
        """Save the active target."""

        if self._current_radio.get_active():
            target = gaupol.gtk.targets.CURRENT
        elif self._all_radio.get_active():
            target = gaupol.gtk.targets.ALL
        self.conf.target = target
