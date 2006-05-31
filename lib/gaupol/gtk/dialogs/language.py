# Copyright (C) 2005 Osmo Salomaa
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


try:
    from psyco.classes import *
except ImportError:
    pass

try:
    import enchant
except ImportError:
    pass
except enchant.Error:
    pass

import gobject
import gtk

from gaupol.base.util import langlib
from gaupol.gtk.util  import config, gtklib


class LanguageDialog(object):

    """Dialog for configuring spell-check."""

    def __init__(self, parent):

        glade_xml = gtklib.get_glade_xml('language-dialog')
        get = glade_xml.get_widget

        self._col_main_check    = get('columns_main_check_button')
        self._col_tran_check    = get('columns_translation_check_button')
        self._dialog            = get('dialog')
        self._lang_main_view    = get('languages_main_tree_view')
        self._lang_tran_view    = get('languages_translation_tree_view')
        self._prj_all_radio     = get('projects_all_radio_button')
        self._prj_current_radio = get('projects_current_radio_button')

        # List of languages
        self._langs = []

        self._init_views()
        self._init_signals()
        self._init_langs()
        self._init_data()
        self._init_sizes()

        self._dialog.set_transient_for(parent)
        self._dialog.set_default_response(gtk.RESPONSE_CLOSE)

    def _init_data(self):
        """Initialize data."""

        # Languages
        main_selection = self._lang_main_view.get_selection()
        tran_selection = self._lang_tran_view.get_selection()
        main_lang = config.spell_check.main_lang
        tran_lang = config.spell_check.tran_lang
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

        # Projects
        check_all = config.spell_check.all_projects
        self._prj_all_radio.set_active(check_all)

        # Columns
        check_main = config.spell_check.main
        check_tran = config.spell_check.tran
        self._col_main_check.set_active(check_main)
        self._col_tran_check.set_active(check_tran)
        self._lang_main_view.set_sensitive(check_main)
        self._lang_tran_view.set_sensitive(check_tran)

    def _init_langs(self):
        """Initialize list of available languages."""

        # List languages by trying to create a dictionary object for them.
        for lang in langlib.locales:
            try:
                enchant.Dict(lang)
                self._langs.append(lang)
            except enchant.Error:
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

    def _init_signals(self):
        """Initialize signals."""

        method = self._on_prj_all_radio_toggled
        self._prj_all_radio.connect('toggled', method)
        method = self._on_col_main_check_toggled
        self._col_main_check.connect('toggled', method)
        method = self._on_col_tran_check_toggled
        self._col_tran_check.connect('toggled', method)

        selection = self._lang_main_view.get_selection()
        method = self._on_lang_main_view_selection_changed
        selection.connect('changed', method)
        selection = self._lang_tran_view.get_selection()
        method = self._on_lang_tran_view_selection_changed
        selection.connect('changed', method)

    def _init_sizes(self):
        """Initialize widget sizes."""

        width, height = gtklib.get_tree_view_size(self._lang_main_view)
        width  = (width * 2) + 100 + gtklib.EXTRA
        height = height      + 267 + gtklib.EXTRA
        gtklib.resize_dialog(self._dialog, width, height, 0.5, 0.5)

    def _init_views(self):
        """Initialize language views."""

        for view in (self._lang_main_view, self._lang_tran_view):
            view.columns_autosize()
            selection = view.get_selection()
            selection.set_mode(gtk.SELECTION_SINGLE)
            selection.unselect_all()
            store = gtk.ListStore(gobject.TYPE_STRING)
            view.set_model(store)
            cell_renderer = gtk.CellRendererText()
            tree_view_column = gtk.TreeViewColumn('', cell_renderer, text=0)
            view.append_column(tree_view_column)

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

    def _on_col_main_check_toggled(self, check_button):
        """Set checking of main texts."""

        check = check_button.get_active()
        config.spell_check.main = check
        self._lang_main_view.set_sensitive(check)

    def _on_col_tran_check_toggled(self, check_button):
        """Set checking of translation texts."""

        check = check_button.get_active()
        config.spell_check.tran = check
        self._lang_tran_view.set_sensitive(check)

    def _on_lang_main_view_selection_changed(self, *args):
        """Set main text language."""

        row = self._get_selected_language_row(self._lang_main_view)
        if row is not None:
            config.spell_check.main_lang = self._langs[row]

    def _on_lang_tran_view_selection_changed(self, *args):
        """Set translation text language."""

        row = self._get_selected_language_row(self._lang_tran_view)
        if row is not None:
            config.spell_check.tran_lang = self._langs[row]

    def _on_prj_all_radio_toggled(self, radio_button):
        """Set project to check."""

        check_all = radio_button.get_active()
        config.spell_check.all_projects = check_all

    def run(self):
        """Show and run the dialog."""

        self._dialog.show()
        return self._dialog.run()


if __name__ == '__main__':

    from gaupol.test import Test

    class TestLanguageDialog(Test):

        def __init__(self):

            Test.__init__(self)
            self.dialog = LanguageDialog(gtk.Window())

        def test_get_selected_language_row(self):

            view = self.dialog._lang_main_view
            selection = view.get_selection()

            selection.unselect_all()
            assert self.dialog._get_selected_language_row(view) is None

            selection.select_path(0)
            assert self.dialog._get_selected_language_row(view) == 0

        def test_signals(self):

            self.dialog._prj_all_radio.emit('toggled')
            self.dialog._col_main_check.emit('toggled')
            self.dialog._col_tran_check.emit('toggled')

            selection = self.dialog._lang_main_view.get_selection()
            selection.emit('changed')
            selection = self.dialog._lang_tran_view.get_selection()
            selection.emit('changed')

    TestLanguageDialog().run()
