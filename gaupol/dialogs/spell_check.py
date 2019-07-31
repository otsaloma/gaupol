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

from aeidon.i18n   import _
from gi.repository import Gtk
from gi.repository import Pango

__all__ = ("SpellCheckDialog",)


class SpellCheckDialog(gaupol.BuilderDialog):

    """
    Dialog for checking and correcting spelling.

    :ivar _doc: :attr:`aeidon.documents` item currectly being checked
    :ivar _entry_handler: Handler for replacement entry's "changed" signal
    :ivar _language: Language code for :attr:`_navigator`
    :ivar _navigator: :class:`aeidon.SpellCheckNavigator` instance used
    :ivar _new_rows: List of rows in the current page with changed texts
    :ivar _new_texts: List of changed texts in the current page
    :ivar _page: :class:`gaupol.Page` instance currectly being checked
    :ivar _pager: Iterator to iterate over all target pages
    :ivar _row: Row currently being checked
    :ivar _rower: Iterator to iterate over all rows
    """

    _widgets = [
        "add_button",
        "edit_button",
        "entry",
        "grid",
        "ignore_all_button",
        "ignore_button",
        "join_back_button",
        "join_forward_button",
        "replace_all_button",
        "replace_button",
        "text_view",
        "tree_view",
    ]

    def __init__(self, parent, application):
        """Initialize a :class:`SpellCheckDialog` instance."""
        gaupol.BuilderDialog.__init__(self, "spell-check-dialog.ui")
        self.application = application
        self._doc = None
        self._entry_handler = None
        self._language = gaupol.conf.spell_check.language
        self._language_name = aeidon.locales.code_to_name(self._language)
        self._navigator = aeidon.SpellCheckNavigator(self._language)
        self._new_rows = []
        self._new_texts = []
        self._page = None
        self._pager = None
        self._row = None
        self._rower = None
        self._init_dialog(parent)
        self._init_widgets()
        self._init_sensitivities()
        self.resize(*gaupol.conf.spell_check.size)
        self._pager = self._yield_pages()
        next(self._pager)
        self._proceed()

    def _append_changes(self):
        """Append current changes to the list of changes."""
        subtitle = self._page.project.subtitles[self._row]
        if self._navigator.text == subtitle.get_text(self._doc): return
        self._new_rows.append(self._row)
        self._new_texts.append(self._navigator.text)

    def _init_dialog(self, parent):
        """Initialize the dialog."""
        self.set_default_response(Gtk.ResponseType.CLOSE)
        self.set_transient_for(parent)
        self.set_modal(True)

    def _init_sensitivities(self):
        """Initialize widget sensitivities."""
        self._join_back_button.set_sensitive(False)
        self._join_forward_button.set_sensitive(False)
        self._replace_all_button.set_sensitive(False)
        self._replace_button.set_sensitive(False)

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
        gaupol.style.use_font(self._entry, "custom")
        gaupol.style.use_font(self._text_view, "custom")
        gaupol.style.use_font(self._tree_view, "custom")
        with aeidon.util.silent(AttributeError):
            # Top and bottom margins available since GTK 3.18.
            self._text_view.set_top_margin(6)
            self._text_view.set_bottom_margin(6)
        text_buffer = self._text_view.get_buffer()
        text_buffer.create_tag("misspelled", weight=Pango.Weight.BOLD)
        scale = gaupol.util.scale_to_size
        scale(self._text_view, nchar=55, nlines=4, font="custom")
        scale(self._tree_view, nchar=20, nlines=6, font="custom")
        self._entry_handler = self._entry.connect("changed", self._on_entry_changed)

    def _on_add_button_clicked(self, *args):
        """Add the current word to personal word list."""
        self._navigator.add()
        self._proceed()

    def _on_edit_button_clicked(self, *args):
        """Edit the current text in a separate dialog."""
        text = self._navigator.text
        dialog = gaupol.TextEditDialog(self._dialog, text)
        response = gaupol.util.run_dialog(dialog)
        text = dialog.get_text()
        dialog.destroy()
        if response != Gtk.ResponseType.OK: return
        self._navigator.reset(text)
        self._proceed()

    def _on_entry_changed(self, entry):
        """Populate suggestions based on text in `entry`."""
        word = entry.get_text()
        suggestions = self._navigator.checker.suggest(word) if word else []
        self._populate_tree_view(suggestions, select=False)
        self._replace_button.set_sensitive(bool(word))
        self._replace_all_button.set_sensitive(bool(word))

    def _on_ignore_all_button_clicked(self, *args):
        """Ignore the current word and any subsequent instances."""
        self._navigator.ignore_all()
        self._proceed()

    def _on_ignore_button_clicked(self, *args):
        """Ignore the current word."""
        self._navigator.ignore()
        self._proceed()

    def _on_join_back_button_clicked(self, *args):
        """Join the current word with the previous."""
        self._navigator.join_with_previous()
        self._proceed()

    def _on_join_forward_button_clicked(self, *args):
        """Join the current word with the next."""
        self._navigator.join_with_next()
        self._proceed()

    def _on_replace_all_button_clicked(self, *args):
        """Replace the current word and subsequent instances with `replacement`."""
        self._navigator.replace_all(self._entry.get_text())
        self._proceed()

    def _on_replace_button_clicked(self, *args):
        """Replace the current word with `replacement`."""
        self._navigator.replace(self._entry.get_text())
        self._proceed()

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
        store = self._tree_view.get_model()
        self._tree_view.set_model(None)
        store.clear()
        for suggestion in suggestions:
            store.append((suggestion,))
        self._tree_view.set_model(store)
        if select and len(store) > 0:
            self._tree_view.set_cursor(0)
            self._tree_view.scroll_to_cell(0)

    def _proceed(self):
        """Move on to the next spelling error."""
        try:
            # Move on to the next spelling error in the current text.
            return self._proceed_current()
        except StopIteration:
            # Commit changes to the current text.
            self._append_changes()
        try:
            # Move on to the next row.
            next(self._rower)
            return self._proceed()
        except StopIteration:
            # Commit changes to the current page.
            self._register_changes()
        try:
            # Move on to the next page.
            next(self._pager)
            return self._proceed()
        except StopIteration:
            self._set_done()

    def _proceed_current(self):
        """Move on to the next spelling error in the current text."""
        next(self._navigator)
        col = self._page.document_to_text_column(self._doc)
        self._page.view.set_focus(self._row, col)
        self._page.view.scroll_to_row(self._row)
        text_buffer = self._text_view.get_buffer()
        text_buffer.set_text(self._navigator.text)
        start = text_buffer.get_iter_at_offset(self._navigator.pos)
        end = text_buffer.get_iter_at_offset(self._navigator.endpos)
        text_buffer.apply_tag_by_name("misspelled", start, end)
        mark = text_buffer.create_mark(None, end, True)
        self._text_view.scroll_to_mark(mark=mark,
                                       within_margin=0,
                                       use_align=False,
                                       xalign=0.5,
                                       yalign=0.5)

        leading = self._navigator.leading_context(1)
        trailing = self._navigator.trailing_context(1)
        self._join_back_button.set_sensitive(leading.isspace())
        self._join_forward_button.set_sensitive(trailing.isspace())
        self._set_entry_text("")
        self._populate_tree_view(self._navigator.suggest())
        self._tree_view.grab_focus()

    def _register_changes(self):
        """Register changes to the current page."""
        if not self._new_rows: return
        self._page.project.replace_texts(
            self._new_rows, self._doc, self._new_texts)
        self._page.project.set_action_description(
            aeidon.registers.DO, _("Spell-checking"))
        self._new_rows = []
        self._new_texts = []

    def _save_geometry(self):
        """Save dialog size."""
        if self.is_maximized(): return
        gaupol.conf.spell_check.size = list(self.get_size())

    def _set_done(self):
        """Set state of widgets for finished spell-check."""
        self._text_view.get_buffer().set_text("")
        self._set_entry_text("")
        self._populate_tree_view([])
        self._grid.set_sensitive(False)
        self._navigator.checker.write_replacements()

    def _set_entry_text(self, word):
        """Set `word` to the entry with its "changed" handler blocked."""
        self._entry.handler_block(self._entry_handler)
        self._entry.set_text(word)
        self._entry.handler_unblock(self._entry_handler)
        self._replace_button.set_sensitive(bool(word))
        self._replace_all_button.set_sensitive(bool(word))

    def _yield_pages(self):
        """Yield pages to check spelling in."""
        field = gaupol.conf.spell_check.field
        doc = gaupol.util.text_field_to_document(field)
        target = gaupol.conf.spell_check.target
        for page in self.application.get_target_pages(target):
            if not page.project.subtitles: continue
            self.application.set_current_page(page)
            self._page = page
            self._doc = doc
            self._rower = self._yield_rows(page)
            next(self._rower)
            yield page

    def _yield_rows(self, page):
        """Yield rows to check spelling in."""
        for row, subtitle in enumerate(page.project.subtitles):
            self._row = row
            text = subtitle.get_text(self._doc)
            self._navigator.reset(text)
            yield row
