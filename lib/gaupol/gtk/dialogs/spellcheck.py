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


# PyEnchant problems:
# (1) Unicoding
# (2) User dictionaries
# (3) Memory freeing
# (4) Replacement handling
#
# (1) Unicoding between Python, Enchant and GTK widgets seems very
# unpredictable. To be on the safe side, all acquired text from where-ever is
# always converted to unicode.
#
# (2) By default PyEnchant uses a single broker for all dictionaries. This
# seems to cause that user dictionaries (a.k.a. personal word lists) all end up
# writing to the same file. Solution: Use a separate broker for main text and
# translation text.
#
# (3) PyEnchant (or Enchant) seems to have problems freeing dictionaries after
# the spell check dialog has been closed and properly destroyed. This seems to
# be a problem when using PyEnchant's default way of having one module-global
# broker object. By creating a new broker every time, we avoid AssertionErrors
# when creating dictionaries, but the memory problems remain.
#
# (4) enchant.Dict method store_replacement seems to have no effect, at least
# with Aspell. Replacements can be handled internally with better reliability.


try:
    from psyco.classes import *
except ImportError:
    pass

try:
    import enchant
    import enchant.checker
except ImportError:
    pass
except enchant.Error:
    pass

from gettext import gettext as _
import codecs
import logging
import os

import gobject
import gtk
import pango

from gaupol.base.util            import langlib, listlib
from gaupol.base.cons            import Document
from gaupol.gtk.dialogs.message  import ErrorDialog
from gaupol.gtk.dialogs.textedit import TextEditDialog
from gaupol.gtk.error            import Cancelled
from gaupol.gtk.util             import config, gtklib


logger = logging.getLogger()

SPELL_CHECK_DIR = os.path.join(
    os.path.expanduser('~'),
    '.gaupol',
    'spell-check'
)

repl_sep = '|'

MAIN = Document.MAIN
TRAN = Document.TRAN


