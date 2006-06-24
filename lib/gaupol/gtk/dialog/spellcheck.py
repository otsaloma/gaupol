# Copyright (C) 2005-2006 Osmo Salomaa
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


"""Dialog for checking spelling."""


# Known problems:
# (1) Unicoding
# (2) User dictionaries
# (3) Memory freeing
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


from gettext import gettext as _
import codecs
import os

import gobject
import gtk
import pango

from gaupol.base.paths          import PROFILE_DIR
from gaupol.base.util           import langlib, listlib
from gaupol.gtk.icons           import *
from gaupol.gtk.dialog.message  import ErrorDialog
from gaupol.gtk.dialog.textedit import TextEditDialog
from gaupol.gtk.error           import Default
from gaupol.gtk.util            import conf, gtklib

try:
    import enchant
    import enchant.checker
except ImportError:
    pass
except enchant.Error:
    pass


_SPELL_CHECK_DIR = os.path.join(PROFILE_DIR, 'spell-check')
_REPL_SEP = '|'


class _ErrorDialog(ErrorDialog):

    """Dialog for informing that spell-check failed to start."""

    def __init__(self, parent, lang, message):

        try:
            name = langlib.get_long_name(lang)
        except KeyError:
            name = lang

        ErrorDialog.__init__(
            self, parent,
            _('Failed to load dictionary for language "%s"') % name,
            _('%s.') % message
        )


