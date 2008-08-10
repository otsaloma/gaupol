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

"""Dialog for checking spelling."""

import gaupol.gtk
import gtk
import os
import sys
import pango
_ = gaupol.i18n._

__all__ = ("SpellCheckDialog",)


class SpellCheckDialog(gaupol.gtk.GladeDialog):

    """Dialog for checking spelling.

    Class variables:
     * _max_replacemnts: Maximum amount of replacements to save to file
     * _personal_dir: Directory for user dictionary and replacement files

    Instance variables:
     * _checker: Enchant spell-checker object
     * _doc: The document currectly being checked
     * _entry_handler: Handler for the replacement entry's 'changed' signal
     * _new_rows: List of rows in the current page with changed texts
     * _new_texts: List of changed texts in the current page
     * _page: The page currectly being checked
     * _pager: Iterator to iterate over all target pages
     * _replacements: List of misspelled words and their replacements
     * _row: The row in the current page being checked
    """

    __metaclass__ = gaupol.Contractual
    _max_replacemnts = 5000
    _personal_dir = os.path.join(gaupol.PROFILE_DIR, "spell-check")

    def __init___require(self, parent, application):
        assert gaupol.util.enchant_available()

    def __init__(self, parent, application):
        """Initialize a SpellCheckDialog object.

        Raise ValueError if dictionary initialization fails.
        """
        gaupol.gtk.GladeDialog.__init__(self, "spellcheck.glade")
        get_widget = self._glade_xml.get_widget
        self._add_button = get_widget("add_button")
        self._edit_button = get_widget("edit_button")
        self._entry = get_widget("entry")
        self._ignore_all_button = get_widget("ignore_all_button")
        self._ignore_button = get_widget("ignore_button")
        self._join_back_button = get_widget("join_back_button")
        self._join_forward_button = get_widget("join_forward_button")
        self._language_label = get_widget("language_label")
        self._replace_all_button = get_widget("replace_all_button")
        self._replace_button = get_widget("replace_button")
        self._table = get_widget("table")
        self._text_view = get_widget("text_view")
        self._tree_view = get_widget("tree_view")

        self._checker = None
        self._doc = None
        self._entry_handler = None
        self._new_rows = []
        self._new_texts = []
        self._page = None
        self._pager = None
        self._replacements = []
        self._row = None
        self.application = application
        self.conf = gaupol.gtk.conf.spell_check

        self._init_spell_check()
        self._init_fonts()
        self._init_tree_view()
        self._init_sensitivities()
        self._init_signal_handlers()
        self._init_sizes()
        self._dialog.set_transient_for(parent)
        self._dialog.set_default_response(gtk.RESPONSE_CLOSE)
        self._start()

    def _advance(self):
        """Advance to the next spelling error."""

        while True:
            try:
                # Advance to the next spelling error in the current text.
                return self._advance_current()
            except StopIteration:
                # Save the current text if changes were made.
                text = unicode(self._checker.get_text())
                subtitles = self._page.project.subtitles
                if text != subtitles[self._row].get_text(self._doc):
                    self._new_rows.append(self._row)
                    self._new_texts.append(text)
            # Move to the next row in the current page, move to the next page
            # in the sequence of target pages or end when all pages checked,
            try:
                self._advance_row()
            except StopIteration:
                try:
                    self._pager.next()
                except StopIteration:
                    break
        self._set_done()

    def _advance_current(self):
        """Advance to the next spelling error in the current text.

        Raise StopIteration when no more errors in the current text.
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
        mark = text_buffer.create_mark(None, end, True)
        self._text_view.scroll_to_mark(mark, 0.2)

        sensitive = text[max(0, a - 1):a].isspace()
        self._join_back_button.set_sensitive(sensitive)
        sensitive = text[z:min(len(text), z + 1)].isspace()
        self._join_forward_button.set_sensitive(sensitive)
        self._set_entry_text("")
        self._populate_tree_view(self._checker.suggest())
        self._tree_view.grab_focus()

    def _advance_row(self):
        """Advance to the next subtitle and set its text to the checker.

        Raise StopIteration when no more subtitles left in the current page.
        """
        subtitles = self._page.project.subtitles
        self._row += 1
        if self._row >= len(subtitles):
            raise StopIteration
        text = subtitles[self._row].get_text(self._doc)
        self._checker.set_text(unicode(text))

    def _get_next_page(self):
        """Return the next page to check the spelling in."""

        doc = gaupol.gtk.util.text_field_to_document(self.conf.field)
        for page in self.application.get_target_pages(self.conf.target):
            self.application.set_current_page(page)
            self._page = page
            self._doc = doc
            self._row = -1
            self._advance_row()
            yield page
            self._register_changes()

    def _init_checker(self):
        """Initialize the checker for conf.spell_check.language.

        Raise ValueError if dictionary initialization fails.
        """
        import enchant.checker
        language = self.conf.language
        path = os.path.join(self._personal_dir, "%s.dict" % language)
        try:
            try: dict = enchant.DictWithPWL(str(language), str(path))
            except IOError, (no, message):
                gaupol.util.print_write_io(sys.exc_info(), path)
                self._add_button.set_sensitive(False)
                dict = enchant.Dict(str(language))
        except enchant.Error, (message,):
            self._show_error_dialog(message)
            raise ValueError
        self._checker = enchant.checker.SpellChecker(dict, "")

    def _init_fonts(self):
        """Initialize widget fonts and text tags."""

        if gaupol.gtk.conf.editor.use_custom_font:
            font = gaupol.gtk.conf.editor.custom_font
            gaupol.gtk.util.set_widget_font(self._entry, font)
            gaupol.gtk.util.set_widget_font(self._text_view, font)
            gaupol.gtk.util.set_widget_font(self._tree_view, font)
        text_buffer = self._text_view.get_buffer()
        text_buffer.create_tag("misspelled", weight=pango.WEIGHT_BOLD)

    def _init_replacements(self):
        """Read misspelled words and their replacements from file."""

        basename = "%s.repl" % self.conf.language
        path = os.path.join(self._personal_dir, basename)
        if not os.path.isfile(path): return
        silent = gaupol.deco.silent(IOError, UnicodeError)
        lines = silent(gaupol.util.readlines)(path)
        if lines is None: return
        for line in gaupol.util.get_unique(lines):
            item = tuple(line.strip().split("|"))
            self._replacements.append(item)

    def _init_sensitivities(self):
        """Initialize widget sensitivities."""

        self._join_back_button.set_sensitive(False)
        self._join_forward_button.set_sensitive(False)
        self._replace_all_button.set_sensitive(False)
        self._replace_button.set_sensitive(False)

    def _init_signal_handlers(self):
        """Initialize signal handlers."""

        gaupol.util.connect(self, "_add_button", "clicked")
        gaupol.util.connect(self, "_edit_button", "clicked")
        gaupol.util.connect(self, "_ignore_all_button", "clicked")
        gaupol.util.connect(self, "_ignore_button", "clicked")
        gaupol.util.connect(self, "_join_back_button", "clicked")
        gaupol.util.connect(self, "_join_forward_button", "clicked")
        gaupol.util.connect(self, "_replace_all_button", "clicked")
        gaupol.util.connect(self, "_replace_button", "clicked")
        gaupol.util.connect(self, self, "response")
        callback = self._on_entry_changed
        self._entry_handler = self._entry.connect("changed", callback)

    def _init_sizes(self):
        """Initialize widget sizes."""

        label = gtk.Label("\n".join(["m" * 30] * 4))
        if gaupol.gtk.conf.editor.use_custom_font:
            font = gaupol.gtk.conf.editor.custom_font
            gaupol.gtk.util.set_label_font(label, font)
        width, height = label.size_request()
        self._text_view.set_size_request(width + 4, height + 7)

        label = gtk.Label("m" * 20)
        if gaupol.gtk.conf.editor.use_custom_font:
            font = gaupol.gtk.conf.editor.custom_font
            gaupol.gtk.util.set_label_font(label, font)
        width = label.size_request()[0]
        self._tree_view.set_size_request(width + 4, -1)

    def _init_spell_check(self):
        """Initialize spell-check components and related widgets.

        Raise ValueError if dictionary initialization fails.
        """
        gaupol.util.makedirs(self._personal_dir)
        self._init_checker()
        self._init_replacements()
        name = gaupol.locales.code_to_name(self.conf.language)
        self._language_label.set_markup("<b>%s</b>" % name)

    def _init_tree_view(self):
        """Initialize the suggestion tree view."""

        selection = self._tree_view.get_selection()
        selection.set_mode(gtk.SELECTION_SINGLE)
        selection.connect("changed", self._on_tree_view_selection_changed)
        store = gtk.ListStore(str)
        self._tree_view.set_model(store)
        column = gtk.TreeViewColumn("", gtk.CellRendererText(), text=0)
        self._tree_view.append_column(column)

    def _on_add_button_clicked(self, *args):
        """Add the current word to the user dictionary."""

        word = unicode(self._checker.word)
        self._checker.dict.add_to_pwl(word)
        self._advance()

    def _on_edit_button_clicked(self, *args):
        """Edit the current text in a separate dialog."""

        text = unicode(self._checker.get_text())
        dialog = gaupol.gtk.TextEditDialog(self._dialog, text)
        response = self.run_dialog(dialog)
        text = unicode(dialog.get_text())
        dialog.destroy()
        if response == gtk.RESPONSE_OK:
            self._checker.set_text(text)
            self._advance()

    def _on_entry_changed(self, entry):
        """Populate suggestions based on the word in the entry."""

        word = unicode(self._entry.get_text())
        suggestions = self._checker.suggest(word)
        self._populate_tree_view(suggestions, False)
        self._replace_button.set_sensitive(bool(word))
        self._replace_all_button.set_sensitive(bool(word))

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

    def _on_tree_view_selection_changed(self, *args):
        """Copy the selected suggestion into the entry."""

        selection = self._tree_view.get_selection()
        store, itr = selection.get_selected()
        if itr is None: return
        row = store.get_path(itr)[0]
        self._set_entry_text(unicode(store[row][0]))

    def _populate_tree_view(self, suggestions, select=True):
        """Populate the tree view with suggestions."""

        word = unicode(self._checker.word)
        iterator = reversed(self._replacements)
        formers = [x[1] for x in iterator if x[0] == word]
        get_unique = gaupol.util.get_unique
        suggestions = get_unique(formers + suggestions)
        store = self._tree_view.get_model()
        store.clear()
        for suggestion in suggestions:
            store.append((unicode(suggestion),))
        if (select and (len(store) > 0)):
            self._tree_view.set_cursor(0)
            self._tree_view.scroll_to_cell(0)

    def _register_changes(self):
        """Register made changes to the current page."""

        if not self._new_rows: return
        rows = self._new_rows
        doc = self._doc
        texts = self._new_texts
        self._page.project.replace_texts(rows, doc, texts)
        self._page.project.set_action_description(
            gaupol.registers.DO, _("Spell-checking"))
        self._new_rows = []
        self._new_texts = []

    def _set_done(self):
        """Finish spell-checking and set proper GUI properties."""

        self._text_view.get_buffer().set_text("")
        self._set_entry_text("")
        self._populate_tree_view([])
        self._table.set_sensitive(False)
        self._write_replacements()

    def _set_entry_text(self, word):
        """Set word to the entry with the 'changed' handler blocked."""

        self._entry.handler_block(self._entry_handler)
        self._entry.set_text(word)
        self._entry.handler_unblock(self._entry_handler)
        self._replace_button.set_sensitive(bool(word))
        self._replace_all_button.set_sensitive(bool(word))

    def _show_error_dialog(self, message):
        """Show an error dialog after failing to load dictionary."""

        name = gaupol.locales.code_to_name(self.conf.language)
        title = _('Failed to load dictionary for language "%s"') % name
        dialog = gaupol.gtk.ErrorDialog(self._dialog, title, message)
        dialog.add_button(gtk.STOCK_OK, gtk.RESPONSE_OK)
        self.flash_dialog(dialog)

    def _start(self):
        """Start checking the spelling of texts."""

        self._pager = self._get_next_page()
        self._pager.next()
        self._advance()

    def _store_replacement(self, misspelled, correct):
        """Store a misspelled word and its replacement."""

        self._replacements.append((misspelled, correct))
        get_unique = gaupol.util.get_unique
        self._replacements = get_unique(self._replacements, True)

    def _write_replacements(self):
        """Write misspelled words and their replacements to file."""

        if not self._replacements: return
        basename = "%s.repl" % self.conf.language
        path = os.path.join(self._personal_dir, basename)
        if len(self._replacements) > self._max_replacemnts:
            # Discard the oldest replacements.
            self._replacements[- self._max_replacemnts:]
        get_line = lambda x: "%s|%s%s" % (x[0], x[1], os.linesep)
        text = "".join([get_line(x) for x in self._replacements])
        try: gaupol.util.write(path, text)
        except (IOError, UnicodeError):
            gaupol.util.print_write_io(sys.exc_info(), path)
