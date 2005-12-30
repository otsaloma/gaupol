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


"""Dialog for spell-checking."""


# Unicoding between Python, Enchant and GTK widgets seems very unpredictable.
# To be on the safe side, all acquired text from where-ever is always converted
# to unicode.


try:
    from psyco.classes import *
except ImportError:
    pass

import enchant
import enchant.checker
import logging
import os

import gobject
import gtk
import pango

from gaupol.base.util           import langlib
from gaupol.constants           import Document
from gaupol.gtk.dialogs.message import ErrorDialog
from gaupol.gtk.error           import Cancelled
from gaupol.gtk.util            import config, gui


logger = logging.getLogger()


USER_DICT_DIR = os.path.join(os.path.expanduser('~'), '.gaupol', 'dict')


class SpellCheckErrorDialog(ErrorDialog):

    """Dialog to inform that spell-check failed."""

    def __init__(self, parent, detail):

        title  = _('Failed to start spell-check')
        ErrorDialog.__init__(self, parent, title, detail)


class TextEditDialog(gtk.Dialog):

    """Dialog for editing the text of a single subtitle."""

    def __init__(self, parent, text):

        gtk.Dialog.__init__(self)

        self.add_button(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL)
        self.add_button(gtk.STOCK_OK, gtk.RESPONSE_OK)
        self.set_default_response(gtk.RESPONSE_OK)

        self.set_has_separator(False)
        self.set_transient_for(parent)
        self.set_border_width(6)
        self.set_modal(True)

        # Create text view.
        self._text_view = gtk.TextView()
        self._text_view.set_wrap_mode(gtk.WRAP_NONE)
        text_buffer = self._text_view.get_buffer()
        text_buffer.set_text(unicode(text))

        # Put text view in a scrolled window.
        scrolled_window = gtk.ScrolledWindow()
        scrolled_window.set_border_width(6)
        scrolled_window.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scrolled_window.set_shadow_type(gtk.SHADOW_IN)
        scrolled_window.add(self._text_view)

        # Set text view size
        label = gtk.Label(unicode(text))
        width, height = label.size_request()
        width  = min(400, width  + 72)
        height = min(200, height + 36)
        self._text_view.set_size_request(width, height)

        main_vbox = self.get_child()
        main_vbox.add(scrolled_window)
        self.show_all()

    def get_text(self):
        """Get the text in the text view."""

        text_buffer = self._text_view.get_buffer()
        start, end = text_buffer.get_bounds()
        return text_buffer.get_text(start, end, True)


