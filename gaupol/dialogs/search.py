# -*- coding: utf-8 -*-

# Copyright (C) 2006 Osmo Salomaa
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

"""Dialog for searching for and replacing text."""

import aeidon
import functools
import gaupol
import os
import re

from aeidon.i18n   import _, n_
from gi.repository import Gdk
from gi.repository import Gtk

__all__ = ("SearchDialog",)


def page_changing(function):
    """Decorator for :class:`SearchDialog` methods that edit data."""
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        args[0]._handle_page_changes = False
        value = function(*args, **kwargs)
        args[0]._handle_page_changes = True
        return value
    return wrapper


class SearchDialog(gaupol.BuilderDialog):

    """
    Dialog for searching for and replacing text.

    :ivar _handle_page_changes: ``True`` to invalidate search on page changes
    :ivar _match_doc: :attr:`gaupol.documents` item of the last match
    :ivar _match_page: :class:`gaupol.Page` instance of the last match
    :ivar _match_row: Row in :attr:`_match_page` of the last match
    :ivar _match_span: Start, end position of the last match
    :ivar patterns: List of patterns previously searched for
    :ivar replacements: List of replacements previously used
    :ivar _statuslabel: Instance of :class:`gaupol.FloatingLabel` used
    :ivar _was_next: ``True`` if the last search was "next", else ``False``
    """

    _widgets = [
        "all_radio",
        "current_radio",
        "ignore_case_check",
        "main_check",
        "next_button",
        "overlay",
        "pattern_combo",
        "previous_button",
        "regex_check",
        "replace_all_button",
        "replace_button",
        "replacement_combo",
        "search_vbox",
        "text_view",
        "tran_check",
    ]

    def __init__(self, parent, application):
        """Initialize a :class:`SearchDialog` instance."""
        gaupol.BuilderDialog.__init__(self, "search-dialog.ui")
        self.application = application
        self._handle_page_changes = True
        self._match_doc = None
        self._match_page = None
        self._match_row = None
        self._match_span = None
        self.max_history = 10
        self._pattern_entry = None
        self.patterns = []
        self._replacement_entry = None
        self.replacements = []
        self._statuslabel = gaupol.FloatingLabel()
        self._was_next = None
        self._read_history("patterns")
        self._read_history("replacements")
        self._init_dialog(parent)
        self._init_text_view()
        self._init_pattern_combo()
        self._init_replacement_combo()
        self._init_keys()
        self._init_values()
        self._init_signal_handlers()
        self._init_sensitivities()
        self._overlay.add_overlay(self._statuslabel)
        self._overlay.show_all()
        self._statuslabel.set_text(None)

    def _add_pattern_to_history(self):
        """Add current pattern to the pattern combo box."""
        pattern = self._pattern_entry.get_text()
        store = self._pattern_combo.get_model()
        if pattern == self.application.pattern: return
        self.application.pattern = pattern
        self.patterns.insert(0, pattern)
        self.patterns = aeidon.util.get_unique(self.patterns)
        del self.patterns[self.max_history:]
        store.clear()
        for pattern in self.patterns:
            store.append((pattern,))
        self._write_history("patterns")
        self.application.update_gui()

    def _add_replacement_to_history(self):
        """Add current replacement to the replacement combo box."""
        replacement = self._replacement_entry.get_text()
        store = self._replacement_combo.get_model()
        if replacement == self.application.replacement: return
        self.application.replacement = replacement
        self.replacements.insert(0, replacement)
        self.replacements = aeidon.util.get_unique(self.replacements)
        del self.replacements[self.max_history:]
        store.clear()
        for replacement in self.replacements:
            store.append((replacement,))
        self._write_history("replacements")
        self.application.update_gui()

    def _get_cursor_offset(self, page, row, doc, next):
        """Return current cursor offset of the search or ``None``."""
        if page is not self._match_page: return None
        if row != self._match_row: return None
        if doc != self._match_doc: return None
        return self._match_span[next]

    def _get_fields(self):
        """Return a sequence of fields to search in."""
        fields = []
        if self._main_check.get_active():
            fields.append(gaupol.fields.MAIN_TEXT)
        if self._tran_check.get_active():
            fields.append(gaupol.fields.TRAN_TEXT)
        return tuple(fields)

    def _get_position(self, next):
        """
        Return current position of the search.

        Raise :exc:`gaupol.Default` if no pages open.
        Return row, document, cursor offset.
        """
        page = self.application.get_current_page()
        gaupol.util.raise_default(page is None)
        rows = page.view.get_selected_rows()
        row = rows[0] if rows else None
        if row is None:
            row = 0 if next else len(page.project.subtitles) - 1
        col = page.view.get_focus()[1]
        doc = None
        if page.view.is_text_column(col):
            doc = page.text_column_to_document(col)
        docs = list(map(gaupol.util.text_field_to_document,
                        gaupol.conf.search.fields))

        if doc is None or not doc in docs:
            doc = docs[0] if next else docs[-1]
        pos = self._get_cursor_offset(page, row, doc, next)
        return row, doc, pos

    def _get_target(self):
        """Return :attr:`gaupol.targets` item to search in."""
        if self._current_radio.get_active():
            return gaupol.targets.CURRENT
        if self._all_radio.get_active():
            return gaupol.targets.ALL
        raise ValueError("Invalid target radio state")

    def _init_dialog(self, parent):
        """Initialize the dialog."""
        self.add_button(_("_Help"), Gtk.ResponseType.HELP)
        self._dialog.set_default_response(Gtk.ResponseType.CLOSE)
        self._dialog.set_transient_for(parent)
        self.set_modal(False)

    def _init_keys(self):
        """Initialize keyboard shortcuts."""
        accel_group = Gtk.AccelGroup()
        accel_group.connect(Gdk.KEY_f,
                            Gdk.ModifierType.CONTROL_MASK,
                            Gtk.AccelFlags.MASK,
                            self._on_find_key_pressed)

        self.add_accel_group(accel_group)

    def _init_pattern_combo(self):
        """Initialize the pattern combo box."""
        store = Gtk.ListStore(str)
        self._pattern_combo.set_model(store)
        for pattern in self.patterns:
            store.append((pattern,))
        self._pattern_combo.set_entry_text_column(0)
        self._pattern_entry = self._pattern_combo.get_child()

    def _init_replacement_combo(self):
        """Initialize the replacement combo box."""
        store = Gtk.ListStore(str)
        self._replacement_combo.set_model(store)
        for replacement in self.replacements:
            store.append((replacement,))
        self._replacement_combo.set_entry_text_column(0)
        self._replacement_entry = self._replacement_combo.get_child()

    def _init_sensitivities(self):
        """Initialize widget sensitivities."""
        self._next_button.set_sensitive(False)
        self._pattern_entry.emit("changed")
        self._previous_button.set_sensitive(False)
        self._regex_check.emit("toggled")
        self._replace_all_button.set_sensitive(False)
        self._replace_button.set_sensitive(False)
        self._replacement_entry.emit("changed")
        self._text_view.set_sensitive(False)

    def _init_signal_handlers(self):
        """Initialize signal handlers."""
        aeidon.util.connect(self, "_pattern_entry", "changed")
        aeidon.util.connect(self, "application", "page-changed")
        callback = lambda *args: args[-1]._update_search_targets()
        self.application.connect("page-added", callback, self)
        gaupol.conf.search.connect("notify::fields", callback, self)
        gaupol.conf.search.connect("notify::target", callback, self)

    def _init_text_view(self):
        """Initialize the text view."""
        with aeidon.util.silent(AttributeError):
            # Top and bottom margins available since GTK 3.18.
            self._text_view.set_top_margin(6)
            self._text_view.set_bottom_margin(6)
        gaupol.util.prepare_text_view(self._text_view)
        gaupol.util.scale_to_size(self._text_view,
                                  nchar=55,
                                  nlines=6,
                                  font="custom")

        text_buffer = self._text_view.get_buffer()
        text_buffer.connect("changed", self._on_text_buffer_changed)

    def _init_values(self):
        """Initialize default values for widgets."""
        self._pattern_entry.set_text(self.application.pattern)
        self._replacement_entry.set_text(self.application.replacement)
        self._regex_check.set_active(gaupol.conf.search.regex)
        self._ignore_case_check.set_active(gaupol.conf.search.ignore_case)
        fields = gaupol.conf.search.fields
        target = gaupol.conf.search.target
        self._main_check.set_active(gaupol.fields.MAIN_TEXT in fields)
        self._tran_check.set_active(gaupol.fields.TRAN_TEXT in fields)
        self._all_radio.set_active(target == gaupol.targets.ALL)
        self._current_radio.set_active(target == gaupol.targets.CURRENT)
        self._update_search_targets()

    @aeidon.deco.silent(gaupol.Default)
    def next(self):
        """Find the next match of pattern."""
        page = self.application.get_current_page()
        row, doc, pos = self._get_position(next=True)
        pages = self.application.pages[:]
        i = pages.index(page)
        # Loop twice over the current page,
        # since starting in the middle.
        for page in (pages[i:] + pages[:i+1]):
            self._set_pattern(page)
            try:
                # Return match in page after position.
                row, doc, span = page.project.find_next(row, doc, pos)
                return self._set_success_state(page, row, doc, span, next=True)
            except StopIteration:
                target = gaupol.conf.search.target
                if target == gaupol.targets.CURRENT:
                    # Fail wrapped single-page search.
                    return self._set_failure_state()
                # Proceed to the next page.
                row = doc = pos = None
        # Fail wrapped search of all pages.
        self._set_failure_state()

    def _on_all_radio_toggled(self, radio_button):
        """Save search target."""
        gaupol.conf.search.target = self._get_target()

    def _on_application_page_changed(self, application, page):
        """Invalidate the current search if underlying data has changed."""
        # If data in page was changed from outside the search dialog,
        # the current search must be invalidated to avoid making edits
        # (especially via the text view's focus-out handler) based on data
        # that no longer exists. All search dialog's data changing methods
        # need to be wrapped to disable this handling of application's
        # page-changed signals.
        if self._handle_page_changes:
            if self._match_page is not None:
                self._reset_properties()

    def _on_current_radio_toggled(self, radio_button):
        """Save search target."""
        gaupol.conf.search.target = self._get_target()

    def _on_find_key_pressed(self, *args):
        """Move focus to the pattern entry."""
        self._pattern_entry.grab_focus()

    def _on_ignore_case_check_toggled(self, check_button):
        """Save ignore case setting."""
        gaupol.conf.search.ignore_case = check_button.get_active()

    def _on_main_check_toggled(self, check_button):
        """Save search target."""
        gaupol.conf.search.fields = list(self._get_fields())
        self._search_vbox.set_sensitive(bool(self._get_fields()))

    def _on_next_button_clicked(self, *args):
        """Find the next match of pattern."""
        # Make sure the text view experiences a focus-out-event.
        self._next_button.grab_focus()
        self.next()

    def _on_pattern_entry_changed(self, entry):
        """Update action sensitivities."""
        have_pattern = bool(entry.get_text())
        self._next_button.set_sensitive(have_pattern)
        self._previous_button.set_sensitive(have_pattern)
        self._replace_all_button.set_sensitive(have_pattern)

    def _on_previous_button_clicked(self, *args):
        """Find the previous match of pattern."""
        # Make sure the text view experiences a focus-out-event.
        self._previous_button.grab_focus()
        self.previous()

    def _on_regex_check_toggled(self, check_button):
        """Save regular expression setting."""
        use_regex = check_button.get_active()
        gaupol.conf.search.regex = use_regex
        self.set_response_sensitive(Gtk.ResponseType.HELP, use_regex)

    def _on_replace_all_button_clicked(self, *args):
        """Replace all matches of pattern."""
        # Make sure the text view experiences a focus-out-event.
        self._replace_all_button.grab_focus()
        gaupol.util.set_cursor_busy(self._dialog)
        self.replace_all()
        gaupol.util.set_cursor_normal(self._dialog)

    def _on_replace_button_clicked(self, *args):
        """Replace the current match of pattern."""
        # Make sure the text view experiences a focus-out-event.
        self._replace_button.grab_focus()
        self._replace_button.set_sensitive(False)
        self.replace()

    def _on_response(self, dialog, response):
        """Do not send response if browsing help."""
        if response == Gtk.ResponseType.HELP:
            gaupol.util.show_uri(gaupol.REGEX_HELP_URL)
            self.stop_emission_by_name("response")

    def _on_show(self, *args):
        """Move focus to the pattern entry and select the pattern."""
        self._pattern_entry.select_region(0, -1)
        self._pattern_entry.grab_focus()

    def _on_text_buffer_changed(self, *args):
        """Disable replace action."""
        self._replace_button.set_sensitive(False)

    @page_changing
    def _on_text_view_focus_out_event(self, text_view, event):
        """Save changes made in `text_view`."""
        if self._match_page is None: return
        if self._match_row  is None: return
        if self._match_doc  is None: return
        if not self._text_view.get_sensitive(): return
        page = self.application.get_current_page()
        if page is not self._match_page: return
        text_buffer = text_view.get_buffer()
        start, end = text_buffer.get_bounds()
        text = text_buffer.get_text(start, end, False)
        page.project.set_text(self._match_row, self._match_doc, text)

    def _on_tran_check_toggled(self, check_button):
        """Save search target."""
        gaupol.conf.search.fields = list(self._get_fields())
        self._search_vbox.set_sensitive(bool(self._get_fields()))

    @aeidon.deco.silent(gaupol.Default)
    def previous(self):
        """Find the previous match of pattern."""
        page = self.application.get_current_page()
        row, doc, pos = self._get_position(next=False)
        pages = self.application.pages[::-1]
        i = pages.index(page)
        # Loop twice over the current page,
        # since starting in the middle.
        for page in (pages[i:] + pages[:i+1]):
            self._set_pattern(page)
            try:
                # Return match in page before position.
                row, doc, span = page.project.find_previous(row, doc, pos)
                return self._set_success_state(page, row, doc, span, next=False)
            except StopIteration:
                target = gaupol.conf.search.target
                if target == gaupol.targets.CURRENT:
                    # Fail wrapped single-page search.
                    return self._set_failure_state()
                # Proceed to the previous page.
                row = doc = pos = None
        # Fail wrapped search of all pages.
        self._set_failure_state()

    def _read_history(self, name):
        """Read history from file of type `name`."""
        directory = os.path.join(aeidon.CONFIG_HOME_DIR, "search")
        path = os.path.join(directory, "{}.history".format(name))
        if not os.path.isfile(path): return
        history = aeidon.util.readlines(path)
        setattr(self, name, history)

    @page_changing
    @aeidon.deco.silent(gaupol.Default)
    def replace(self):
        """Replace the current match of pattern."""
        page = self.application.get_current_page()
        if page is not self._match_page: return
        self._set_replacement(page)
        subtitle = page.project.subtitles[self._match_row]
        length = len(subtitle.get_text(self._match_doc))
        try:
            page.project.replace()
        except re.error as error:
            return self._show_regex_error_dialog_replacement(str(error))
        shift = (len(subtitle.get_text(self._match_doc)) - length)
        self._match_span[1] += shift
        if self._was_next:
            return self.next()
        return self.previous()

    @page_changing
    @aeidon.deco.silent(gaupol.Default)
    def replace_all(self):
        """Replace all matches of pattern."""
        count = 0
        target = gaupol.conf.search.target
        for page in self.application.get_target_pages(target):
            self._set_pattern(page)
            self._set_replacement(page)
            try:
                count += page.project.replace_all()
            except re.error as error:
                self._show_regex_error_dialog_replacement(str(error))
                break
        self._reset_properties()
        self._statuslabel.flash_text(n_(
            "Found and replaced {:d} occurence",
            "Found and replaced {:d} occurences",
            count).format(count))

    def _reset_properties(self):
        """Reset search properties to defaults."""
        self._match_page = None
        self._match_doc  = None
        self._match_row  = None
        self._match_span = None
        self._text_view.get_buffer().set_text("")
        self._text_view.set_sensitive(False)

    def _set_failure_state(self):
        """Set search properties for failure to find a match."""
        self._reset_properties()
        pattern = self._pattern_entry.get_text()
        message = _('"{}" not found').format(pattern)
        self._statuslabel.flash_text(message)

    def _set_pattern(self, page):
        """
        Set search pattern for `page`.

        Raise :exc:`gaupol.Default` if pattern empty or bad.
        """
        pattern = self._pattern_entry.get_text()
        gaupol.util.raise_default(not pattern)
        ignore_case = gaupol.conf.search.ignore_case
        if not gaupol.conf.search.regex:
            self._add_pattern_to_history()
            return page.project.set_search_string(pattern, ignore_case)
        flags = re.DOTALL | re.MULTILINE
        if gaupol.conf.search.ignore_case:
            flags = flags | re.IGNORECASE
        try:
            page.project.set_search_regex(pattern, flags)
        except re.error as error:
            self._show_regex_error_dialog_pattern(str(error))
            raise gaupol.Default
        self._add_pattern_to_history()

    def _set_replacement(self, page):
        """Set search replacement for `page`."""
        replacement = self._replacement_entry.get_text()
        page.project.set_search_replacement(replacement)
        self._add_replacement_to_history()

    def _set_success_state(self, page, row, doc, match_span, next):
        """Set search properties for found match."""
        self._match_page = page
        self._match_row = row
        self._match_doc = doc
        self._match_span = list(match_span)
        self._was_next = next
        self.application.set_current_page(page)
        self._set_text(page, row, doc, match_span)
        col = page.document_to_text_column(doc)
        page.view.set_focus(row, col)
        page.view.scroll_to_row(row)
        self._replace_button.set_sensitive(True)

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
        self._text_view.scroll_to_mark(mark=mark,
                                       within_margin=0,
                                       use_align=False,
                                       xalign=0.5,
                                       yalign=0.5)

        self._text_view.set_sensitive(True)
        self._text_view.grab_focus()

    def _show_regex_error_dialog_pattern(self, message):
        """Show an error dialog if regex pattern failed to compile."""
        title = _("Error in regular expression pattern")
        dialog = gaupol.ErrorDialog(self._dialog, title, message)
        dialog.add_button(_("_OK"), Gtk.ResponseType.OK)
        dialog.set_default_response(Gtk.ResponseType.OK)
        gaupol.util.flash_dialog(dialog)

    def _show_regex_error_dialog_replacement(self, message):
        """Show an error dialog if regex replacement is invalid."""
        title = _("Error in regular expression replacement")
        dialog = gaupol.ErrorDialog(self._dialog, title, message)
        dialog.add_button(_("_OK"), Gtk.ResponseType.OK)
        dialog.set_default_response(Gtk.ResponseType.OK)
        gaupol.util.flash_dialog(dialog)

    def _update_search_targets(self):
        """Update search targets in all pages."""
        docs = list(map(gaupol.util.text_field_to_document,
                        gaupol.conf.search.fields))

        wrap = (gaupol.conf.search.target != gaupol.targets.ALL)
        for page in self.application.pages:
            page.project.set_search_target(None, docs, wrap)

    def _write_history(self, name):
        """Write history to file of type `name`."""
        directory = os.path.join(aeidon.CONFIG_HOME_DIR, "search")
        with aeidon.util.silent(OSError, tb=True):
            path = os.path.join(directory, "{}.history".format(name))
            history = getattr(self, name)
            text = "\n".join(history) + "\n"
            aeidon.util.write(path, text)
