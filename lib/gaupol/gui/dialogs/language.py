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


"""Dialog for selecting language and target for spell-check."""


import logging

try:
    from psyco.classes import *
except ImportError:
    pass

import enchant
import gobject
import gtk

from gaupol.gui.util import gui
from gaupol.lib.util import langlib


logger = logging.getLogger()


class LanguageDialog(object):

    """Dialog for selecting language and target for spell-check."""
    
    def __init__(self, parent):

        glade_xml = gui.get_glade_xml('language-dialog.glade')
        w = glade_xml.get_widget
        
        self._dialog                   = w('dialog')
        self._doc_current_radio_button = w('document_current_radio_button')
        self._doc_all_radio_button     = w('document_all_radio_button')
        self._col_text_check_button    = w('column_text_check_button')
        self._col_tran_check_button    = w('column_translation_check_button')
        self._lang_text_tree_view      = w('language_text_tree_view')
        self._lang_tran_tree_view      = w('language_translation_tree_view')
        
        self._dialog.set_transient_for(parent)
        self._dialog.set_default_response(gtk.RESPONSE_CLOSE)
        
        # Set radio group for document radio buttons. ValueError is raised
        # if button already is in group.
        group = self._doc_current_radio_button.get_group()[0]
        try:
            self._doc_all_radio_button.set_group(group)
        except ValueError:
            pass

        # Set list mnemonics.
        text_label = w('language_text_label')
        text_label.set_mnemonic_widget(self._lang_text_tree_view)
        tran_label = w('language_translation_label')
        tran_label.set_mnemonic_widget(self._lang_tran_tree_view)
        
        self._lang_codes = []
        self._lang_names = []
        self._countries  = []
        self._providers  = []
        
        # Full language names: "language-country" to get alphabetical order
        # correct
        self._full_names = []
        
        self._list_languages()
        self._fill_language_tree_view(self._lang_text_tree_view)
        self._fill_language_tree_view(self._lang_tran_tree_view)

    def destroy(self):
        """Destroy the dialog."""
        
        self._dialog.destroy()
        
    def _fill_language_tree_view(self, tree_view):
        """Fill the language tree view with available languages."""

        model = gtk.ListStore(gobject.TYPE_STRING)
        tree_view.set_model(model)
        tree_view.set_headers_visible(False)
        
        def render_text(tree_view_column, cell_renderer, model, tree_iter):
            """Render text in the cell."""

            full_name = model.get_value(tree_iter, 0)
            index = self._full_names.index(full_name)
            markup = ''
            
            if self._lang_names[index] is not None:
                markup += '<b>%s</b>' % self._lang_names[index]
                
            if self._countries[index] is not None:
                markup += '\n%s' % self._countries[index]
            
            # TRANSLATORS: Spell-check dictionary, e.g. "aspell: en_US".
            details = self._providers[index], self._lang_codes[index]
            detail = _('%s: %s') % details
            markup += '\n<small>%s</small>' % detail
            
            cell_renderer.set_property('markup', markup)

        cell_renderer = gtk.CellRendererText()
        tree_view_column = gtk.TreeViewColumn('', cell_renderer)
        tree_view_column.set_cell_data_func(cell_renderer, render_text)
        tree_view.append_column(tree_view_column)
        
        # Add available languages to list.
        names = self._full_names[:]
        names.sort()
        for name in names:
            model.append([name])
            
        selection = tree_view.get_selection()
        selection.set_mode(gtk.SELECTION_SINGLE)
        selection.unselect_all()

    def get_check_all_documents(self):
        """Return True if all documents are chosen to be checked."""
        
        return self._doc_all_radio_button.get_active()
        
    def get_check_text(self):
        """Return True if text column is chosen to be checked."""
        
        return self._col_text_check_button.get_active()
        
    def get_check_translation(self):
        """Return True if translation column is chosen to be checked."""
        
        return self._col_tran_check_button.get_active()
        
    def _get_language(self, selection):
        """Get language from gtk.TreeSelection."""
        
        model, rows = selection.get_selected_rows()
        
        if not rows:
            return None
        else:
            row = rows[0]
        
        full_name = model[row][0]
        index = self._full_names.index(full_name)
        return self._lang_codes[index]
        
    def get_text_language(self):
        """Get language set for text column."""
        
        selection = self._lang_text_tree_view.get_selection()
        
        return self._get_language(selection)
        
    def get_translation_language(self):
        """Get language set for text column."""
        
        selection = self._lang_tran_tree_view.get_selection()
        
        return self._get_language(selection)
        
    def _list_languages(self):
        """Create lists of available languages."""

        self._lang_codes = enchant.list_languages()
        broker = enchant.Broker()
        
        # Get providers.
        for code in self._lang_codes:
        
            try:
                self._providers.append(broker.request_dict(code).provider.name)
            except enchant.Error, detail:
                logger.error(detail)
                self._providers.append(None)
    
        # Remove all languages that failed provider check.
        for i in reversed(range(len(self._providers))):
            if self._providers[i] is None:
                self._providers.pop(i)
                self._lang_codes.pop(i)
        
        # Get languages names and countries.
        for code in self._lang_codes:
        
            try:
                self._lang_names.append(langlib.get_language(code))
            except KeyError:
                self._lang_names.append(None)
                
            try:
                self._countries.append(langlib.get_country(code))
            except KeyError:
                self._countries.append(None)
        
        # Get full names.
        for i in range(len(self._lang_codes)):
            entry = '%s-%s' % (self._lang_names[i], self._countries[i])
            self._full_names.append(entry)
        
    def run(self):
        """Show and run the dialog."""
        
        self._dialog.show()
        
        return self._dialog.run()
        
    def set_check_all_documents(self, check):
        """Set whether all documents should be checked."""
        
        self._doc_all_radio_button.set_active(check)
        
    def set_check_text(self, check):
        """Set whether text column should be checked."""
        
        self._col_text_check_button.set_active(check)
        
    def set_check_translation(self, check):
        """Set whether translation column should be checked."""
        
        self._col_tran_check_button.set_active(check)
        
    def _set_language(self, selection, lang):
        """Set language from gtk.TreeSelection."""
        
        model = selection.get_tree_view().get_model()
        
        # Try language.
        try:
            index = self._lang_codes.index(lang)
        except ValueError:
        
            # Try language with only first two letters.
            try:
                index = self._lang_codes.index(lang[:2])
            except (TypeError, ValueError):
        
                # Try default language.
                try:
                    lang = enchant.Dict().tag
                    try:
                        index = self._lang_codes.index(lang)
                    except ValueError:
                    
                        # Try default language with only first two letters.
                        try:
                            index = self._lang_codes.index(lang[:2])
                        except ValueError:
                            return
                except enchant.Error:
                    return
        
        full_name = self._full_names[index]
        
        for i in range(len(model)):
            if model[i][0] == full_name:
                selection.select_path(i)
                break
        
    def set_text_language(self, lang):
        """Set language for text column."""
        
        selection = self._lang_text_tree_view.get_selection()
        
        self._set_language(selection, lang)
        
    def set_translation_language(self, lang):
        """Set language for translation column."""
        
        selection = self._lang_tran_tree_view.get_selection()
        
        self._set_language(selection, lang)