class SpellCheckErrorDialog(ErrorDialog):

    """Dialog to inform that spell-check initialization failed."""

    def __init__(self, parent, language, message):

        title   = _('Failed to initialize dictionary for language "%s"') \
                  % language
        message = _('%s.') % message
        ErrorDialog.__init__(self, parent, title, message)


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

        glade_xml = gtklib.get_glade_xml('spellcheck-dialog')
        get_widget = glade_xml.get_widget

        # Widgets
        self._add_button          = get_widget('add_button')
        self._add_lower_button    = get_widget('add_lower_button')
        self._check_button        = get_widget('check_button')
        self._close_button        = get_widget('close_button')
        self._dialog              = get_widget('dialog')
        self._dictionary_label    = get_widget('dictionary_label')
        self._edit_button         = get_widget('edit_button')
        self._entry               = get_widget('entry')
        self._ignore_all_button   = get_widget('ignore_all_button')
        self._ignore_button       = get_widget('ignore_button')
        self._join_back_button    = get_widget('join_back_button')
        self._join_forward_button = get_widget('join_forward_button')
        self._language_label      = get_widget('language_label')
        self._main_vbox           = get_widget('main_vbox')
        self._replace_all_button  = get_widget('replace_all_button')
        self._replace_button      = get_widget('replace_button')
        self._suggestion_view     = get_widget('suggestion_tree_view')
        self._text_view           = get_widget('text_view')

        # Pages to check
        self._pages = pages

        # PyEnchant objects
        self._brokers  = [enchant.Broker(), enchant.Broker()]
        self._checkers = [None, None]

        # Language codes and descriptive names
        self._langs = [
            config.spell_check.main_lang,
            config.spell_check.tran_lang
        ]
        self._lang_names = [None, None]

        # Current checking position
        self._page     = None
        self._document = None
        self._texts    = None
        self._row      = None

        # Replacement tuples (misspelled, correct)
        self._replacements = [[], []]

        # Corrected data
        self._corrected_rows  = [[], []]
        self._corrected_texts = [[], []]

        self._init_spell_check()
        self._init_fonts()
        self._init_sensitivities()
        self._init_text_tags()
        self._init_suggestion_view()
        self._init_signals()
        self._init_sizes()

        self._dialog.set_transient_for(parent)
        self._dialog.set_default_response(gtk.RESPONSE_CLOSE)

    def _init_checker(self, document):
        """Initialize spell-checker for document."""

        lang   = self._langs[document]
        name   = self._lang_names[document]
        broker = self._brokers[document]
        path   = os.path.join(SPELL_CHECK_DIR, lang + '.dict')
        dialog = None

        try:
            try:
                dictionary = enchant.DictWithPWL(lang, path, broker)
            except IOError, (no, message):
                message = 'Failed to create user dictionary file "%s": %s.' \
                          % (path, message)
                logger.error(message)
                self._dictionary_label.set_sensitive(False)
                self._add_button.set_sensitive(False)
                self._add_lower_button.set_sensitive(False)
                dictionary = enchant.Dict(lang, broker)
        except enchant.Error, message:
            dialog = SpellCheckErrorDialog(self._dialog, name, message)
            dialog.run()
            dialog.destroy()
            raise Cancelled

        self._checkers[document] = enchant.checker.SpellChecker(dictionary, '')

    def _init_fonts(self):
        """Initialize fonts."""

        if not config.editor.use_default_font:
            gtklib.set_widget_font(self._text_view      , config.editor.font)
            gtklib.set_widget_font(self._entry          , config.editor.font)
            gtklib.set_widget_font(self._suggestion_view, config.editor.font)

    def _init_lang_name(self, document):
        """Initialize language descriptive name for document."""

        lang = self._langs[document]
        name = langlib.get_descriptive_name(lang)
        self._lang_names[document] = name

    def _init_replacements(self, document):
        """Initialize replacements for document."""

        lang = self._langs[document]
        path = os.path.join(SPELL_CHECK_DIR, lang + '.repl')

        if not os.path.isfile(path):
            return

        # Read replacement file.
        try:
            replacement_file = codecs.open(path, 'r', 'utf_8')
            try:
                replacements = replacement_file.readlines()
            finally:
                replacement_file.close()
        except IOError, (no, message):
            message = 'Failed to read replacement file "%s": %s.' \
                      % (path, message)
            logger.error(message)
            return
        except UnicodeDecodeError, message:
            message = 'Failed to decode replacement file "%s": %s.' \
                      % (path, message)
            logger.error(message)
            return

        # Parse replacements.
        replacements = listlib.remove_duplicates(replacements)
        for replacement in replacements:
            replacement = replacement.strip()
            if replacement.find(repl_sep) == -1:
                continue
            entry = tuple(replacement.split(repl_sep))
            self._replacements[document].append(entry)

    def _init_sensitivities(self):
        """Initialize sensitivities."""

        self._replace_button.set_sensitive(False)
        self._replace_all_button.set_sensitive(False)
        self._join_back_button.set_sensitive(False)
        self._join_forward_button.set_sensitive(False)
        self._check_button.set_sensitive(False)

    def _init_signals(self):
        """Initialize signals."""

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
        self._dialog.connect('delete-event', self._destroy)

    def _init_sizes(self):
        """Initialize widget sizes."""

        # Set suggestion list width to 30 ex.
        label = gtk.Label('x' * 30)
        if not config.editor.use_default_font:
            gtklib.set_label_font(label, config.editor.font)
        width = label.size_request()[0]
        self._suggestion_view.set_size_request(width + 4, -1)

        # Set text view width to 46 ex and height to 4 lines.
        label = gtk.Label('\n'.join(['x' * 46] * 4))
        if not config.editor.use_default_font:
            gtklib.set_label_font(label, config.editor.font)
        width, height = label.size_request()
        self._text_view.set_size_request(width + 4, height + 7)

    def _init_spell_check(self):
        """Initialize spell check."""

        # Create profile directory if it doesn't exist.
        if not os.path.isdir(SPELL_CHECK_DIR):
            try:
                os.makedirs(SPELL_CHECK_DIR)
            except OSError, message:
                message = 'Failed to create spell-check profile directory ' \
                          '"%s": %s.' % (SPELL_CHECK_DIR, message)
                logger.error(message)

        if config.spell_check.main:
            self._init_lang_name(MAIN)
            self._init_checker(MAIN)
            self._init_replacements(MAIN)

        if config.spell_check.tran:
            self._init_lang_name(TRAN)
            self._init_checker(TRAN)
            self._init_replacements(TRAN)

    def _init_suggestion_view(self):
        """Initialize suggestions view."""

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

    def _init_text_tags(self):
        """Init text tags."""

        text_buffer = self._text_view.get_buffer()
        text_buffer.create_tag('misspelled', weight=pango.WEIGHT_BOLD)

    def _add_correction(self, row, text):
        """Add row and text to the lists of corrections."""

        self._corrected_rows[self._document].append(row)
        self._corrected_texts[self._document].append(text)

    def _advance(self):
        """Advance to next spelling error."""

        checker = self._checkers[self._document]

        # Move to next error in current text.
        try:
            checker.next()

        # Done with current text.
        except StopIteration:

            # Add correction.
            new_text = unicode(checker.get_text())
            old_text = self._texts[self._row]
            if new_text != old_text:
                self._add_correction(self._row, new_text)

            # Set next text for checker or return if done.
            try:
                self._set_next_text()
            except IndexError:
                self._set_done()
                return

            # Advance to next error.
            return self._advance()

        self.emit('cell-selected', self._page, self._row, self._document)

        # Show text.
        text = unicode(checker.get_text())
        text_buffer = self._text_view.get_buffer()
        text_buffer.set_text(text)

        # Highlight misspelled word.
        start = checker.wordpos
        end = start + len(checker.word)
        start_iter = text_buffer.get_iter_at_offset(start)
        end_iter = text_buffer.get_iter_at_offset(end)
        text_buffer.apply_tag_by_name('misspelled', start_iter, end_iter)

        # Set sensitivities of join buttons.
        sensitive = text[max(0, start - 1):start].isspace()
        self._join_back_button.set_sensitive(sensitive)
        sensitive = text[end:min(len(text), end + 1)].isspace()
        self._join_forward_button.set_sensitive(sensitive)

        # Add suggestions.
        self._entry.set_text(u'')
        self._fill_suggestion_view(checker.suggest())
        self._suggestion_view.grab_focus()

    def _destroy(self, *args):
        """Destroy the dialog after registering changes."""

        self._register_changes()
        self._set_done()
        self._dialog.destroy()
        self.emit('destroyed')

    def _get_selected_suggestion(self):
        """Get the selected suggestion."""

        selection = self._suggestion_view.get_selection()
        store, itr = selection.get_selected()
        if itr is None:
            return None
        return store.get_value(itr, 0)

    def _fill_suggestion_view(self, suggestions, select=True):
        """Fill the list of suggestions."""

        suggestions = suggestions[:]
        checker = self._checkers[self._document]
        replacements = self._replacements[self._document]
        store = self._suggestion_view.get_model()
        store.clear()

        # Add replacement matches.
        word = unicode(checker.word)
        for misspelled, correct in replacements:
            if misspelled == word:
                store.append([unicode(correct)])
                try:
                    suggestions.remove(correct)
                except ValueError:
                    pass

        # Add spell-checker's suggestions.
        for suggestion in suggestions:
            store.append([unicode(suggestion)])

        if len(store) > 0:
            selection = self._suggestion_view.get_selection()
            selection.unselect_all()
            if select:
                selection.select_path(0)

    def _on_add_button_clicked(self, *args):
        """Add word to personal word list."""

        checker = self._checkers[self._document]
        word = unicode(checker.word)
        checker.dict.add_to_pwl(word)
        self._advance()

    def _on_add_lower_button_clicked(self, *args):
        """Add word as lowercase to personal word list."""

        checker = self._checkers[self._document]
        word = unicode(checker.word).lower()
        checker.dict.add_to_pwl(word)
        self._advance()

    def _on_check_button_clicked(self, *args):
        """Check current word in the entry."""

        checker = self._checkers[self._document]
        word = unicode(self._entry.get_text())
        suggestions = checker.suggest(word)
        self._fill_suggestion_view(suggestions, False)

    def _on_edit_button_clicked(self, *args):
        """Edit the text in a dialog."""

        checker = self._checkers[self._document]
        text = unicode(checker.get_text())
        dialog = TextEditDialog(self._dialog, text)
        response = dialog.run()
        text = unicode(dialog.get_text())
        gtklib.destroy_gobject(dialog)

        if response == gtk.RESPONSE_OK:
            checker.set_text(text)
            self._advance()

    def _on_entry_changed(self, entry):
        """Set sensitivity of replace buttons."""

        # BUG:
        # The sensitivity setting in this method causes inability to click the
        # same replace button twice without moving the mouse outside the button
        # between the clicks. This is probably a GTK bug.

        sensitive = bool(entry.get_text())
        self._replace_button.set_sensitive(sensitive)
        self._replace_all_button.set_sensitive(sensitive)
        self._check_button.set_sensitive(sensitive)

    def _on_ignore_all_button_clicked(self, *args):
        """Ignore all instances of word."""

        checker = self._checkers[self._document]
        checker.ignore_always()
        self._advance()

    def _on_ignore_button_clicked(self, *args):
        """Ignore misspelled word."""

        self._advance()

    def _on_join_back_button_clicked(self, *args):
        """Join word with the preceding word."""

        checker = self._checkers[self._document]
        text = unicode(checker.get_text())
        start = checker.wordpos
        text = text[:start - 1] + text[start:]
        checker.set_text(text)
        self._advance()

    def _on_join_forward_button_clicked(self, *args):
        """Join word with the following word."""

        checker = self._checkers[self._document]
        text = unicode(checker.get_text())
        start = checker.wordpos
        end = start + len(checker.word)
        text = text[:end] + text [end + 1:]
        checker.set_text(text)
        self._advance()

    def _on_replace_all_button_clicked(self, *args):
        """Replace all instances of word with the word in the entry."""

        checker = self._checkers[self._document]
        misspelled = unicode(checker.word)
        correct = unicode(self._entry.get_text())
        self._store_replacement(misspelled, correct)
        checker.replace_always(correct)
        self._advance()

    def _on_replace_button_clicked(self, *args):
        """Replace word with the word in the entry."""

        checker = self._checkers[self._document]
        misspelled = unicode(checker.word)
        correct = unicode(self._entry.get_text())
        self._store_replacement(misspelled, correct)
        checker.replace(correct)
        self._advance()

    def _on_suggestion_view_selection_changed(self, *args):
        """Copy the selected suggestion into the entry."""

        suggestion = self._get_selected_suggestion()
        if suggestion is not None:
            self._entry.set_text(unicode(suggestion))

    def _register_changes(self):
        """Register changes and empty the lists of corrections."""

        self.emit(
            'page-checked',
            self._page,
            self._corrected_rows,
            self._corrected_texts
        )

        self._corrected_rows  = [[], []]
        self._corrected_texts = [[], []]

    def _set_document(self, document):
        """Set start position for checking document."""

        self._document = document
        self._set_language_label(document)
        self._row = 0

        if document == MAIN:
            self._texts = self._page.project.main_texts
        elif document == TRAN:
            self._texts = self._page.project.tran_texts

    def _set_done(self):
        """Set checking done."""

        self._text_view.get_buffer().set_text('')
        self._fill_suggestion_view([])
        self._main_vbox.set_sensitive(False)
        self._write_replacements()

    def _set_language_label(self, document):
        """Set name in the language label."""

        name = self._lang_names[document]
        self._language_label.set_text('<b>%s</b>' % name)
        self._language_label.set_use_markup(True)

    def _set_next_text(self):
        """
        Set the next text for spell-checker.

        Raise IndexError if there are no more texts to check.
        """
        # Move to next row, document or page.
        try:
            self._texts[self._row + 1]
            self._row += 1
        except IndexError:
            if self._document == MAIN and config.spell_check.tran:
                self._set_document(TRAN)
            else:
                self._register_changes()
                index = self._pages.index(self._page)
                self._set_page(self._pages[index + 1])

        try:
            text = unicode(self._texts[self._row])
        except IndexError:
            return self._set_next_text()
        self._checkers[self._document].set_text(text)

    def _set_page(self, page):
        """Set start position for checking page."""

        self._page = page
        self.emit('page-selected', self._page)

        if config.spell_check.main:
            self._set_document(MAIN)
        elif config.spell_check.tran:
            self._set_document(TRAN)

    def show(self):
        """Show the dialog and start the spell-check."""

        # Set start position.
        self._set_page(self._pages[0])
        self._row = -1
        self._set_next_text()

        self._dialog.show()
        self._advance()

    def _store_replacement(self, misspelled, correct):
        """Store replacement."""

        replacements = self._replacements[self._document]
        for entry in replacements:
            if entry == (misspelled, correct):
                return
        replacements.append((misspelled, correct))

    def _write_replacements(self):
        """Write replacement info to files."""

        for i, replacements in enumerate(self._replacements):

            if not replacements:
                continue
            replacements = listlib.remove_duplicates(replacements)

            lang = self._checkers[i].lang
            path = os.path.join(SPELL_CHECK_DIR, lang + '.repl')
            try:
                replacement_file = codecs.open(path, 'w', 'utf_8')
                try:
                    for misspelled, correct in replacements:
                        info = misspelled, repl_sep, correct, os.linesep
                        replacement_file.write('%s%s%s%s' % info)
                finally:
                    replacement_file.close()
            except IOError, (no, message):
                message = 'Failed to write replacement file "%s": %s.' \
                          % (path, message)
                logger.error(message)
            except UnicodeEncodeError, message:
                message = 'Failed to encode replacement file "%s": %s.' \
                          % (path, message)
                logger.error(message)


