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


import re
from gettext import gettext as _

import gobject
import gtk

from gaupol import urls
from gaupol.gtk import conf, cons, util
from gaupol.gtk.dialogs import ErrorDialog
from gaupol.gtk.errors import Default
from gaupol.gtk.index import *
from .glade import GladeDialog


class SearchDialog(GladeDialog):

    """Dialog for searching for and replacing text.

    Instance variables:

        _all_radio:          gtk.RadioButton, target all subtitles
        _current_radio:      gtk.RadioButton, target the current project
        _ignore_case_check:  gtk.CheckButton, active to ignore case
        _main_check:         gtk.CheckButton, find in main text column
        _match_doc:          Document of the last match
        _match_page:         Page of the last match
        _match_row:          Row of the last match
        _match_span:         The start and end positions of the last match
        _next_button:        gtk.Button, find next match
        _pattern_combo:      gtk.ComboBoxEntry, patterns to find
        _pattern_entry:      gtk.Entry, pattern to find
        _previous_button:    gtk.Button, find previous match
        _regex_check:        gtk.CheckButton, if active pattern is a regex
        _replace_all_button: gtk.Button, replace all matches
        _replace_button:     gtk.Button, replace the current match
        _replacement_combo:  gtk.ComboBoxEntry, replacements
        _replacement_entry:  gtk.Entry, replacement
        _text_view:          gtk.TextView, text of the matching subtitle
        _tran_check:         gtk.CheckButton, find in translation text column
        _was_next:           True if last find was next, False for previous
        application:         Associated Application
    """

    def __init__(self, application):

        GladeDialog.__init__(self, "search-dialog")
        get_widget = self._glade_xml.get_widget
        self._all_radio          = get_widget("all_radio")
        self._current_radio      = get_widget("current_radio")
        self._ignore_case_check  = get_widget("ignore_case_check")
        self._main_check         = get_widget("main_check")
        self._next_button        = get_widget("next_button")
        self._pattern_combo      = get_widget("pattern_combo")
        self._pattern_entry      = self._pattern_combo.child
        self._previous_button    = get_widget("previous_button")
        self._regex_check        = get_widget("regex_check")
        self._replace_all_button = get_widget("replace_all_button")
        self._replace_button     = get_widget("replace_button")
        self._replacement_combo  = get_widget("replacement_combo")
        self._replacement_entry  = self._replacement_combo.child
        self._text_view          = get_widget("text_view")
        self._tran_check         = get_widget("tran_check")

        self._match_doc  = None
        self._match_page = None
        self._match_row  = None
        self._match_span = None
        self._was_next   = None
        self.application = application

        util.prepare_text_view(self._text_view)
        self._init_data()
        self._init_conf_handlers()
        self._init_search_handlers()
        self._init_target_handlers()
        self._init_sensitivities()
        self._init_sizes()
        self._dialog.set_transient_for(None)
        self._dialog.set_type_hint(gtk.gdk.WINDOW_TYPE_HINT_NORMAL)
        self._dialog.set_default_response(gtk.RESPONSE_CLOSE)

    @util.ignore_exceptions(AssertionError)
    def _add_pattern(self):
        """Add the current pattern to the pattern combo box."""

        pattern = self._pattern_entry.get_text()
        store = self._pattern_combo.get_model()
        assert pattern != self.application.pattern
        self.application.pattern = pattern
        conf.search.patterns.insert(0, pattern)
        conf.search.patterns = util.get_unique(conf.search.patterns)
        while len(conf.search.patterns) > conf.search.max_history:
            conf.search.patterns.pop()

        store.clear()
        for pattern in conf.search.patterns:
            store.append([pattern])
        self.application.update_gui()

    @util.ignore_exceptions(AssertionError)
    def _add_replacement(self):
        """Add the current replacement to the replacement combo box."""

        replacement = self._replacement_entry.get_text()
        store = self._replacement_combo.get_model()
        assert replacement != self.application.replacement
        self.application.replacement = replacement
        conf.search.replacements.insert(0, replacement)
        conf.search.replacements = util.get_unique(conf.search.replacements)
        while len(conf.search.replacements) > conf.search.max_history:
            conf.search.replacements.pop()

        store.clear()
        for replacement in conf.search.replacements:
            store.append([replacement])
        self.application.update_gui()

    def _admit_failure(self):
        """Set failure state and inform of zarro matchees."""

        self._match_page = None
        self._match_doc = None
        self._match_row = None
        self._match_span = None
        self._text_view.get_buffer().set_text("")
        self._text_view.set_sensitive(False)
        pattern = self._pattern_entry.get_text()
        message = _('"%s" not found') % pattern
        self.application.push_message(message)

    def _admit_success(self, page, row, doc, match_span, next):
        """Update data and text view."""

        self._match_page = page
        self._match_row = row
        self._match_doc = doc
        self._match_span = list(match_span[:])
        self._was_next = next

        self.application.set_current_page(page)
        self._set_text(page, row, doc, match_span)
        col = page.document_to_text_column(doc)
        page.view.set_focus(row, col)
        page.view.scroll_to_row(row)
        self._replace_button.set_sensitive(True)
        self._add_pattern()

    def _get_cursor_offset(self, page, row, doc, next):
        """Return the cursor offset in the current text or None."""

        try:
            assert page == self._match_page
            assert row == self._match_row
            assert doc == self._match_doc
            return self._match_span[next]
        except AssertionError:
            return None

    def _get_position(self, next):
        """Get the current position in the view.

        Raise Default if no pages open.
        Return row, document, position.
        """
        page = self.application.get_current_page()
        if page is None:
            raise Default
        rows = page.view.get_selected_rows()
        row = (rows[0] if rows else None)
        if row is None:
            row = (len(page.project.times) - 1, 0)[next]
        col = page.view.get_focus()[1]
        doc = None
        if col in (MTXT, TTXT):
            doc = page.text_column_to_document(col)
        docs = list(page.text_column_to_document(x) for x in conf.search.cols)
        if doc is None or doc not in docs:
            doc = (docs[-1], docs[0])[next]
        pos = self._get_cursor_offset(page, row, doc, next)
        return row, doc, pos

    def _init_conf_handlers(self):
        """Initialize configuration signal handlers."""

        def update_page(page):
            translate = page.text_column_to_document
            docs = list(translate(x) for x in conf.search.cols)
            wrap = (conf.search.target != cons.TARGET.ALL)
            page.project.set_search_target(None, docs, wrap)

        def update_pages(*args):
            for page in self.application.pages:
                update_page(page)

        self.application.connect("page-added", update_pages)
        conf.search.connect("notify::cols", update_pages)
        conf.search.connect("notify::target", update_pages)
        update_pages()

    def _init_data(self):
        """Initialize default values for widgets."""

        self._pattern_entry.set_text(self.application.pattern)
        self._replacement_entry.set_text(self.application.replacement)
        self._regex_check.set_active(conf.search.regex)
        self._ignore_case_check.set_active(conf.search.ignore_case)

        target = conf.search.target
        self._main_check.set_active(MTXT in conf.search.cols)
        self._tran_check.set_active(TTXT in conf.search.cols)
        self._all_radio.set_active(target == cons.TARGET.ALL)
        self._current_radio.set_active(target == cons.TARGET.CURRENT)

        store = self._pattern_combo.get_model()
        store.clear()
        for pattern in conf.search.patterns:
            store.append([pattern])

        store = self._replacement_combo.get_model()
        store.clear()
        for replacement in conf.search.replacements:
            store.append([replacement])

    def _init_search_handlers(self):
        """Initialize search signal handlers."""

        util.connect(self, "_next_button"       , "clicked" )
        util.connect(self, "_pattern_entry"     , "changed" )
        util.connect(self, "_previous_button"   , "clicked" )
        util.connect(self, "_regex_check"       , "toggled" )
        util.connect(self, "_replace_all_button", "clicked" )
        util.connect(self, "_replace_button"    , "clicked" )
        util.connect(self, self, "response")

        def disable_replace(*args):
            self._replace_button.set_sensitive(False)
        text_buffer = self._text_view.get_buffer()
        text_buffer.connect("changed", disable_replace)
        util.connect(self, "_text_view", "focus-out-event")

        def save_ignore_case(check_button):
            conf.search.ignore_case = check_button.get_active()
        self._ignore_case_check.connect("toggled", save_ignore_case)

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
        if not conf.editor.use_default_font:
            util.set_label_font(label, conf.editor.font)
        width, height = label.size_request()
        self._text_view.set_size_request(width + 4, height + 7)

    def _init_target_handlers(self):
        """Initialize target signal handlers."""

        def save_columns(*args):
            main = ([MTXT] if self._main_check.get_active() else [])
            tran = ([TTXT] if self._tran_check.get_active() else [])
            conf.search.cols = (main + tran)
        self._main_check.connect("toggled", save_columns)
        self._tran_check.connect("toggled", save_columns)

        def save_target(*args):
            if self._current_radio.get_active():
                conf.search.target = cons.TARGET.CURRENT
            elif self._all_radio.get_active():
                conf.search.target = cons.TARGET.ALL
        self._current_radio.connect("toggled", save_target)
        self._all_radio.connect("toggled", save_target)

    @util.ignore_exceptions(Default)
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

    @util.ignore_exceptions(Default)
    def _on_previous_button_clicked(self, *args):
        """Find the previous match of pattern."""

        # Make sure the text view experiences a focus-out-event.
        self._previous_button.grab_focus()
        self.previous()

    def _on_regex_check_toggled(self, check_button):
        """Save regular expression setting and update sensitivities."""

        active = check_button.get_active()
        conf.search.regex = active
        self.set_response_sensitive(gtk.RESPONSE_HELP, active)

    def _on_replace_all_button_clicked(self, *args):
        """Replace all matches of pattern."""

        # Make sure the text view experiences a focus-out-event.
        self._replace_all_button.grab_focus()
        util.set_cursor_busy(self._dialog)
        self.replace_all()
        util.set_cursor_normal(self._dialog)

    def _on_replace_button_clicked(self, *args):
        """Replace the current match."""

        # Make sure the text view experiences a focus-out-event.
        self._replace_button.grab_focus()
        self.replace()

    def _on_response(self, dialog, response):
        """Do not send response if browsing help."""

        if response == gtk.RESPONSE_HELP:
            util.browse_url(urls.REGEX_HELP)
            self.stop_emission("response")

    @util.ignore_exceptions(AssertionError)
    def _on_text_view_focus_out_event(self, text_view, event):
        """Save changes made in the text view."""

        assert self._match_page is not None
        assert self._match_row is not None
        assert self._match_doc is not None
        assert self._text_view.props.sensitive
        page = self.application.get_current_page()
        assert page == self._match_page

        text_buffer = text_view.get_buffer()
        bounds = text_buffer.get_bounds()
        text = text_buffer.get_text(*bounds)
        page.project.set_text(self._match_row, self._match_doc, text)

    def _set_pattern(self, page):
        """Set the search pattern for page.

        Raise Default if pattern is empty or if it sucks.
        """
        pattern = self._pattern_entry.get_text()
        if not pattern:
            raise Default
        ignore_case = self._ignore_case_check.get_active()
        if not conf.search.regex:
            return page.project.set_search_string(pattern, ignore_case)
        flags = (re.IGNORECASE if ignore_case else 0)
        try:
            page.project.set_search_regex(pattern, flags)
        except re.error, message:
            self._show_regex_error_dialog(message)
            raise Default

    def _set_replacement(self, page):
        """Set the search replacement for page.

        Raise Default if replacement is empty.
        """
        replacement = self._replacement_entry.get_text()
        page.project.set_search_replacement(replacement)

    def _set_text(self, page, row, doc, match_span):
        """Set text to text view."""

        text_buffer = self._text_view.get_buffer()
        text = page.project.get_texts(doc)[row]
        text_buffer.set_text(text)
        ins = text_buffer.get_iter_at_offset(match_span[1])
        bound = text_buffer.get_iter_at_offset(match_span[0])
        text_buffer.select_range(ins, bound)
        mark = text_buffer.create_mark(None, ins, True)
        self._text_view.scroll_to_mark(mark, 0.2)
        self._text_view.set_sensitive(True)
        self._text_view.grab_focus()

    def _show_regex_error_dialog(self, message):
        """Show an error dialog after regex failed to compile."""

        title = _('Error in regular expression')
        message = _("%s.") % message
        dialog = ErrorDialog(self._dialog, title, message)
        dialog.add_button(gtk.STOCK_OK, gtk.RESPONSE_OK)
        self.flash_dialog(dialog)

    def next(self):
        """Find the next match of pattern.

        Raise Default if no pages or no (acceptable) pattern.
        """
        page = self.application.get_current_page()
        row, doc, pos = self._get_position(True)
        i = self.application.pages.index(page)
        # Loop twice over the current page, since starting in the middle.
        pages = self.application.pages[i:] + self.application.pages[:i + 1]
        for page in pages:
            self._set_pattern(page)
            try:
                # Return match in page after position.
                row, doc, span = page.project.find_next(row, doc, pos)
                return self._admit_success(page, row, doc, span, True)
            except StopIteration:
                if conf.search.target == cons.TARGET.CURRENT:
                    # Fail wrapped single-page search.
                    return self._admit_failure()
                # Proceed to the next page.
                row = doc = pos = None
        self._admit_failure()

    def previous(self):
        """Find the previous match of pattern.

        Raise Default if no pages or no (acceptable) pattern.
        """
        page = self.application.get_current_page()
        row, doc, pos = self._get_position(False)
        pages = self.application.pages[::-1]
        i = pages.index(page)
        # Loop twice over the current page, since starting in the middle.
        pages = pages[i:] + pages[:i + 1]
        for page in pages:
            self._set_pattern(page)
            try:
                # Return match in page before position.
                row, doc, span = page.project.find_previous(row, doc, pos)
                return self._admit_success(page, row, doc, span, False)
            except StopIteration:
                if conf.search.target == cons.TARGET.CURRENT:
                    # Fail wrapped single-page search.
                    return self._admit_failure()
                # Proceed to the previous page.
                row = doc = pos = None
        self._admit_failure()

    @util.ignore_exceptions(AssertionError, Default)
    def replace(self):
        """Replace the current match."""

        page = self.application.get_current_page()
        assert page == self._match_page
        self._set_replacement(page)
        texts = page.project.get_texts(self._match_doc)
        length = len(texts[self._match_row])
        page.project.replace()
        self._add_replacement()
        shift = (len(texts[self._match_row]) - length)
        self._match_span[1] += shift
        (self.previous, self.next)[self._was_next]()

    def replace_all(self):
        """Replace all matches of pattern."""

        count = 0
        if conf.search.target == cons.TARGET.CURRENT:
            pages = [self.application.get_current_page()]
        elif conf.search.target == cons.TARGET.ALL:
            pages = self.application.pages
        for page in pages:
            self._set_pattern(page)
            self._set_replacement(page)
            count += page.project.replace_all()

        self._match_page = None
        self._match_doc = None
        self._match_row = None
        self._match_span = None
        self._text_view.get_buffer().set_text("")
        self._text_view.set_sensitive(False)
        self._add_pattern()
        self._add_replacement()
        message = _("Found and replaced %d occurences") % count
        self.application.push_message(message)
