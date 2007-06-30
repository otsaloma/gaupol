# Copyright (C) 2006-2007 Osmo Salomaa
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


"""Dialog for searching for and replacing text."""


import gaupol.gtk
import gtk
import re
_ = gaupol.i18n._

from .glade import GladeDialog


class SearchDialog(GladeDialog):

    """Dialog for searching for and replacing text.

    Instance variables:
     * _match_doc: DOCUMENT constant of the last match of pattern
     * _match_page: Page of the last match of pattern
     * _match_row: Row in page of the last match of pattern
     * _match_span: Start, end position of the last match of pattern
     * _was_next: True if the last search was 'next', False for 'previous'
    """

    __metaclass__ = gaupol.Contractual

    def __init__(self, application):

        GladeDialog.__init__(self, "search-dialog")
        get_widget = self._glade_xml.get_widget
        self._all_radio = get_widget("all_radio")
        self._current_radio = get_widget("current_radio")
        self._ignore_case_check = get_widget("ignore_case_check")
        self._main_check = get_widget("main_check")
        self._next_button = get_widget("next_button")
        self._pattern_combo = get_widget("pattern_combo")
        self._pattern_entry = self._pattern_combo.child
        self._previous_button = get_widget("previous_button")
        self._regex_check = get_widget("regex_check")
        self._replace_all_button = get_widget("replace_all_button")
        self._replace_button = get_widget("replace_button")
        self._replacement_combo = get_widget("replacement_combo")
        self._replacement_entry = self._replacement_combo.child
        self._search_vbox = get_widget("search_vbox")
        self._text_view = get_widget("text_view")
        self._tran_check = get_widget("tran_check")
        gaupol.gtk.util.prepare_text_view(self._text_view)

        self._match_doc = None
        self._match_page = None
        self._match_row = None
        self._match_span = None
        self._was_next = None
        self.application = application

        self._init_combo_box_entries()
        self._init_values()
        self._init_conf_handlers()
        self._init_dialog_handlers()
        self._init_search_handlers()
        self._init_target_handlers()
        self._init_sensitivities()
        self._init_sizes()
        self._dialog.set_transient_for(None)
        self._dialog.set_type_hint(gtk.gdk.WINDOW_TYPE_HINT_NORMAL)
        self._dialog.set_default_response(gtk.RESPONSE_CLOSE)

    @gaupol.gtk.util.asserted_return
    def _add_pattern_to_history(self):
        """Add the current pattern to the pattern combo box."""

        pattern = self._pattern_entry.get_text()
        store = self._pattern_combo.get_model()
        assert pattern != self.application.pattern
        self.application.pattern = pattern
        domain = gaupol.gtk.conf.search
        domain.patterns.insert(0, pattern)
        get_unique = gaupol.gtk.util.get_unique
        domain.patterns = get_unique(domain.patterns)
        while len(domain.patterns) > domain.max_history:
            domain.patterns.pop()
        store.clear()
        for pattern in domain.patterns:
            store.append([pattern])
        self.application.update_gui()

    @gaupol.gtk.util.asserted_return
    def _add_replacement_to_history(self):
        """Add the current replacement to the replacement combo box."""

        replacement = self._replacement_entry.get_text()
        store = self._replacement_combo.get_model()
        assert replacement != self.application.replacement
        self.application.replacement = replacement
        domain = gaupol.gtk.conf.search
        domain.replacements.insert(0, replacement)
        get_unique = gaupol.gtk.util.get_unique
        domain.replacements = get_unique(domain.replacements)
        while len(domain.replacements) > domain.max_history:
            domain.replacements.pop()
        store.clear()
        for replacement in domain.replacements:
            store.append([replacement])
        self.application.update_gui()

    def _admit_failure(self):
        """Set search and GUI properties to suit failure."""

        self._reset_properties()
        pattern = self._pattern_entry.get_text()
        message = _('"%s" not found') % pattern
        self.application.flash_message(message)

    def _admit_success(self, page, row, doc, match_span, next):
        """Set search and GUI properties to suit a match."""

        self._match_page = page
        self._match_row = row
        self._match_doc = doc
        self._match_span = list(match_span[:])
        self._was_next = next
        self.application.set_current_page(page)
        self._set_text(page, row, doc, match_span)
        col = gaupol.gtk.util.document_to_text_column(doc)
        page.view.set_focus(row, col)
        page.view.scroll_to_row(row)
        self._replace_button.set_sensitive(True)

    @gaupol.gtk.util.asserted_return
    def _get_cursor_offset(self, page, row, doc, next):
        """Return the cursor offset in the current text or None."""

        assert page is self._match_page
        assert row == self._match_row
        assert doc == self._match_doc
        return self._match_span[next]

    def _get_columns(self):
        """Get a list of columns to search in."""

        cols = []
        if self._main_check.get_active():
            cols.append(gaupol.gtk.COLUMN.MAIN_TEXT)
        if self._tran_check.get_active():
            cols.append(gaupol.gtk.COLUMN.TRAN_TEXT)
        return cols

    def _get_position(self, next):
        """Get the current position in the view.

        Raise Default if no pages open.
        Return row, document, position.
        """
        page = self.application.get_current_page()
        gaupol.gtk.util.raise_default(page is None)
        rows = page.view.get_selected_rows()
        row = (rows[0] if rows else None)
        if row is None:
            row = (len(page.project.subtitles) - 1, 0)[next]
        col = page.view.get_focus()[1]
        doc = None
        translate = gaupol.gtk.util.text_column_to_document
        if gaupol.gtk.util.is_text_column(col):
            doc = translate(col)
        cols = gaupol.gtk.conf.search.columns
        docs = [translate(x) for x in cols]
        if (doc is None) or (doc not in docs):
            doc = (docs[-1], docs[0])[next]
        pos = self._get_cursor_offset(page, row, doc, next)
        return row, doc, pos

    def _get_target(self):
        """Get the TARGET constant to search in."""

        if self._current_radio.get_active():
            return gaupol.gtk.TARGET.CURRENT
        if self._all_radio.get_active():
            return gaupol.gtk.TARGET.ALL
        raise ValueError

    def _init_combo_box_entries(self):
        """Initialize the history lists in the combo box entries."""

        store = self._pattern_combo.get_model()
        for pattern in gaupol.gtk.conf.search.patterns:
            store.append([pattern])
        store = self._replacement_combo.get_model()
        for replacement in gaupol.gtk.conf.search.replacements:
            store.append([replacement])

    def _init_conf_handlers(self):
        """Initialize configuration signal handlers."""

        callback = lambda *args: self._update_search_targets()
        self.application.connect("page-added", callback)
        gaupol.gtk.conf.search.connect("notify::columns", callback)
        gaupol.gtk.conf.search.connect("notify::target", callback)
        self._update_search_targets()

    def _init_dialog_handlers(self):
        """Initialize dialog signal handlers."""

        gaupol.gtk.util.connect(self, self, "response")
        gaupol.gtk.util.connect(self, self, "show")

    def _init_search_handlers(self):
        """Initialize search signal handlers."""

        gaupol.gtk.util.connect(self, "_next_button", "clicked")
        gaupol.gtk.util.connect(self, "_pattern_entry", "changed")
        gaupol.gtk.util.connect(self, "_previous_button", "clicked")
        gaupol.gtk.util.connect(self, "_regex_check", "toggled")
        gaupol.gtk.util.connect(self, "_replace_all_button", "clicked")
        gaupol.gtk.util.connect(self, "_replace_button", "clicked")
        gaupol.gtk.util.connect(self, "_text_view", "focus-out-event")
        gaupol.gtk.util.connect(self, "_ignore_case_check", "toggled")

        text_buffer = self._text_view.get_buffer()
        callback = lambda *args: self._replace_button.set_sensitive(False)
        text_buffer.connect("changed", callback)

    def _init_sensitivities(self):
        """Initialize widget sensitivities."""

        self._text_view.set_sensitive(False)
        self._next_button.set_sensitive(False)
        self._previous_button.set_sensitive(False)
        self._replace_button.set_sensitive(False)
        self._replace_all_button.set_sensitive(False)
        self._pattern_entry.emit("changed")
        self._replacement_entry.emit("changed")
        self._regex_check.emit("toggled")

    def _init_sizes(self):
        """Initialize widget sizes."""

        label = gtk.Label("\n".join(["M" * 34] * 4))
        if gaupol.gtk.conf.editor.use_custom_font:
            font = gaupol.gtk.conf.editor.custom_font
            gaupol.gtk.util.set_label_font(label, font)
        width, height = label.size_request()
        self._text_view.set_size_request(width + 4, height + 7)

    def _init_target_handlers(self):
        """Initialize target signal handlers."""

        def save_columns(*args):
            gaupol.gtk.conf.search.columns = self._get_columns()
            self._search_vbox.set_sensitive(bool(self._get_columns()))
        self._main_check.connect("toggled", save_columns)
        self._tran_check.connect("toggled", save_columns)
        def save_target(*args):
            gaupol.gtk.conf.search.target = self._get_target()
        self._current_radio.connect("toggled", save_target)
        self._all_radio.connect("toggled", save_target)

    def _init_values(self):
        """Initialize default values for widgets."""

        self._pattern_entry.set_text(self.application.pattern)
        self._replacement_entry.set_text(self.application.replacement)
        self._regex_check.set_active(gaupol.gtk.conf.search.regex)
        self._ignore_case_check.set_active(gaupol.gtk.conf.search.ignore_case)
        cols = gaupol.gtk.conf.search.columns
        self._main_check.set_active(gaupol.gtk.COLUMN.MAIN_TEXT in cols)
        self._tran_check.set_active(gaupol.gtk.COLUMN.TRAN_TEXT in cols)
        target = gaupol.gtk.conf.search.target
        self._all_radio.set_active(target == gaupol.gtk.TARGET.ALL)
        self._current_radio.set_active(target == gaupol.gtk.TARGET.CURRENT)

    def _on_ignore_case_check_toggled(self, check_button):
        """Save the ignore case setting."""

        gaupol.gtk.conf.search.ignore_case = check_button.get_active()

    def _on_next_button_clicked(self, *args):
        """Find the next match of pattern."""

        # Make sure the text view experiences a focus-out-event.
        self._next_button.grab_focus()
        self.next()

    def _on_pattern_entry_changed(self, entry):
        """Update action sensitivities."""

        sensitive = bool(entry.get_text())
        self._next_button.set_sensitive(sensitive)
        self._previous_button.set_sensitive(sensitive)
        self._replace_all_button.set_sensitive(sensitive)

    def _on_previous_button_clicked(self, *args):
        """Find the previous match of pattern."""

        # Make sure the text view experiences a focus-out-event.
        self._previous_button.grab_focus()
        self.previous()

    def _on_regex_check_toggled(self, check_button):
        """Save regular expression setting and update sensitivities."""

        active = check_button.get_active()
        gaupol.gtk.conf.search.regex = active
        self.set_response_sensitive(gtk.RESPONSE_HELP, active)

    def _on_replace_all_button_clicked(self, *args):
        """Replace all matches of pattern."""

        # Make sure the text view experiences a focus-out-event.
        self._replace_all_button.grab_focus()
        gaupol.gtk.util.set_cursor_busy(self._dialog)
        self.replace_all()
        gaupol.gtk.util.set_cursor_normal(self._dialog)

    def _on_replace_button_clicked(self, *args):
        """Replace the current match of pattern."""

        # Ensure that the text view experiences a focus-out-event.
        self._replace_button.grab_focus()
        self.replace()

    @gaupol.gtk.util.asserted_return
    def _on_response(self, dialog, response):
        """Do not send response if browsing help."""

        assert response == gtk.RESPONSE_HELP
        gaupol.gtk.util.browse_url(gaupol.REGEX_HELP_URL)
        self.stop_emission("response")

    def _on_show(self, *args):
        """Move focus to the pattern entry and select the pattern."""

        self._pattern_entry.select_region(0, -1)
        self._pattern_entry.grab_focus()

    @gaupol.gtk.util.asserted_return
    def _on_text_view_focus_out_event(self, text_view, event):
        """Save changes made in the text view."""

        assert self._match_page is not None
        assert self._match_row is not None
        assert self._match_doc is not None
        assert self._text_view.props.sensitive
        page = self.application.get_current_page()
        assert page is self._match_page
        text_buffer = text_view.get_buffer()
        bounds = text_buffer.get_bounds()
        text = text_buffer.get_text(*bounds)
        page.project.set_text(self._match_row, self._match_doc, text)

    def _reset_properties(self):
        """Reset search and GUI properties to defaults."""

        self._match_page = None
        self._match_doc = None
        self._match_row = None
        self._match_span = None
        self._text_view.get_buffer().set_text("")
        self._text_view.set_sensitive(False)

    def _set_pattern(self, page):
        """Set the search pattern for page.

        Raise Default if pattern is empty or bad.
        """
        pattern = self._pattern_entry.get_text()
        gaupol.gtk.util.raise_default(not pattern)
        ignore_case = self._ignore_case_check.get_active()
        if not gaupol.gtk.conf.search.regex:
            self._add_pattern_to_history()
            return page.project.set_search_string(pattern, ignore_case)
        flags = (re.IGNORECASE if ignore_case else 0)
        try:
            page.project.set_search_regex(pattern, flags)
        except re.error, message:
            self._show_regex_error_dialog_pattern(message)
            raise gaupol.gtk.Default
        self._add_pattern_to_history()

    def _set_replacement(self, page):
        """Set the search replacement for page."""

        replacement = self._replacement_entry.get_text()
        page.project.set_search_replacement(replacement)
        self._add_replacement_to_history()

    def _set_text(self, page, row, doc, match_span):
        """Set subtitle text to text view."""

        text_buffer = self._text_view.get_buffer()
        subtitle = page.project.subtitles[row]
        text = subtitle.get_text(doc)
        text_buffer.set_text(text)
        ins = text_buffer.get_iter_at_offset(match_span[0])
        bound = text_buffer.get_iter_at_offset(match_span[1])
        text_buffer.select_range(ins, bound)
        mark = text_buffer.create_mark(None, bound, True)
        self._text_view.scroll_to_mark(mark, 0.2)
        self._text_view.set_sensitive(True)
        self._text_view.grab_focus()

    def _show_regex_error_dialog_pattern(self, message):
        """Show an error dialog if pattern failed to compile."""

        title = _('Error in regular expression pattern')
        message = _("%s.") % message
        dialog = gaupol.gtk.ErrorDialog(self._dialog, title, message)
        dialog.add_button(gtk.STOCK_OK, gtk.RESPONSE_OK)
        self.flash_dialog(dialog)

    def _show_regex_error_dialog_replacement(self, message):
        """Show an error dialog if replacement is invalid."""

        title = _('Error in regular expression replacement')
        message = _("%s.") % message
        dialog = gaupol.gtk.ErrorDialog(self._dialog, title, message)
        dialog.add_button(gtk.STOCK_OK, gtk.RESPONSE_OK)
        self.flash_dialog(dialog)

    def _update_search_targets(self):
        """Update the search targets in all application's pages."""

        for page in self.application.pages:
            translate = gaupol.gtk.util.text_column_to_document
            docs = [translate(x) for x in gaupol.gtk.conf.search.columns]
            wrap = (gaupol.gtk.conf.search.target != gaupol.gtk.TARGET.ALL)
            page.project.set_search_target(None, docs, wrap)

    def next_require(self):
        assert self._pattern_entry.get_text()

    @gaupol.gtk.util.silent(gaupol.gtk.Default)
    def next(self):
        """Find the next match of pattern."""

        page = self.application.get_current_page()
        row, doc, pos = self._get_position(True)
        pages = self.application.pages[:]
        i = pages.index(page)
        # Loop twice over the current page,
        # since starting in the middle.
        for page in (pages[i:] + pages[:i + 1]):
            self._set_pattern(page)
            try:
                # Return match in page after position.
                row, doc, span = page.project.find_next(row, doc, pos)
                return self._admit_success(page, row, doc, span, True)
            except StopIteration:
                target = gaupol.gtk.conf.search.target
                if target == gaupol.gtk.TARGET.CURRENT:
                    # Fail wrapped single-page search.
                    return self._admit_failure()
                # Proceed to the next page.
                row = doc = pos = None
        # Fail wrapped search of all pages.
        self._admit_failure()

    def previous_require(self):
        assert self._pattern_entry.get_text()

    @gaupol.gtk.util.silent(gaupol.gtk.Default)
    def previous(self):
        """Find the previous match of pattern."""

        page = self.application.get_current_page()
        row, doc, pos = self._get_position(False)
        pages = self.application.pages[::-1]
        i = pages.index(page)
        # Loop twice over the current page,
        # since starting in the middle.
        for page in (pages[i:] + pages[:i + 1]):
            self._set_pattern(page)
            try:
                # Return match in page before position.
                row, doc, span = page.project.find_previous(row, doc, pos)
                return self._admit_success(page, row, doc, span, False)
            except StopIteration:
                target = gaupol.gtk.conf.search.target
                if target == gaupol.gtk.TARGET.CURRENT:
                    # Fail wrapped single-page search.
                    return self._admit_failure()
                # Proceed to the previous page.
                row = doc = pos = None
        # Fail wrapped search of all pages.
        self._admit_failure()

    def replace_require(self):
        assert self._match_doc is not None
        assert self._match_page is not None
        assert self._match_row is not None
        assert self._match_span is not None
        assert self._was_next is not None

    @gaupol.gtk.util.silent(gaupol.gtk.Default)
    @gaupol.gtk.util.asserted_return
    def replace(self):
        """Replace the current match of pattern."""

        page = self.application.get_current_page()
        assert page is self._match_page
        self._set_replacement(page)
        subtitle = page.project.subtitles[self._match_row]
        length = len(subtitle.get_text(self._match_doc))
        try:
            page.project.replace()
        except re.error, message:
            return self._show_regex_error_dialog_replacement(message)
        shift = (len(subtitle.get_text(self._match_doc)) - length)
        self._match_span[1] += shift
        (self.previous, self.next)[self._was_next]()

    def replace_all_require(self):
        assert self._pattern_entry.get_text()

    @gaupol.gtk.util.silent(gaupol.gtk.Default)
    def replace_all(self):
        """Replace all matches of pattern."""

        count = 0
        target = gaupol.gtk.conf.search.target
        for page in self.application.get_target_pages(target):
            self._set_pattern(page)
            self._set_replacement(page)
            try:
                count += page.project.replace_all()
            except re.error, message:
                self._show_regex_error_dialog_replacement(message)
                break
        self._reset_properties()
        message = _("Found and replaced %d occurences")
        self.application.flash_message(message % count)
