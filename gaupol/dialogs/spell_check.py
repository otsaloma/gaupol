# -*- coding: utf-8 -*-

# Copyright (C) 2005 Osmo Salomaa
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""Dialog for checking and correcting spelling."""

import aeidon
import gaupol
import os

from aeidon.i18n   import _
from gi.repository import Gtk
from gi.repository import Pango

try:
    import enchant.checker
except Exception:
    pass

__all__ = ("SpellCheckDialog",)


class SpellCheckDialog(gaupol.BuilderDialog):

    """
    Dialog for checking and correcting spelling.

    :cvar _max_replacements: Maximum amount of replacements to save to file
    :cvar _personal_dir: Directory for user replacement files
    :ivar _checker: :class:`enchant.Checker` instance used
    :ivar _doc: :attr:`aeidon.documents` item currectly being checked
    :ivar _entry_handler: Handler for replacement entry's "changed" signal
    :ivar _language: Language code for :attr:`_checker`
    :ivar _new_rows: List of rows in the current page with changed texts
    :ivar _new_texts: List of changed texts in the current page
    :ivar _page: :class:`gaupol.Page` instance currectly being checked
    :ivar _pager: Iterator to iterate over all target pages
    :ivar _replacements: List of misspelled words and their replacements
    :ivar _row: Row currently being checked
    """
    _max_replacements = 10000
    _personal_dir = os.path.join(aeidon.CONFIG_HOME_DIR, "spell-check")

    _widgets = (
        "add_button",
        "edit_button",
        "entry",
        "ignore_all_button",
        "ignore_button",
        "join_back_button",
        "join_forward_button",
        "replace_all_button",
        "replace_button",
        "grid",
        "text_view",
        "tree_view",
    )

    def __init__(self, parent, application):
        """
        Initialize a :class:`SpellCheckDialog` instance.

        Raise :exc:`ValueError` if dictionary initialization fails.
        """
        gaupol.BuilderDialog.__init__(self, "spell-check-dialog.ui")
        self.application = application
        self._checker = None
        self._doc = None
        self._entry_handler = None
        self._language = gaupol.conf.spell_check.language
        self._language_name = aeidon.locales.code_to_name(self._language)
        self._new_rows = []
        self._new_texts = []
        self._page = None
        self._pager = None
        self._replacements = []
        self._row = None
        self._init_spell_check()
        self._init_widgets()
        self._init_sensitivities()
        self.resize(*gaupol.conf.spell_check.size)
        self._dialog.set_transient_for(parent)
        self._dialog.set_default_response(Gtk.ResponseType.CLOSE)
        self._start()

    def _advance(self):
        """Advance to the next spelling error."""
        while True:
            try:
                # Advance to the next spelling error in the current text.
                return self._advance_current()
            except StopIteration:
                # Save the current text if changes were made.
                text = self._checker.get_text()
                subtitle = self._page.project.subtitles[self._row]
                if text != subtitle.get_text(self._doc):
                    self._new_rows.append(self._row)
                    self._new_texts.append(text)
            # Move to the next row in the current page, move to the next page
            # in the sequence of target pages or end when all pages checked.
            try:
                self._advance_row()
            except StopIteration:
                try:
                    next(self._pager)
                except StopIteration:
                    break
        self._set_done()

    def _advance_current(self):
        """
        Advance to the next spelling error in the current text.

        Raise :exc:`StopIteration` when no more errors in the current text.
        """
        next(self._checker)
        col = self._page.document_to_text_column(self._doc)
        self._page.view.set_focus(self._row, col)
        self._page.view.scroll_to_row(self._row)
        text = self._checker.get_text()
        text_buffer = self._text_view.get_buffer()
        text_buffer.set_text(text)
        a = self._checker.wordpos
        z = a + len(self._checker.word)
        start = text_buffer.get_iter_at_offset(a)
        end = text_buffer.get_iter_at_offset(z)
        text_buffer.apply_tag_by_name("misspelled", start, end)
        mark = text_buffer.create_mark(None, end, True)
        self._text_view.scroll_to_mark(mark=mark,
                                       within_margin=0,
                                       use_align=False,
                                       xalign=0.5,
                                       yalign=0.5)

        leading = self._checker.leading_context(1)
        trailing = self._checker.trailing_context(1)
        self._join_back_button.set_sensitive(leading.isspace())
        self._join_forward_button.set_sensitive(trailing.isspace())
        self._set_entry_text("")
        self._populate_tree_view(self._checker.suggest())
        self._tree_view.grab_focus()

    def _advance_row(self):
        """
        Advance to the next subtitle and feed its text to the spell-checker.

        Raise :exc:`StopIteration` when no more subtitles in the current page.
        """
        self._row += 1
        if self._row >= len(self._page.project.subtitles):
            raise StopIteration
        subtitle = self._page.project.subtitles[self._row]
        text = subtitle.get_text(self._doc)
        self._checker.set_text(text)

    def _get_next_page(self):
        """Return the next page to check spelling in."""
        field = gaupol.conf.spell_check.field
        doc = gaupol.util.text_field_to_document(field)
        target = gaupol.conf.spell_check.target
        for page in self.application.get_target_pages(target):
            self.application.set_current_page(page)
            self._page = page
            self._doc = doc
            self._row = -1
            self._advance_row()
            yield page
            self._register_changes()

    def _init_checker(self):
        """
        Initialize spell-checker and its dictionary.

        Raise :exc:`ValueError` if dictionary initialization fails.
        """
        try:
            dictionary = enchant.Dict(self._language)
            # Sometimes enchant will initialize a dictionary that will not
            # actually work when trying to use it, hence check something.
            dictionary.check("gaupol")
        except enchant.Error as error:
            self._show_error_dialog(str(error))
            raise ValueError("Dictionary initialization failed for language {}"
                             .format(repr(self._language)))

        self._checker = enchant.checker.SpellChecker(dictionary, "")

    def _init_replacements(self):
        """Read misspelled words and their replacements from file."""
        basename = "{}.repl".format(gaupol.conf.spell_check.language)
        path = os.path.join(self._personal_dir, basename)
        if not os.path.isfile(path): return
        with aeidon.util.silent(IOError, OSError):
            lines = aeidon.util.readlines(path)
            for line in aeidon.util.get_unique(lines):
                misspelled, correct  = line.strip().split("|", 1)
                self._replacements.append((misspelled, correct))

    def _init_sensitivities(self):
        """Initialize widget sensitivities."""
        self._join_back_button.set_sensitive(False)
        self._join_forward_button.set_sensitive(False)
        self._replace_all_button.set_sensitive(False)
        self._replace_button.set_sensitive(False)

    def _init_spell_check(self):
        """
        Initialize spell-check components and related widgets.

        Raise :exc:`ValueError` if dictionary initialization fails.
        """
        aeidon.util.makedirs(self._personal_dir)
        self._init_checker()
        self._init_replacements()

    def _init_tree_view(self):
        """Initialize the suggestion tree view."""
        selection = self._tree_view.get_selection()
        selection.set_mode(Gtk.SelectionMode.SINGLE)
        selection.connect("changed", self._on_tree_view_selection_changed)
        store = Gtk.ListStore(str)
        self._tree_view.set_model(store)
        column = Gtk.TreeViewColumn("", Gtk.CellRendererText(), text=0)
        self._tree_view.append_column(column)

    def _init_widgets(self):
        """Initialize widget properties."""
        self._init_tree_view()
        font = gaupol.util.get_font()
        gaupol.util.set_widget_font(self._entry, font)
        gaupol.util.set_widget_font(self._text_view, font)
        gaupol.util.set_widget_font(self._tree_view, font)
        text_buffer = self._text_view.get_buffer()
        text_buffer.create_tag("misspelled", weight=Pango.Weight.BOLD)
        gaupol.util.scale_to_size(self._text_view, nchar=50, nlines=4, font=font)
        gaupol.util.scale_to_size(self._tree_view, nchar=20, nlines=6, font=font)
        self._entry_handler = self._entry.connect("changed",
                                                  self._on_entry_changed)

    def _on_add_button_clicked(self, *args):
        """Add the current word to the user dictionary."""
        self._checker.dict.add(self._checker.word)
        self._advance()

    def _on_edit_button_clicked(self, *args):
        """Edit the current text in a separate dialog."""
        text = self._checker.get_text()
        dialog = gaupol.TextEditDialog(self._dialog, text)
        response = gaupol.util.run_dialog(dialog)
        text = dialog.get_text()
        dialog.destroy()
        if response != Gtk.ResponseType.OK: return
        self._checker.set_text(text)
        self._advance()

    def _on_entry_changed(self, entry):
        """Populate suggestions based on text in `entry`."""
        word = entry.get_text()
        suggestions = (self._checker.suggest(word) if word else [])
        self._populate_tree_view(suggestions, select=False)
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
        text = self._checker.get_text()
        a = self._checker.wordpos
        text = text[:a-1] + text[a:]
        self._checker.set_text(text)
        self._advance()

    def _on_join_forward_button_clicked(self, *args):
        """Join the current word with the following word."""
        text = self._checker.get_text()
        z = self._checker.wordpos + len(self._checker.word)
        text = text[:z] + text [z+1:]
        self._checker.set_text(text)
        self._advance()

    def _on_replace_all_button_clicked(self, *args):
        """Replace all instances of the current word."""
        misspelled = self._checker.word
        correct = self._entry.get_text()
        self._replacements.append((misspelled, correct))
        self._checker.replace_always(correct)
        self._advance()

    def _on_replace_button_clicked(self, *args):
        """Replace the current word."""
        misspelled = self._checker.word
        correct = self._entry.get_text()
        self._replacements.append((misspelled, correct))
        self._checker.replace(correct)
        self._advance()

    def _on_response(self, dialog, response):
        """Apply changes to the current page."""
        self._register_changes()
        self._save_geometry()
        self._set_done()

    def _on_tree_view_selection_changed(self, *args):
        """Copy the selected suggestion into the entry."""
        selection = self._tree_view.get_selection()
        store, itr = selection.get_selected()
        if itr is None: return
        path = store.get_path(itr)
        row = gaupol.util.tree_path_to_row(path)
        self._set_entry_text(store[row][0])

    def _populate_tree_view(self, suggestions, select=True):
        """Populate the tree view with `suggestions`."""
        word = self._checker.word
        repl = reversed(self._replacements)
        replacements = [x[1] for x in repl if x[0] == word]
        suggestions = list(replacements) + list(suggestions)
        suggestions = aeidon.util.get_unique(suggestions)
        store = self._tree_view.get_model()
        self._tree_view.set_model(None)
        store.clear()
        for suggestion in suggestions:
            store.append((suggestion,))
        self._tree_view.set_model(store)
        if select and len(store) > 0:
            self._tree_view.set_cursor(0)
            self._tree_view.scroll_to_cell(0)

    def _register_changes(self):
        """Register changes to the current page."""
        if not self._new_rows: return
        self._page.project.replace_texts(self._new_rows,
                                         self._doc,
                                         self._new_texts)

        self._page.project.set_action_description(
            aeidon.registers.DO, _("Spell-checking"))
        self._new_rows = []
        self._new_texts = []

    def _save_geometry(self):
        """Save dialog size."""
        with aeidon.util.silent(AttributeError):
            # is_maximized was added in GTK+ 3.12.
            if self.is_maximized(): return
        gaupol.conf.spell_check.size = list(self.get_size())

    def _set_done(self):
        """Set state of widgets for finished spell-check."""
        self._text_view.get_buffer().set_text("")
        self._set_entry_text("")
        self._populate_tree_view(())
        self._grid.set_sensitive(False)
        self._write_replacements()

    def _set_entry_text(self, word):
        """Set `word` to the entry with its "changed" handler blocked."""
        self._entry.handler_block(self._entry_handler)
        self._entry.set_text(word)
        self._entry.handler_unblock(self._entry_handler)
        self._replace_button.set_sensitive(bool(word))
        self._replace_all_button.set_sensitive(bool(word))

    def _show_error_dialog(self, message):
        """Show an error dialog after failing to load dictionary."""
        title = _('Failed to load dictionary for language "{}"')
        title = title.format(self._language_name)
        dialog = gaupol.ErrorDialog(self._dialog, title, message)
        dialog.add_button(_("_OK"), Gtk.ResponseType.OK)
        dialog.set_default_response(Gtk.ResponseType.OK)
        gaupol.util.flash_dialog(dialog)

    def _start(self):
        """Start checking the spelling."""
        self._pager = self._get_next_page()
        next(self._pager)
        self._advance()

    def _write_replacements(self):
        """Write misspelled words and their replacements to file."""
        if not self._replacements: return
        self._replacements = aeidon.util.get_unique(self._replacements,
                                                    keep_last=True)

        basename = "{}.repl".format(self._language)
        path = os.path.join(self._personal_dir, basename)
        if len(self._replacements) > self._max_replacements:
            # Discard the oldest of replacements.
            self._replacements[-self._max_replacements:]
        text = "\n".join("|".join(x) for x in self._replacements) + "\n"
        with aeidon.util.silent(IOError, OSError):
            aeidon.util.write(path, text)