class SpellCheckDialog(gobject.GObject):

    """Dialog for spell-checking."""

    __gsignals__ = {
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
        """
        Initialize SpellCheckDialog object.

        Raise Default if fails.
        """
        gobject.GObject.__init__(self)

        domain = conf.spell_check
        self._brokers      = [enchant.Broker(), enchant.Broker()]
        self._checker      = None
        self._checkers     = [None, None]
        self._doc          = None
        self._langs        = [domain.main_lang, domain.tran_lang]
        self._new_rows     = [[], []]
        self._new_texts    = [[], []]
        self._page         = None
        self._pages        = pages
        self._replacements = [[], []]
        self._row          = None
        self._texts        = None

        glade_xml = gtklib.get_glade_xml('spellcheck-dialog')
        self._add_button          = glade_xml.get_widget('add_button')
        self._add_lower_button    = glade_xml.get_widget('add_lower_button')
        self._check_button        = glade_xml.get_widget('check_button')
        self._dialog              = glade_xml.get_widget('dialog')
        self._dict_label          = glade_xml.get_widget('dict_label')
        self._edit_button         = glade_xml.get_widget('edit_button')
        self._entry               = glade_xml.get_widget('entry')
        self._ignore_all_button   = glade_xml.get_widget('ignore_all_button')
        self._ignore_button       = glade_xml.get_widget('ignore_button')
        self._join_back_button    = glade_xml.get_widget('join_back_button')
        self._join_forward_button = glade_xml.get_widget('join_forward_button')
        self._lang_label          = glade_xml.get_widget('lang_label')
        self._main_vbox           = glade_xml.get_widget('main_vbox')
        self._replace_all_button  = glade_xml.get_widget('replace_all_button')
        self._replace_button      = glade_xml.get_widget('replace_button')
        self._text_view           = glade_xml.get_widget('text_view')
        self._tree_view           = glade_xml.get_widget('tree_view')

        self._init_spell_check()
        self._init_fonts()
        self._init_sensitivities()
        self._init_tree_view()
        self._init_signals()
        self._init_sizes()
        self._dialog.set_transient_for(parent)
        self._dialog.set_default_response(gtk.RESPONSE_CLOSE)

    def _advance(self):
        """Advance to next spelling error."""

        loop = True
        while loop:
            loop = self._advance_current()

    def _advance_current(self):
        """
        Advance to next spelling error in current text.

        Return True if needed to be called again.
        """
        try:
            self._checker.next()
        except StopIteration:
            new_text = unicode(self._checker.get_text())
            old_text = self._texts[self._row]
            if new_text != old_text:
                self._new_rows[self._doc].append(self._row)
                self._new_texts[self._doc].append(new_text)
            try:
                self._set_next_text()
            except IndexError:
                self._set_done()
                return False
            return True

        col = self._page.document_to_text_column(self._doc)
        self._page.view.set_focus(self._row, col)
        self._page.view.scroll_to_row(self._row)

        text = unicode(self._checker.get_text())
        text_buffer = self._text_view.get_buffer()
        text_buffer.set_text(text)
        start = self._checker.wordpos
        end = start + len(self._checker.word)
        start_iter = text_buffer.get_iter_at_offset(start)
        end_iter = text_buffer.get_iter_at_offset(end)
        text_buffer.apply_tag_by_name('misspelled', start_iter, end_iter)

        sensitive = text[max(0, start - 1):start].isspace()
        self._join_back_button.set_sensitive(sensitive)
        sensitive = text[end:min(len(text), end + 1)].isspace()
        self._join_forward_button.set_sensitive(sensitive)

        self._entry.set_text(u'')
        self._fill_tree_view(self._checker.suggest())
        self._tree_view.grab_focus()
        return False

    def _fill_tree_view(self, suggestions, select=True):
        """Fill tree view with suggestions."""

        suggestions = suggestions[:]
        store = self._tree_view.get_model()
        store.clear()
        for misspelled, correct in reversed(self._replacements[self._doc]):
            if misspelled == unicode(self._checker.word):
                store.append([unicode(correct)])
                try:
                    suggestions.remove(correct)
                except ValueError:
                    pass
        for suggestion in suggestions:
            store.append([unicode(suggestion)])

        if len(store) > 0 and select:
            self._tree_view.set_cursor(0)
            self._tree_view.scroll_to_cell(0)

    def _init_checker(self, doc):
        """
        Initialize spell-checker for document.

        Raise Default if fails.
        """
        path = os.path.join(_SPELL_CHECK_DIR, self._langs[doc] + '.dict')
        try:
            try:
                dict_ = enchant.DictWithPWL(
                    self._langs[doc], path, self._brokers[doc])
            except IOError, (no, message):
                print 'Failed to create user dictionary file "%s": %s.' % (
                    path, message)
                self._dict_label.set_sensitive(False)
                self._add_button.set_sensitive(False)
                self._add_lower_button.set_sensitive(False)
                dict_ = enchant.Dict(self._langs[doc], self._brokers[doc])
        except enchant.Error, message:
            gtklib.run(_ErrorDialog(self._dialog, self._langs[doc], message))
            raise Default
        self._checkers[doc] = enchant.checker.SpellChecker(dict_, '')

    def _init_fonts(self):
        """Initialize fonts and text tags."""

        if not conf.editor.use_default_font:
            gtklib.set_widget_font(self._entry    , conf.editor.font)
            gtklib.set_widget_font(self._text_view, conf.editor.font)
            gtklib.set_widget_font(self._tree_view, conf.editor.font)

        text_buffer = self._text_view.get_buffer()
        text_buffer.create_tag('misspelled', weight=pango.WEIGHT_BOLD)

    def _init_replacements(self, doc):
        """Initialize replacements for document."""

        path = os.path.join(_SPELL_CHECK_DIR, self._langs[doc] + '.repl')
        if not os.path.isfile(path):
            return
        try:
            fobj = codecs.open(path, 'r', 'utf_8')
            try:
                lines = fobj.readlines()
            finally:
                fobj.close()
        except IOError, (no, message):
            print 'Failed to read replacement file "%s": %s.' % (path, message)
            return
        except UnicodeDecodeError, message:
            print 'Failed to decode replacement file "%s": %s.' % (
                path, message)
            return

        lines = listlib.unique(lines)
        for line in lines:
            if line.find(_REPL_SEP) == -1:
                continue
            entry = tuple(line.strip().split(_REPL_SEP))
            self._replacements[doc].append(entry)
        while len(self._replacements[doc]) > conf.spell_check.max_repl:
            self._replacements[doc].pop(0)

    def _init_sensitivities(self):
        """Initialize sensitivities."""

        self._check_button.set_sensitive(False)
        self._join_back_button.set_sensitive(False)
        self._join_forward_button.set_sensitive(False)
        self._replace_all_button.set_sensitive(False)
        self._replace_button.set_sensitive(False)

    def _init_signals(self):
        """Initialize signals."""

        gtklib.connect(self, '_add_button'         , 'clicked' )
        gtklib.connect(self, '_add_lower_button'   , 'clicked' )
        gtklib.connect(self, '_check_button'       , 'clicked' )
        gtklib.connect(self, '_dialog'             , 'response')
        gtklib.connect(self, '_edit_button'        , 'clicked' )
        gtklib.connect(self, '_entry'              , 'changed' )
        gtklib.connect(self, '_ignore_all_button'  , 'clicked' )
        gtklib.connect(self, '_ignore_button'      , 'clicked' )
        gtklib.connect(self, '_join_back_button'   , 'clicked' )
        gtklib.connect(self, '_join_forward_button', 'clicked' )
        gtklib.connect(self, '_replace_all_button' , 'clicked' )
        gtklib.connect(self, '_replace_button'     , 'clicked' )

    def _init_sizes(self):
        """Initialize widget sizes."""

        label = gtk.Label('x' * 30)
        if not conf.editor.use_default_font:
            gtklib.set_label_font(label, conf.editor.font)
        width = label.size_request()[0]
        self._tree_view.set_size_request(width + 4, -1)

        label = gtk.Label('\n'.join(['x' * 46] * 4))
        if not conf.editor.use_default_font:
            gtklib.set_label_font(label, conf.editor.font)
        width, height = label.size_request()
        self._text_view.set_size_request(width + 4, height + 7)

    def _init_spell_check(self):
        """
        Initialize spell-check.

        Raise Default if fails.
        """
        if not os.path.isdir(_SPELL_CHECK_DIR):
            try:
                os.makedirs(_SPELL_CHECK_DIR)
            except OSError, message:
                print 'Failed to create spell-check profile directory "%s": ' \
                      '%s.' % (_SPELL_CHECK_DIR, message)

        if MTXT in conf.spell_check.cols:
            self._init_checker(MAIN)
            self._init_replacements(MAIN)
        if TTXT in conf.spell_check.cols:
            self._init_checker(TRAN)
            self._init_replacements(TRAN)

    def _init_tree_view(self):
        """Initialize tree view."""

        self._tree_view.columns_autosize()
        selection = self._tree_view.get_selection()
        selection.set_mode(gtk.SELECTION_SINGLE)
        selection.unselect_all()
        selection.connect('changed', self._on_tree_view_selection_changed)
        store = gtk.ListStore(gobject.TYPE_STRING)
        self._tree_view.set_model(store)
        column = gtk.TreeViewColumn('', gtk.CellRendererText(), text=0)
        self._tree_view.append_column(column)

    def _on_add_button_clicked(self, *args):
        """Add word to user dictionary."""

        self._checker.dict.add_to_pwl(unicode(self._checker.word))
        self._advance()

    def _on_add_lower_button_clicked(self, *args):
        """Add word in lowercase to personal word list."""

        self._checker.dict.add_to_pwl(unicode(self._checker.word).lower())
        self._advance()

    def _on_check_button_clicked(self, *args):
        """Check current word in entry."""

        word = unicode(self._entry.get_text())
        self._fill_tree_view(self._checker.suggest(word), False)

    def _on_dialog_response(self, dialog, response):
        """Register changes."""

        self._register_changes()
        self._set_done()

    def _on_edit_button_clicked(self, *args):
        """Edit text in a separate dialog."""

        text = unicode(self._checker.get_text())
        dialog = TextEditDialog(self._dialog, text)
        response = dialog.run()
        text = unicode(dialog.get_text())
        gtklib.destroy_gobject(dialog)
        if response == gtk.RESPONSE_OK:
            self._checker.set_text(text)
            self._advance()

    def _on_entry_changed(self, entry):
        """Set button sensitivities."""

        sensitive = bool(entry.get_text())
        self._check_button.set_sensitive(sensitive)
        self._replace_all_button.set_sensitive(sensitive)
        self._replace_button.set_sensitive(sensitive)

    def _on_ignore_all_button_clicked(self, *args):
        """Ignore all instances of word."""

        self._checker.ignore_always()
        self._advance()

    def _on_ignore_button_clicked(self, *args):
        """Ignore word."""

        self._advance()

    def _on_join_back_button_clicked(self, *args):
        """Join word with preceding word."""

        text = unicode(self._checker.get_text())
        start = self._checker.wordpos
        text = text[:start - 1] + text[start:]
        self._checker.set_text(text)
        self._advance()

    def _on_join_forward_button_clicked(self, *args):
        """Join word with following word."""

        text = unicode(self._checker.get_text())
        end = self._checker.wordpos + len(self._checker.word)
        text = text[:end] + text [end + 1:]
        self._checker.set_text(text)
        self._advance()

    def _on_replace_all_button_clicked(self, *args):
        """Replace all instances of word."""

        misspelled = unicode(self._checker.word)
        correct = unicode(self._entry.get_text())
        self._store_replacement(misspelled, correct)
        self._checker.replace_always(correct)
        self._advance()

    def _on_replace_button_clicked(self, *args):
        """Replace word."""

        misspelled = unicode(self._checker.word)
        correct = unicode(self._entry.get_text())
        self._store_replacement(misspelled, correct)
        self._checker.replace(correct)
        self._advance()

    def _on_tree_view_selection_changed(self, *args):
        """Copy selected suggestion into entry."""

        selection = self._tree_view.get_selection()
        try:
            row = int(selection.get_selected_rows()[1][0][0])
        except (IndexError, TypeError):
            return
        store = self._tree_view.get_model()
        self._entry.set_text(unicode(store[row][0]))

    def _register_changes(self):
        """Register changes to current page."""

        self.emit('page-checked', self._page, self._new_rows, self._new_texts)
        self._new_rows  = [[], []]
        self._new_texts = [[], []]

    def _set_document(self, doc):
        """Prepare for checking document."""

        self._doc = doc
        self._row = 0
        self._checker = self._checkers[doc]
        if doc == MAIN:
            self._texts = self._page.project.main_texts
        elif doc == TRAN:
            self._texts = self._page.project.tran_texts

        name = langlib.get_long_name(self._langs[doc])
        self._lang_label.set_text(name)

    def _set_done(self):
        """Finish spell-checking."""

        self._text_view.get_buffer().set_text('')
        self._entry.set_text('')
        self._fill_tree_view([])
        self._main_vbox.set_sensitive(False)
        self._write_replacements()

    def _set_next_text(self):
        """
        Set next text for checker.

        Raise IndexError if done.
        """
        try:
            while True:
                self._row += 1
                if self._texts[self._row]:
                    break
        except IndexError:
            if self._doc == MAIN and TTXT in conf.spell_check.cols:
                self._set_document(TRAN)
            else:
                self._register_changes()
                index = self._pages.index(self._page)
                self._set_page(self._pages[index + 1])
        try:
            text = unicode(self._texts[self._row])
        except IndexError:
            return self._set_next_text()
        self._checker.set_text(text)

    def _set_page(self, page):
        """Prepare for checking page."""

        self._page = page
        self.emit('page-selected', page)
        if MTXT in conf.spell_check.cols:
            self._set_document(MAIN)
        elif TTXT in conf.spell_check.cols:
            self._set_document(TRAN)

    def _store_replacement(self, misspelled, correct):
        """Store replacement."""

        replacements = self._replacements[self._doc]
        replacements.append((misspelled, correct))
        replacements = listlib.unique(replacements)
        while len(replacements) > conf.spell_check.max_repl:
            replacements.pop(0)
        self._replacements[self._doc] = replacements

    def _write_replacements(self):
        """Write replacement files."""

        for doc, replacements in enumerate(self._replacements):
            if not replacements:
                continue
            path = os.path.join(_SPELL_CHECK_DIR, self._langs[doc] + '.repl')
            try:
                fobj = codecs.open(path, 'w', 'utf_8')
                try:
                    for misspelled, correct in replacements:
                        fobj.write('%s%s%s%s' % (
                            misspelled, _REPL_SEP, correct, os.linesep))
                finally:
                    fobj.close()
            except IOError, (no, message):
                print 'Failed to write replacement file "%s": %s.' % (
                    path, message)
            except UnicodeEncodeError, message:
                print 'Failed to encode replacement file "%s": %s.' % (
                    path, message)

    def destroy(self):
        """Destroy dialog."""

        self._dialog.destroy()

    def run(self):
        """Run dialog."""

        self._set_page(self._pages[0])
        self._row = -1
        self._set_next_text()
        self._dialog.show()
        self._advance()

        return self._dialog.run()