if __name__ == '__main__':

    from gaupol.gtk.page import Page
    from gaupol.test     import Test

    class TestSpellCheckErrorDialog(Test):

        def test_init(self):

            SpellCheckErrorDialog(gtk.Window(), 'test', 'test')

    class TestSpellCheckDialog(Test):

        def __init__(self):

            Test.__init__(self)

            page_1 = Page()
            page_1.project = self.get_project()
            page_1.project.remove_subtitles([1])
            page_2 = Page()
            page_2.project = self.get_project()
            page_2.project.remove_subtitles([1])
            pages  = [page_1, page_2]

            config.spell_check.main_lang        = 'en_CA'
            config.spell_check.tran_lang = 'en_CA'
            config.spell_check.main        = True
            config.spell_check.tran = True

            self.repl_path = os.path.join(SPELL_CHECK_DIR, 'en_CA.repl')
            self.dict_path = os.path.join(SPELL_CHECK_DIR, 'en_CA.dict')

            self.remove_repl = True
            self.remove_dict = True

            if os.path.isfile(self.repl_path):
                self.remove_repl = False
            if os.path.isfile(self.dict_path):
                self.remove_dict = False

            self.dialog = SpellCheckDialog(gtk.Window(), pages)

        def destroy(self):

            if self.remove_repl:
                try:
                    os.remove(self.repl_path)
                except OSError:
                    pass
            if self.remove_dict:
                try:
                    os.remove(self.dict_path)
                except OSError:
                    pass

        def test_all(self):

            self.dialog.show()
            self._test_get_selected_suggestion()
            self._test_signals()
            self.dialog._destroy()

        def _test_get_selected_suggestion(self):

            suggestion = self.dialog._get_selected_suggestion()
            assert isinstance(suggestion, basestring)

        def _test_signals(self):

            self.dialog._add_button.emit('clicked')
            self.dialog._add_lower_button.emit('clicked')
            self.dialog._check_button.emit('clicked')
            self.dialog._edit_button.emit('clicked')
            self.dialog._ignore_all_button.emit('clicked')
            self.dialog._ignore_button.emit('clicked')
            self.dialog._join_back_button.emit('clicked')
            self.dialog._join_forward_button.emit('clicked')
            self.dialog._replace_all_button.emit('clicked')
            self.dialog._replace_button.emit('clicked')

    TestSpellCheckErrorDialog().run()
    TestSpellCheckDialog().run()