class SpellCheckDialog(gobject.GObject):

    """Dialog for spell-checking."""

    __gsignals__ = {
        'cell-selected': (
            gobject.SIGNAL_RUN_LAST,
            None,
            (object, gobject.TYPE_INT, gobject.TYPE_INT)
        ),
        'destroyed': (
            gobject.SIGNAL_RUN_LAST,
            None,
            ()
        ),
        'page-checked': (
            gobject.SIGNAL_RUN_LAST,
            None,
            (object, object, object)
        ),
        'page-selected': (
            gobject.SIGNAL_RUN_LAST,
            None,
            (object,)
        ),
    }

    def __init__(self, parent, pages):

        gobject.GObject.__init__(self)

        glade_xml = gui.get_glade_xml('spellcheck-dialog.glade')
        get = glade_xml.get_widget

        # Widgets
        self._add_button          = get('add_button')
        self._add_lower_button    = get('add_lower_button')
        self._check_button        = get('check_button')
        self._close_button        = get('close_button')
        self._dialog              = get('dialog')
        self._dictionary_label    = get('dictionary_label')
        self._edit_button         = get('edit_button')
        self._entry               = get('entry')
        self._ignore_all_button   = get('ignore_all_button')
        self._ignore_button       = get('ignore_button')
        self._join_back_button    = get('join_back_button')
        self._join_forward_button = get('join_forward_button')
        self._language_label      = get('language_label')
        self._main_vbox           = get('main_vbox')
        self._replace_all_button  = get('replace_all_button')
        self._replace_button      = get('replace_button')
        self._suggestion_view     = get('suggestion_tree_view')
        self._text_view           = get('text_view')

        self._dialog.set_transient_for(parent)
        self._dialog.set_default_response(gtk.RESPONSE_CLOSE)
        self._dialog.connect('delete-event', self._destroy)

        # Set initial button sensitivities to False.
        self._replace_button.set_sensitive(False)
        self._replace_all_button.set_sensitive(False)
        self._join_back_button.set_sensitive(False)
        self._join_forward_button.set_sensitive(False)
        self._check_button.set_sensitive(False)

        # Create text tag for text view.
        text_buffer = self._text_view.get_buffer()
        text_buffer.create_tag('misspelled', weight=pango.WEIGHT_BOLD)

        # Pages to check
        self._pages = pages

        # Spell-checkers
        self._main_checker = None
        self._tran_checker = None

        # Language descriptive names
        self._main_lang_name = None
        self._tran_lang_name = None

        # Current checking position
        self._page     = None
        self._document = None
        self._texts    = None
        self._checker  = None
        self._row      = None

        # Corrected data
        self._corrected_main_rows  = []
        self._corrected_main_texts = []
        self._corrected_tran_rows  = []
        self._corrected_tran_texts = []

        self._init_checkers()
        self._init_suggestion_view()
        self._set_mnemonics(glade_xml)
        self._connect_signals()

    def _init_checkers(self):
        """Initialize the spell-checkers to use."""

        # Create personal word list directory if it doesn't exist.
        if not os.path.isdir(USER_DICT_DIR):
            try:
                os.makedirs(USER_DICT_DIR)
            except OSError, detail:
                msg  = 'Failed to create user dictionary directory '
                msg += '"%s": %s.' % (USER_DICT_DIR, detail)
                logger.error(msg)

        if config.spell_check.check_main:
            lang = config.spell_check.main_language
            name, checker = self._init_checker(Document.MAIN, lang)
            self._main_lang_name = name
            self._main_checker = checker

        if config.spell_check.check_translation:
            lang = config.spell_check.translation_language
            name, checker = self._init_checker(Document.TRAN, lang)
            self._tran_lang_name = name
            self._tran_checker = checker

    def _init_checker(self, document, lang):
        """
        Initialize spell-checker for document.

        Return (Language name, enchant.checker.SpellChecker).
        """
        def show_error(detail):
            """Show error dialog and exit."""

            dialog = SpellCheckErrorDialog(self._dialog, detail)
            dialog.run()
            dialog.destroy()
            raise Cancelled

        def get_enchant_error_detail(name, detail):
            """Get detailed error string for enchant errors."""

            return _('Dictionary initialization for language "%s" returned '
                     'error: %s') % (name, detail)

        not_set_msgs = (
            _('Main text language is not set. Please use the '
              '"Configure Spell-check" dialog to select a language and then '
              'try again.'),
            _('Translation text language is not set. Please use the '
              '"Configure Spell-check" dialog to select a language and then '
              'try again.')
        )

        if lang is None:
            show_error(not_set_msgs[document])

        name = langlib.get_descriptive_name(lang)
        dict_path = os.path.join(USER_DICT_DIR, lang + '.dict')

        # Try to create dictionary with a personal word list.
        try:
            dictionary = enchant.DictWithPWL(lang, dict_path)
        except IOError, (errno, detail):
            msg = 'Failed to create user dictionary file "%s".' % dict_path
            logger.error(msg)
            self._dictionary_label.set_sensitive(False)
            self._add_button.set_sensitive(False)
            self._add_lower_button.set_sensitive(False)

            # Try to create dictionary without a personal word list.
            try:
                dictionary = enchant.Dict(lang)

        # Failed.
            except enchant.Error, detail:
                show_error(get_enchant_error_detail(name, detail))
        except enchant.Error, detail:
            show_error(get_enchant_error_detail(name, detail))

        return name, enchant.checker.SpellChecker(dictionary, u'')

    def _init_suggestion_view(self):
        """Initialize the list of suggestions."""

        view = self._suggestion_view
        view.columns_autosize()

        selection = view.get_selection()
        selection.set_mode(gtk.SELECTION_SINGLE)
        selection.unselect_all()
        method = self._on_suggestion_view_selection_changed
        self._handler = selection.connect('changed', method)

        store = gtk.ListStore(gobject.TYPE_STRING)
        view.set_model(store)

        cell_renderer = gtk.CellRendererText()
        tree_view_column = gtk.TreeViewColumn('', cell_renderer, text=0)
        view.append_column(tree_view_column)

    def _add_correction(self, row, text):
        """Add row and text to the lists of corrections."""

        if self._document == Document.MAIN:
            self._corrected_main_rows.append(row)
            self._corrected_main_texts.append(text)
        elif self._document == Document.TRAN:
            self._corrected_tran_rows.append(row)
            self._corrected_tran_texts.append(text)

    def _advance(self):
        """Advance to next spelling error."""

        # Get next error from current text.
        try:
            self._checker.next()

        # Done with current text.
        except StopIteration:

            # Add correction.
            new_text = unicode(self._checker.get_text())
            old_text = self._texts[self._row]
            if new_text != old_text:
                self._add_correction(self._row, new_text)

            # Get next text.
            try:
                self._get_next_text()

            # Done.
            except IndexError:
                self._text_view.get_buffer().set_text('')
                self._fill_suggestion_view([])
                self._main_vbox.set_sensitive(False)
                return

            # Advance to next error.
            self._advance()
            return

        self.emit('cell-selected', self._page, self._row, self._document)

        # Show text.
        text = unicode(self._checker.get_text())
        text_buffer = self._text_view.get_buffer()
        text_buffer.set_text(text)

        # Highlight mispelled word.
        start = self._checker.wordpos
        end = start + len(self._checker.word)
        start_iter = text_buffer.get_iter_at_offset(start)
        end_iter = text_buffer.get_iter_at_offset(end)
        text_buffer.apply_tag_by_name('misspelled', start_iter, end_iter)

        # Set sensitivity join buttons.
        sensitive = text[max(0, start - 1):start].isspace()
        self._join_back_button.set_sensitive(sensitive)
        sensitive = text[end:min(len(text), end + 1)].isspace()
        self._join_forward_button.set_sensitive(sensitive)

        # Add suggestions.
        self._fill_suggestion_view(self._checker.suggest())
        self._suggestion_view.grab_focus()

    def _connect_signals(self):
        """Connect signals to widgets."""

        connections = (
            (self._add_button         , self._on_add_button_clicked         ),
            (self._add_lower_button   , self._on_add_lower_button_clicked   ),
            (self._close_button       , self._destroy                       ),
            (self._check_button       , self._on_check_button_clicked       ),
            (self._edit_button        , self._on_edit_button_clicked        ),
            (self._ignore_all_button  , self._on_ignore_all_button_clicked  ),
            (self._ignore_button      , self._on_ignore_button_clicked      ),
            (self._join_back_button   , self._on_join_back_button_clicked   ),
            (self._join_forward_button, self._on_join_forward_button_clicked),
            (self._replace_all_button , self._on_replace_all_button_clicked ),
            (self._replace_button     , self._on_replace_button_clicked     ),
        )

        for button, method in connections:
            button.connect('clicked', method)

        self._entry.connect('changed', self._on_entry_changed)

    def _destroy(self, *args):
        """Destroy the dialog after registering changes."""

        self._register_changes()
        self._dialog.destroy()
        self.emit('destroyed')

    def _get_next_text(self):
        """
        Get next text for spell-checker.

        Raise IndexError if there are no more texts to check.
        """
        def set_position(document):
            """Set position for starting to check document."""

            self._document = document
            self._row = 0
            self._set_language_label(document)

            if document == Document.MAIN:
                self._texts   = self._page.project.main_texts
                self._checker = self._main_checker
            elif document == Document.TRAN:
                self._texts   = self._page.project.tran_texts
                self._checker = self._tran_checker

        # Move to next row.
        try:
            text = self._texts[self._row + 1]
            self._row += 1

        # Move from main document to translation document.
        except IndexError:
            try:
                if self._document == Document.TRAN:
                    raise IndexError
                if not config.spell_check.check_translation:
                    raise IndexError
                set_position(Document.TRAN)

            # Move to next page.
            except IndexError:

                self._register_changes()

                # Raises IndexError if we're done.
                index = self._pages.index(self._page)
                self._page = self._pages[index + 1]
                self.emit('page-selected', self._page)

                if config.spell_check.check_main:
                    set_position(Document.MAIN)
                elif config.spell_check.check_translation:
                    set_position(Document.TRAN)

        try:
            text = unicode(self._texts[self._row])
        except IndexError:
            return self._get_next_text()

        self._checker.set_text(text)

    def _get_selected_suggestion(self):
        """Get the selected suggestion."""

        selection = self._suggestion_view.get_selection()
        store, itr = selection.get_selected()
        if itr is None:
            return None
        return store.get_value(itr, 0)

    def _fill_suggestion_view(self, suggestions):
        """Fill the list of suggestions."""

        store = self._suggestion_view.get_model()
        store.clear()
        for suggestion in suggestions:
            store.append([unicode(suggestion)])

        if suggestions:
            selection = self._suggestion_view.get_selection()
            selection.unselect_all()
            selection.select_path(0)

    def _on_add_button_clicked(self, *args):
        """Add word to personal word list."""

        word = unicode(self._checker.word)
        self._checker.dict.add_to_pwl(word)
        self._advance()

    def _on_add_lower_button_clicked(self, *args):
        """Add word as lowercase to personal word list."""

        word = unicode(self._checker.word).lower()
        self._checker.dict.add_to_pwl(word)
        self._advance()

    def _on_check_button_clicked(self, *args):
        """Check current word in the entry."""

        word = unicode(self._entry.get_text())
        suggestions = self._checker.suggest(word)
        self._fill_suggestion_view(suggestions)
        self._suggestion_view.grab_focus()

    def _on_edit_button_clicked(self, *args):
        """Edit the text in a dialog."""

        text = unicode(self._checker.get_text())
        dialog = TextEditDialog(self._dialog, text)
        response = dialog.run()
        text = unicode(dialog.get_text())
        dialog.destroy()

        if response == gtk.RESPONSE_OK:
            self._checker.set_text(text)
            self._advance()

    def _on_entry_changed(self, entry):
        """Set sensitivity of replace buttons."""

        # BUG:
        # The sensitivity setting in this method causes inability to click the
        # same replace button twice without moving the mouse outside the button
        # between the clicks. This is probably a GTK bug. A workaround would be
        # needed, since this sensitivity setting cannot really be left out.

        text = unicode(entry.get_text())
        sensitive = bool(text)
        self._replace_button.set_sensitive(sensitive)
        self._replace_all_button.set_sensitive(sensitive)
        self._check_button.set_sensitive(sensitive)

    def _on_ignore_all_button_clicked(self, *args):
        """Ignore all instances of word."""

        self._checker.ignore_always()
        self._advance()

    def _on_ignore_button_clicked(self, *args):
        """Ignore mispelling of word."""

        self._advance()

    def _on_join_back_button_clicked(self, *args):
        """Join word with the preceding word."""

        text = unicode(self._checker.get_text())
        start = self._checker.wordpos
        text = text[:start - 1] + text [start:]
        self._checker.set_text(text)
        self._advance()

    def _on_join_forward_button_clicked(self, *args):
        """Join word with the following word."""

        text = unicode(self._checker.get_text())
        start = self._checker.wordpos
        end = start + len(self._checker.word)
        text = text[:end] + text [end + 1:]
        self._checker.set_text(text)
        self._advance()

    def _on_replace_all_button_clicked(self, *args):
        """Replace all instances of word with the word in the entry."""

        word = unicode(self._entry.get_text())
        self._checker.replace_always(word)
        self._replace_all_button.realize()
        self._advance()

    def _on_replace_button_clicked(self, *args):
        """Replace word with the word in the entry."""

        word = unicode(self._entry.get_text())
        self._checker.replace(word)
        self._advance()

    def _on_suggestion_view_selection_changed(self, *args):
        """Copy the selected suggestion into the entry."""

        suggestion = self._get_selected_suggestion()
        if suggestion is None:
            self._entry.set_text(u'')
        else:
            self._entry.set_text(unicode(suggestion))

    def _register_changes(self):
        """Register changes and empty the lists of corrections."""

        self.emit(
            'page-checked', self._page,
            (self._corrected_main_rows , self._corrected_tran_rows ),
            (self._corrected_main_texts, self._corrected_tran_texts)
        )

        self._corrected_main_rows  = []
        self._corrected_main_texts = []
        self._corrected_tran_rows  = []
        self._corrected_tran_texts = []

    def _set_language_label(self, document):
        """Set name in the language label."""

        name = (self._main_lang_name, self._tran_lang_name)[document]
        self._language_label.set_text('<b>%s</b>' % name)
        self._language_label.set_use_markup(True)

    def _set_mnemonics(self, glade_xml):
        """Set mnemonics for widgets."""

        # Entry
        label = glade_xml.get_widget('entry_label')
        label.set_mnemonic_widget(self._entry)

        # Suggestion view
        label = glade_xml.get_widget('suggestion_label')
        label.set_mnemonic_widget(self._suggestion_view)

    def _set_start_position(self):
        """Set start position for spell-checking."""

        self._page = self._pages[0]
        self.emit('page-selected', self._page)

        if config.spell_check.check_main:
            self._document = Document.MAIN
            self._texts    = self._page.project.main_texts
            self._checker  = self._main_checker
        elif config.spell_check.check_translation:
            self._document = Document.TRAN
            self._texts    = self._page.project.tran_texts
            self._checker  = self._tran_checker

        self._set_language_label(self._document)
        self._row = -1
        self._get_next_text()

    def show(self):
        """Show the dialog and start the spell-check."""

        self._set_start_position()
        self._dialog.show()
        self._advance()
