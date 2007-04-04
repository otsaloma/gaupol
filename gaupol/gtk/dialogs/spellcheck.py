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


"""Dialog for checking spelling.

Instance variables:

    _SPELL_CHECK_DIR: Directory for user dictionary and replacement files
"""


import gobject
import gtk
import os
import sys
import pango
from gettext import gettext as _

from gaupol import langlib, paths
from gaupol.gtk import conf, cons, util
from gaupol.gtk.index import *
from .glade import GladeDialog
from .message import ErrorDialog
from .textedit import TextEditDialog

try:
    import enchant
    import enchant.checker
except Exception:
    pass


_SPELL_CHECK_DIR = os.path.join(paths.PROFILE_DIR, "spell-check")


class SpellCheckDialog(GladeDialog):

    """Dialog for checking spelling.

    Instance variables:

        _add_button:          gtk.Button
        _check_button:        gtk.Button
        _checker:             enchant.checker.SpellChecker
        _dict_label:          gtk.Label
        _doc:                 DOCUMENT constant to check
        _edit_button:         gtk.Button
        _entry:               gtk.Entry
        _ignore_all_button:   gtk.Button
        _ignore_button:       gtk.Button
        _join_back_button:    gtk.Button
        _join_forward_button: gtk.Button
        _lang_label:          gtk.Label
        _main_vbox:           gtk.VBox
        _new_rows:            List of rows with changed texts
        _new_texts:           List of changed texts
        _page:                Current page
        _replace_all_button:  gtk.Button
        _replace_button:      gtk.Button
        _replacements:        List of used replacements
        _row:                 Current row
        _text_view:           gtk.TextView
        _tree_view:           gtk.TreeView
        application:          Associated Application
    """

    def __init__(self, parent, application):

        GladeDialog.__init__(self, "spellcheck-dialog")
        get_widget = self._glade_xml.get_widget
        self._add_button          = get_widget("add_button")
        self._check_button        = get_widget("check_button")
        self._dict_label          = get_widget("dict_label")
        self._edit_button         = get_widget("edit_button")
        self._entry               = get_widget("entry")
        self._ignore_all_button   = get_widget("ignore_all_button")
        self._ignore_button       = get_widget("ignore_button")
        self._join_back_button    = get_widget("join_back_button")
        self._join_forward_button = get_widget("join_forward_button")
        self._lang_label          = get_widget("lang_label")
        self._main_vbox           = get_widget("main_vbox")
        self._replace_all_button  = get_widget("replace_all_button")
        self._replace_button      = get_widget("replace_button")
        self._text_view           = get_widget("text_view")
        self._tree_view           = get_widget("tree_view")

        self._checker      = None
        self._doc          = None
        self._new_rows     = []
        self._new_texts    = []
        self._page         = None
        self._replacements = []
        self._row          = None
        self.application   = application

        self._init_spell_check()
        self._init_fonts()
        self._init_tree_view()
        self._init_sensitivities()
        self._init_signal_handlers()
        self._init_sizes()
        self._dialog.set_transient_for(parent)
        self._dialog.set_default_response(gtk.RESPONSE_CLOSE)

        self.pager = self._get_page()
        self.pager.next()
        self._advance()

    def _advance(self):
        """Advance to the next spelling error."""

        while True:
            try:
                return self._advance_current()
            except StopIteration:
                text = unicode(self._checker.get_text())
                texts = self._page.project.get_texts(self._doc)
                if self._row < len(texts) and text != texts[self._row]:
                    self._new_rows.append(self._row)
                    self._new_texts.append(text)
            try:
                self._set_next_text()
            except StopIteration:
                try:
                    self.pager.next()
                except StopIteration:
                    break
        self._set_done()

    def _advance_current(self):
        """Advance to the next spelling error in current text.

        Raise StopIteration when done with the current text.
        """
        self._checker.next()
        col = self._page.document_to_text_column(self._doc)
        self._page.view.set_focus(self._row, col)
        self._page.view.scroll_to_row(self._row)

        text = unicode(self._checker.get_text())
        text_buffer = self._text_view.get_buffer()
        text_buffer.set_text(text)
        a = self._checker.wordpos
        z = a + len(self._checker.word)
        start = text_buffer.get_iter_at_offset(a)
        end = text_buffer.get_iter_at_offset(z)
        text_buffer.apply_tag_by_name("misspelled", start, end)

        sensitive = text[max(0, a - 1):a].isspace()
        self._join_back_button.set_sensitive(sensitive)
        sensitive = text[z:min(len(text), z + 1)].isspace()
        self._join_forward_button.set_sensitive(sensitive)
        self._entry.set_text("")
        self._fill_tree_view(self._checker.suggest())
        self._tree_view.grab_focus()

    def _fill_tree_view(self, suggestions, select=True):
        """Fill the tree view with suggestions."""

        suggestions = suggestions[:]
        store = self._tree_view.get_model()
        store.clear()
        word = unicode(self._checker.word)
        for misspelled, correct in reversed(self._replacements):
            if misspelled == word:
                store.append([unicode(correct)])
                if correct in suggestions:
                    suggestions.remove(correct)
        for suggestion in suggestions:
            store.append([unicode(suggestion)])

        if len(store) > 0 and select:
            self._tree_view.set_cursor(0)
            self._tree_view.scroll_to_cell(0)

    def _get_page(self):
        """Get the next page."""

        for page in self._get_target_pages():
            index = self.application.pages.index(page)
            self.application.notebook.set_current_page(index)
            self._page = page
            self._doc = page.text_column_to_document(conf.spell_check.col)
            self._row = -1
            self._set_next_text()
            yield page
            self._register_changes()

    def _get_target_pages(self):
        """Get pages corresponding to target."""

        if conf.spell_check.target == cons.TARGET.ALL:
            return self.application.pages
        return [self.application.get_current_page()]

    def _init_checker(self):
        """Initialize the checker."""

        lang = conf.spell_check.lang
        path = os.path.join(_SPELL_CHECK_DIR, lang + ".dict")
        try:
            try:
                dic = enchant.DictWithPWL(str(lang), str(path))
            except IOError, (no, message):
                util.handle_write_io(sys.exc_info(), path)
                self._dict_label.set_sensitive(False)
                self._add_button.set_sensitive(False)
                dic = enchant.Dict(str(lang))
        except enchant.Error, message:
            self._show_error_dialog(message)
            self.response(gtk.RESPONSE_CLOSE)
        self._checker = enchant.checker.SpellChecker(dic, "")

    def _init_fonts(self):
        """Initialize fonts and text tags."""

        if not conf.editor.use_default_font:
            util.set_widget_font(self._entry    , conf.editor.font)
            util.set_widget_font(self._text_view, conf.editor.font)
            util.set_widget_font(self._tree_view, conf.editor.font)

        text_buffer = self._text_view.get_buffer()
        text_buffer.create_tag("misspelled", weight=pango.WEIGHT_BOLD)

    @util.silent(AssertionError)
    def _init_replacements(self):
        """Read replacements from file."""

        lang = conf.spell_check.lang
        path = os.path.join(_SPELL_CHECK_DIR, lang + ".repl")
        assert os.path.isfile(path)
        exceptions = (IOError, UnicodeError)
        readlines = util.silent(*exceptions)(util.readlines)
        lines = readlines(path, "utf_8")
        for line in util.get_unique(lines):
            entry = tuple(line.strip().split("|"))
            self._replacements.append(entry)

    def _init_sensitivities(self):
        """Initialize widget sensitivities."""

        self._check_button.set_sensitive(False)
        self._join_back_button.set_sensitive(False)
        self._join_forward_button.set_sensitive(False)
        self._replace_all_button.set_sensitive(False)
        self._replace_button.set_sensitive(False)

    def _init_signal_handlers(self):
        """Initialize signal handlers."""

        util.connect(self, "_add_button"         , "clicked")
        util.connect(self, "_check_button"       , "clicked")
        util.connect(self, "_edit_button"        , "clicked")
        util.connect(self, "_entry"              , "changed")
        util.connect(self, "_ignore_all_button"  , "clicked")
        util.connect(self, "_ignore_button"      , "clicked")
        util.connect(self, "_join_back_button"   , "clicked")
        util.connect(self, "_join_forward_button", "clicked")
        util.connect(self, "_replace_all_button" , "clicked")
        util.connect(self, "_replace_button"     , "clicked")
        util.connect(self, self, "response")

    def _init_sizes(self):
        """Initialize widget sizes."""

        label = gtk.Label("\n".join(["M" * 34] * 4))
        if not conf.editor.use_default_font:
            util.set_label_font(label, conf.editor.font)
        width, height = label.size_request()
        self._text_view.set_size_request(width + 4, height + 7)

        label = gtk.Label("M" * 24)
        if not conf.editor.use_default_font:
            util.set_label_font(label, conf.editor.font)
        width = label.size_request()[0]
        self._tree_view.set_size_request(width + 4, -1)

    def _init_spell_check(self):
        """Initialize spell-check stuff."""

        util.makedirs(_SPELL_CHECK_DIR)
        self._init_checker()
        self._init_replacements()

        name = langlib.get_long_name(conf.spell_check.lang)
        self._lang_label.set_text(name)

    def _init_tree_view(self):
        """Initialize tree view."""

        selection = self._tree_view.get_selection()
        selection.set_mode(gtk.SELECTION_SINGLE)
        selection.connect("changed", self._on_tree_view_selection_changed)
        store = gtk.ListStore(gobject.TYPE_STRING)
        self._tree_view.set_model(store)
        column = gtk.TreeViewColumn("", gtk.CellRendererText(), text=0)
        self._tree_view.append_column(column)

    def _on_add_button_clicked(self, *args):
        """Add the current word to the user dictionary."""

        self._checker.dict.add_to_pwl(unicode(self._checker.word))
        self._advance()

    def _on_check_button_clicked(self, *args):
        """Check the current word in the entry."""

        word = unicode(self._entry.get_text())
        self._fill_tree_view(self._checker.suggest(word), False)

    def _on_edit_button_clicked(self, *args):
        """Edit the current text in a separate dialog."""

        text = unicode(self._checker.get_text())
        dialog = TextEditDialog(self._dialog, text)
        response = self.run_dialog(dialog)
        text = unicode(dialog.get_text())
        dialog.destroy()
        if response == gtk.RESPONSE_OK:
            self._checker.set_text(text)
            self._advance()

    def _on_entry_changed(self, entry):
        """Set button sensitivities."""

        sensitive = bool(entry.get_text())
        self._check_button.set_sensitive(sensitive)
        self._replace_button.set_sensitive(sensitive)
        self._replace_all_button.set_sensitive(sensitive)

    def _on_ignore_all_button_clicked(self, *args):
        """Ignore all instances of the current word."""

        self._checker.ignore_always()
        self._advance()

    def _on_ignore_button_clicked(self, *args):
        """Ignore the current word."""

        self._advance()

    def _on_join_back_button_clicked(self, *args):
        """Join the current word with the preceding word."""

        text = unicode(self._checker.get_text())
        a = self._checker.wordpos
        text = text[:a - 1] + text[a:]
        self._checker.set_text(text)
        self._advance()

    def _on_join_forward_button_clicked(self, *args):
        """Join the current word with the following word."""

        text = unicode(self._checker.get_text())
        z = self._checker.wordpos + len(self._checker.word)
        text = text[:z] + text [z + 1:]
        self._checker.set_text(text)
        self._advance()

    def _on_replace_all_button_clicked(self, *args):
        """Replace all instances of the current word."""

        misspelled = unicode(self._checker.word)
        correct = unicode(self._entry.get_text())
        self._store_replacement(misspelled, correct)
        self._checker.replace_always(correct)
        self._advance()

    def _on_replace_button_clicked(self, *args):
        """Replace the current word."""

        misspelled = unicode(self._checker.word)
        correct = unicode(self._entry.get_text())
        self._store_replacement(misspelled, correct)
        self._checker.replace(correct)
        self._advance()

    def _on_response(self, dialog, response):
        """Register changes to the current page."""

        self._register_changes()
        self._set_done()

    @util.silent(AssertionError)
    def _on_tree_view_selection_changed(self, *args):
        """Copy the selected suggestion into the entry."""

        selection = self._tree_view.get_selection()
        store, itr = selection.get_selected()
        assert itr is not None
        row = store.get_path(itr)[0]
        self._entry.set_text(unicode(store[row][0]))

    @util.silent(AssertionError)
    def _register_changes(self):
        """Register changes to current page."""

        assert self._new_rows
        self._page.project.replace_texts(
            self._new_rows, self._doc, self._new_texts)
        self._page.project.set_action_description(
            cons.REGISTER.DO, _("Spell-checking"))
        self.application.update_gui()
        self._new_rows = []
        self._new_texts = []

    def _set_done(self):
        """Finish spell-checking."""

        self._text_view.get_buffer().set_text("")
        self._entry.set_text("")
        self._fill_tree_view([])
        self._main_vbox.set_sensitive(False)
        self._write_replacements()

    def _set_next_text(self):
        """Set the next text in the current page for the checker.

        Raise StopIteration when done.
        """
        texts = self._page.project.get_texts(self._doc)
        self._row += 1
        if self._row >= len(texts):
            raise StopIteration
        text = unicode(texts[self._row])
        self._checker.set_text(text)

    def _show_error_dialog(self, message):

        name = langlib.get_long_name(conf.spell_check.lang)
        title = _('Failed to load dictionary for language "%s"') % name
        message = _("%s.") % message
        dialog = ErrorDialog(self._dialog, title, message)
        dialog.add_button(gtk.STOCK_OK, gtk.RESPONSE_OK)
        self.flash_dialog(dialog)

    def _store_replacement(self, misspelled, correct):
        """Store a replacement."""

        replacements = self._replacements
        replacements.append((misspelled, correct))
        replacements = util.get_unique(replacements)
        self._replacements = replacements

    @util.silent(AssertionError)
    def _write_replacements(self):
        """Write replacement files."""

        assert self._replacements
        lang = conf.spell_check.lang
        path = os.path.join(_SPELL_CHECK_DIR, lang + ".repl")
        text = ""
        for misspelled, correct in self._replacements:
            text += "%s|%s%s" % (misspelled, correct, os.linesep)
        try:
            util.write(path, text, "utf_8")
        except (IOError, UnicodeError):
            util.handle_write_io(sys.exc_info(), path)

