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


"""Dialog for configuring spell-check."""


try:
    from psyco.classes import *
except ImportError:
    pass

import enchant
import gobject
import gtk

from gaupol.base.util import langlib
from gaupol.gtk.util  import config, gui


class LanguageDialog(object):

    """Dialog for configuring spell-check."""

    def __init__(self, parent):

        glade_xml = gui.get_glade_xml('language-dialog.glade')
        get = glade_xml.get_widget

        self._dialog                = get('dialog')
        self._project_current_radio = get('project_current_radio_button')
        self._project_all_radio     = get('project_all_radio_button')
        self._col_main_check        = get('column_main_check_button')
        self._col_tran_check        = get('column_translation_check_button')
        self._lang_main_view        = get('language_main_tree_view')
        self._lang_tran_view        = get('language_translation_tree_view')

        self._dialog.set_transient_for(parent)
        self._dialog.set_default_response(gtk.RESPONSE_CLOSE)

        # Lists of languages
        self._langs = []

        self._init_views()
        self._set_mnemonics(glade_xml)
        self._connect_signals()
        self._list_languages()
        self._set_from_config()

    def _init_views(self):
        """Init the list of languages."""

        views = (
            self._lang_main_view,
            self._lang_tran_view
        )

        methods = (
            self._on_lang_main_view_selection_changed,
            self._on_lang_tran_view_selection_changed
        )

        for i in range(len(views)):

            view = views[i]
            view.columns_autosize()

            selection = view.get_selection()
            selection.set_mode(gtk.SELECTION_SINGLE)
            selection.unselect_all()
            selection.connect('changed', methods[i])

            store = gtk.ListStore(gobject.TYPE_STRING)
            view.set_model(store)

            cell_renderer = gtk.CellRendererText()
            tree_view_column = gtk.TreeViewColumn('', cell_renderer, text=0)
            view.append_column(tree_view_column)

    def _connect_signals(self):
        """Connect signals to widgets."""

        # Ensure that project radio buttons have the same group.
        # ValueError is raised if button already is in group.
        group = self._project_current_radio.get_group()[0]
        try:
            self._project_all_radio.set_group(group)
        except ValueError:
            pass

        # Project radio buttons
        method = self._on_project_all_radio_toggled
        self._project_all_radio.connect('toggled', method)

        # Column check buttons
        method = self._on_col_main_check_toggled
        self._col_main_check.connect('toggled', method)
        method = self._on_col_tran_check_toggled
        self._col_tran_check.connect('toggled', method)

    def _get_selected_language_row(self, view):
        """Get the selected language view row."""

        selection = view.get_selection()
        store, itr = selection.get_selected()

        if itr is None:
            return None

        row = store.get_path(itr)
        try:
            return row[0]
        except TypeError:
            return row

    def destroy(self):
        """Destroy the dialog."""

        self._dialog.destroy()

    def _list_languages(self):
        """List available languages."""

        # List languages by trying to create a dictionary object for them.
        for lang in langlib.locales:
            try:
                enchant.Dict(lang)
                self._langs.append(lang)
            except enchant.Error, detail:
                pass

        self._langs.sort()

        main_store = self._lang_main_view.get_model()
        tran_store = self._lang_tran_view.get_model()
        main_store.clear()
        tran_store.clear()

        for lang in self._langs:
            name = langlib.get_descriptive_name(lang)
            main_store.append([name])
            tran_store.append([name])

    def _on_col_main_check_toggled(self, check_button):
        """Set checking of main texts."""

        check = check_button.get_active()
        config.spell_check.check_main = check
        self._lang_main_view.set_sensitive(check)

    def _on_col_tran_check_toggled(self, check_button):
        """Set checking of translation texts."""

        check = check_button.get_active()
        config.spell_check.check_translation = check
        self._lang_tran_view.set_sensitive(check)

    def _on_lang_main_view_selection_changed(self, *args):
        """Set main text language."""

        row = self._get_selected_language_row(self._lang_main_view)
        if row is None:
            return
        config.spell_check.main_language = self._langs[row]

    def _on_lang_tran_view_selection_changed(self, *args):
        """Set translation text language."""

        row = self._get_selected_language_row(self._lang_tran_view)
        if row is None:
            return
        config.spell_check.translation_language = self._langs[row]

    def _on_project_all_radio_toggled(self, radio_button):
        """Set project to check."""

        check_all = radio_button.get_active()
        config.spell_check.check_all_projects = check_all

    def run(self):
        """Show and run the dialog."""

        self._dialog.show()
        return self._dialog.run()

    def _set_from_config(self):
        """Set values from config."""

        # Projects
        check_all = config.spell_check.check_all_projects
        self._project_all_radio.set_active(check_all)

        # Columns
        check_main = config.spell_check.check_main
        check_tran = config.spell_check.check_translation
        self._col_main_check.set_active(check_main)
        self._col_tran_check.set_active(check_tran)
        self._lang_main_view.set_sensitive(check_main)
        self._lang_tran_view.set_sensitive(check_tran)

        # Languages
        main_selection = self._lang_main_view.get_selection()
        tran_selection = self._lang_tran_view.get_selection()
        main_lang = config.spell_check.main_language
        tran_lang = config.spell_check.translation_language
        try:
            row = self._langs.index(main_lang)
            main_selection.select_path(row)
        except ValueError:
            pass
        try:
            row = self._langs.index(tran_lang)
            tran_selection.select_path(row)
        except ValueError:
            pass

    def _set_mnemonics(self, glade_xml):
        """Set mnemonics for widgets."""

        text_label = glade_xml.get_widget('language_main_label')
        text_label.set_mnemonic_widget(self._lang_main_view)
        tran_label = glade_xml.get_widget('language_translation_label')
        tran_label.set_mnemonic_widget(self._lang_tran_view)
