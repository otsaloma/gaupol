# Copyright (C) 2006 Osmo Salomaa
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


"""Dialogs for finding and replacing text."""


from gettext import gettext as _
import re

import gobject
import gtk

from gaupol.base.util import listlib, wwwlib
from gaupol.gtk       import cons
from gaupol.gtk.icons import *
from gaupol.gtk.error import Default
from gaupol.gtk.urls  import REGEX_HELP_URL
from gaupol.gtk.util  import conf, gtklib


class FindDialog(gobject.GObject):

    """Dialog for finding text."""

    __gsignals__ = {
        'coordinate-request': (
            gobject.SIGNAL_RUN_LAST,
            object,
            ()
        ),
        'destroyed': (
            gobject.SIGNAL_RUN_LAST,
            None,
            ()
        ),
        'message': (
            gobject.SIGNAL_RUN_LAST,
            None,
            (str,)
        ),
        'next-page': (
            gobject.SIGNAL_RUN_LAST,
            None,
            ()
        ),
        'previous-page': (
            gobject.SIGNAL_RUN_LAST,
            None,
            ()
        ),
        'update': (
            gobject.SIGNAL_RUN_LAST,
            None,
            ()
        ),
    }

    def __init__(self):

        gobject.GObject.__init__(self)

        self._page              = None
        self._row               = None
        self._doc               = None
        self._match_span        = None
        self._first_passed_page = None
        self._last_is_next      = None

        glade_xml = gtklib.get_glade_xml('find-dialog')
        self._all_radio         = glade_xml.get_widget('all_radio')
        self._current_radio     = glade_xml.get_widget('current_radio')
        self._dialog            = glade_xml.get_widget('dialog')
        self._dot_all_check     = glade_xml.get_widget('dot_all_check')
        self._ignore_case_check = glade_xml.get_widget('ignore_case_check')
        self._main_check        = glade_xml.get_widget('main_check')
        self._multiline_check   = glade_xml.get_widget('multiline_check')
        self._next_button       = glade_xml.get_widget('next_button')
        self._pattern_combo     = glade_xml.get_widget('pattern_combo')
        self._pattern_entry     = self._pattern_combo.child
        self._previous_button   = glade_xml.get_widget('previous_button')
        self._regex_check       = glade_xml.get_widget('regex_check')
        self._text_view         = glade_xml.get_widget('text_view')
        self._tran_check        = glade_xml.get_widget('tran_check')

        self._init_data()
        self._init_signals()
        self._init_sensitivities()
        self._init_fonts()
        self._init_sizes()
        self._dialog.set_transient_for(None)
        self._dialog.set_type_hint(gtk.gdk.WINDOW_TYPE_HINT_NORMAL)
        self._dialog.set_default_response(gtk.RESPONSE_CLOSE)

    def _add_pattern(self):
        """Add current pattern to combo box."""

        pattern = self._pattern_entry.get_text()
        store = self._pattern_combo.get_model()
        try:
            if store[0][0] == pattern:
                if conf.find.pattern == pattern:
                    return
                conf.find.pattern = pattern
                self.emit('update')
                return
        except IndexError:
            pass
        conf.find.pattern = pattern
        conf.find.patterns.insert(0, pattern)
        conf.find.patterns = listlib.unique(conf.find.patterns)
        while len(conf.find.patterns) > conf.find.max_history:
            conf.find.patterns.pop()

        store.clear()
        for pattern in conf.find.patterns:
            store.append([pattern])

        self.emit('update')

    def _init_data(self):
        """Initialize default values."""

        self._dot_all_check.set_active(conf.find.dot_all)
        self._ignore_case_check.set_active(conf.find.ignore_case)
        self._multiline_check.set_active(conf.find.multiline)
        self._pattern_entry.set_text(conf.find.pattern)
        self._regex_check.set_active(conf.find.regex)

        target = conf.find.target
        self._all_radio.set_active(target == cons.Target.ALL)
        self._current_radio.set_active(target == cons.Target.CURRENT)
        self._main_check.set_active(MTXT in conf.find.cols)
        self._tran_check.set_active(TTXT in conf.find.cols)

        store = self._pattern_combo.get_model()
        store.clear()
        for pattern in conf.find.patterns:
            store.append([pattern])

    def _init_fonts(self):
        """Initialize fonts."""

        if not conf.editor.use_default_font:
            gtklib.set_widget_font(self._text_view    , conf.editor.font)
            gtklib.set_widget_font(self._pattern_entry, conf.editor.font)

    def _init_sensitivities(self):
        """Initialize sensitivities."""

        self._next_button.set_sensitive(False)
        self._previous_button.set_sensitive(False)
        self._text_view.set_sensitive(False)
        self._pattern_entry.emit('changed')
        self._regex_check.emit('toggled')

    def _init_signals(self):
        """Initialize signals."""

        gtklib.connect(self, '_all_radio'        , 'toggled'        )
        gtklib.connect(self, '_current_radio'    , 'toggled'        )
        gtklib.connect(self, '_dialog'           , 'response'       )
        gtklib.connect(self, '_dot_all_check'    , 'toggled'        )
        gtklib.connect(self, '_ignore_case_check', 'toggled'        )
        gtklib.connect(self, '_main_check'       , 'toggled'        )
        gtklib.connect(self, '_multiline_check'  , 'toggled'        )
        gtklib.connect(self, '_next_button'      , 'clicked'        )
        gtklib.connect(self, '_pattern_entry'    , 'changed'        )
        gtklib.connect(self, '_previous_button'  , 'clicked'        )
        gtklib.connect(self, '_regex_check'      , 'toggled'        )
        gtklib.connect(self, '_text_view'        , 'focus-out-event')
        gtklib.connect(self, '_tran_check'       , 'toggled'        )

    def _init_sizes(self):
        """Initialize widget sizes."""

        label = gtk.Label('\n'.join(['x' * 46] * 4))
        if not conf.editor.use_default_font:
            gtklib.set_label_font(label, conf.editor.font)
        width, height = label.size_request()
        self._text_view.set_size_request(width + 4, height + 7)

    def _fail(self):
        """Clean up and dislay failure dialog."""

        self._page = None
        self._row  = None
        self._doc  = None
        self._match_span = None
        self._first_passed_page = None

        text_buffer = self._text_view.get_buffer()
        text_buffer.set_text('')
        self._text_view.set_sensitive(False)

        pattern = self._pattern_entry.get_text()
        self.emit('message', _('Pattern "%s" not found') % pattern)

    def _get_columns(self):
        """Get target columns."""

        cols = []
        if self._main_check.get_active():
            cols.append(MTXT)
        if self._tran_check.get_active():
            cols.append(TTXT)
        return cols

    def _get_documents(self, page):
        """Get target documents."""

        cols = self._get_columns()
        return list(page.text_column_to_document(x) for x in cols)

    def _get_flags(self):
        """Get regular expression flags."""

        flags = 0
        if conf.find.dot_all:
            flags = flags|re.DOTALL
        if conf.find.ignore_case:
            flags = flags|re.IGNORECASE
        if conf.find.multiline:
            flags = flags|re.MULTILINE
        return flags

    def _get_position(self, page, row, doc, next):
        """Return position or None."""

        if page == self._page:
            if row == self._row:
                if doc == self._doc:
                    return self._match_span[next]
        return None

    def _get_target(self):
        """Get target."""

        if self._all_radio.get_active():
            return cons.Target.ALL
        elif self._current_radio.get_active():
            return cons.Target.CURRENT
        raise ValueError

    def _get_text(self, page, row, doc):
        """Get text."""

        if doc == MAIN:
            return page.project.main_texts[row]
        if doc == TRAN:
            return page.project.tran_texts[row]
        raise ValueError

    def _get_wrap(self):
        """Return True to wrap find in single document."""

        if self._get_target() == cons.Target.ALL:
            return False
        return True

    def _on_all_radio_toggled(self, *args):
        """Save target."""

        conf.find.target = self._get_target()

    def _on_current_radio_toggled(self, *args):
        """Save target."""

        conf.find.target = self._get_target()

    def _on_dialog_response(self, dialog, response):
        """Browse help or destroy dialog."""

        if response == gtk.RESPONSE_HELP:
            wwwlib.browse_url(REGEX_HELP_URL)
            return True

        self._dialog.destroy()
        self.emit('destroyed')

    def _on_dot_all_check_toggled(self, check_button):
        """Save setting."""

        conf.find.dot_all = check_button.get_active()

    def _on_ignore_case_check_toggled(self, check_button):
        """Save setting."""

        conf.find.ignore_case = check_button.get_active()

    def _on_main_check_toggled(self, *args):
        """Save target columns."""

        conf.find.cols = self._get_columns()

    def _on_multiline_check_toggled(self, check_button):
        """Save setting."""

        conf.find.multiline = check_button.get_active()

    def _on_next_button_clicked(self, *args):
        """Find next."""

        self._next_button.grab_focus()
        try:
            self.next()
        except Default:
            pass

    def _on_pattern_entry_changed(self, entry):
        """Set action sensitivities."""

        sensitive = bool(entry.get_text())
        self._next_button.set_sensitive(sensitive)
        self._previous_button.set_sensitive(sensitive)

    def _on_previous_button_clicked(self, *args):
        """Find previous."""

        self._previous_button.grab_focus()
        try:
            self.previous()
        except Default:
            pass

    def _on_regex_check_toggled(self, check_button):
        """Save setting and set sensitivities."""

        active = check_button.get_active()
        conf.find.regex = active
        self._dot_all_check.set_sensitive(active)
        self._multiline_check.set_sensitive(active)
        self._dialog.set_response_sensitive(gtk.RESPONSE_HELP, active)

    def _on_text_view_focus_out_event(self, text_view, event):
        """Register changes."""

        if None in (self._page, self._row, self._doc):
            return False
        if not self._text_view.props.sensitive:
            return False
        page = self.emit('coordinate-request')[0]
        if page != self._page:
            return False

        text_buffer = text_view.get_buffer()
        start, end = text_buffer.get_bounds()
        new_text = text_buffer.get_text(start, end)
        orig_text = self._get_text(self._page, self._row, self._doc)
        if new_text != orig_text:
            self._page.project.set_text(self._row, self._doc, new_text)
            self.emit('update')
        return False

    def _on_tran_check_toggled(self, *args):
        """Save target columns."""

        conf.find.cols = self._get_columns()

    def _prepare(self, next):
        """
        Prepare find.

        Raise Default if no pages open.
        Return page, row, document, position, documents, wrap.
        """
        page, row, doc = self.emit('coordinate-request')
        if page is None:
            raise Default

        pos  = self._get_position(page, row, doc, next)
        docs = self._get_documents(page)
        wrap = self._get_wrap()

        if row is None:
            row = (len(page.project.times) - 1, 0)[next]
        if doc is None or doc not in docs:
            doc = (docs[-1], docs[0])[next]

        return page, row, doc, pos, docs, wrap

    def _set_pattern(self, page):
        """
        Set find pattern.

        Raise Default if no pattern.
        """
        pattern = self._pattern_entry.get_text()
        if not pattern:
            raise Default

        if self._regex_check.get_active():
            flags = self._get_flags()
            page.project.set_find_regex(pattern, flags)
        else:
            ignore_case = self._ignore_case_check.get_active()
            page.project.set_find_string(pattern, ignore_case)

    def _set_text(self, page, row, doc, match_span):
        """Set text to text view."""

        text_buffer = self._text_view.get_buffer()
        text_buffer.set_text(self._get_text(page, row, doc))
        ins = text_buffer.get_iter_at_offset(match_span[1])
        bound = text_buffer.get_iter_at_offset(match_span[0])
        text_buffer.select_range(ins, bound)
        self._text_view.set_sensitive(True)
        self._text_view.grab_focus()

        col = page.document_to_text_column(doc)
        page.view.set_focus(row, col)
        page.view.scroll_to_row(row)

    def _succeed(self, page, row, doc, match_span, next):
        """Update data and text view."""

        self._page = page
        self._row  = row
        self._doc  = doc
        self._match_span = list(match_span[:])
        self._first_passed_page = None
        self._last_is_next = next

        self._set_text(page, row, doc, match_span)
        self._add_pattern()

    def close(self):
        """Close dialog."""

        self._dialog.emit('response', gtk.RESPONSE_CLOSE)

    def next(self):
        """
        Find next.

        Raise Default if no pages or no pattern.
        """
        page, row, doc, pos, docs, wrap = self._prepare(True)
        page.project.set_find_target(None, docs, wrap)
        self._set_pattern(page)
        try:
            row, doc, match_span = page.project.find_next(row, doc, pos)
        except StopIteration:
            if wrap or page == self._first_passed_page:
                return self._fail()
            if self._first_passed_page is None:
                self._first_passed_page = page
            self.emit('next-page')
            return self.next()
        self._succeed(page, row, doc, match_span, True)

    def present(self):
        """Present dialog."""

        self._pattern_entry.select_region(0, -1)
        self._pattern_entry.grab_focus()
        self._dialog.present()

    def previous(self):
        """
        Find previous.

        Raise Default if no pages or no pattern.
        """
        page, row, doc, pos, docs, wrap = self._prepare(False)
        page.project.set_find_target(None, docs, wrap)
        self._set_pattern(page)
        try:
            row, doc, match_span = page.project.find_previous(row, doc, pos)
        except StopIteration:
            if wrap or page == self._first_passed_page:
                return self._fail()
            if self._first_passed_page is None:
                self._first_passed_page = page
            self.emit('previous-page')
            return self.previous()
        self._succeed(page, row, doc, match_span, False)

    def show(self):
        """Show dialog."""

        self._pattern_entry.select_region(0, -1)
        self._pattern_entry.grab_focus()
        self._dialog.show()


class ReplaceDialog(FindDialog):

    def __init__(self):

        gobject.GObject.__init__(self)

        self._page              = None
        self._row               = None
        self._doc               = None
        self._match_span        = None
        self._first_passed_page = None
        self._last_is_next      = None

        glade_xml = gtklib.get_glade_xml('replace-dialog')
        self._all_radio          = glade_xml.get_widget('all_radio')
        self._current_radio      = glade_xml.get_widget('current_radio')
        self._dialog             = glade_xml.get_widget('dialog')
        self._dot_all_check      = glade_xml.get_widget('dot_all_check')
        self._ignore_case_check  = glade_xml.get_widget('ignore_case_check')
        self._main_check         = glade_xml.get_widget('main_check')
        self._multiline_check    = glade_xml.get_widget('multiline_check')
        self._next_button        = glade_xml.get_widget('next_button')
        self._pattern_combo      = glade_xml.get_widget('pattern_combo')
        self._pattern_entry      = self._pattern_combo.child
        self._previous_button    = glade_xml.get_widget('previous_button')
        self._regex_check        = glade_xml.get_widget('regex_check')
        self._replace_all_button = glade_xml.get_widget('replace_all_button')
        self._replace_button     = glade_xml.get_widget('replace_button')
        self._replacement_combo  = glade_xml.get_widget('replacement_combo')
        self._replacement_entry  = self._replacement_combo.child
        self._text_view          = glade_xml.get_widget('text_view')
        self._tran_check         = glade_xml.get_widget('tran_check')

        self._init_data()
        self._init_signals()
        self._init_sensitivities()
        self._init_fonts()
        self._init_sizes()
        self._dialog.set_transient_for(None)
        self._dialog.set_type_hint(gtk.gdk.WINDOW_TYPE_HINT_NORMAL)
        self._dialog.set_default_response(gtk.RESPONSE_CLOSE)

    def _add_replacement(self):
        """Add current replacement to combo box."""

        replacement = self._replacement_entry.get_text()
        conf.find.replacement = replacement
        store = self._replacement_combo.get_model()
        try:
            if store[0] == replacement:
                return
        except IndexError:
            pass
        conf.find.replacements.insert(0, replacement)
        conf.find.replacements = listlib.unique(conf.find.replacements)
        while len(conf.find.replacements) > conf.find.max_history:
            conf.find.replacements.pop()

        store.clear()
        for replacement in conf.find.replacements:
            store.append([replacement])

    def _init_data(self):
        """Initialize default values."""

        FindDialog._init_data(self)

        self._replacement_entry.set_text(conf.find.replacement)

        store = self._replacement_combo.get_model()
        store.clear()
        for replacement in conf.find.replacements:
            store.append([replacement])

    def _init_fonts(self):
        """Initialize fonts."""

        FindDialog._init_fonts(self)

        if not conf.editor.use_default_font:
            gtklib.set_widget_font(self._replacement_entry, conf.editor.font)

    def _init_sensitivities(self):
        """Initialize sensitivities."""

        FindDialog._init_sensitivities(self)

        self._replace_all_button.set_sensitive(False)
        self._replace_button.set_sensitive(False)
        self._pattern_entry.emit('changed')
        self._replacement_entry.emit('changed')

    def _init_signals(self):
        """Initialize signals."""

        FindDialog._init_signals(self)

        gtklib.connect(self, '_replace_all_button', 'clicked')
        gtklib.connect(self, '_replace_button'    , 'clicked')

        text_buffer = self._text_view.get_buffer()
        text_buffer.connect('changed', self._on_text_buffer_changed)

    def _on_pattern_entry_changed(self, entry):
        """Set action sensitivities."""

        FindDialog._on_pattern_entry_changed(self, entry)

        sensitive = bool(entry.get_text())
        self._replace_all_button.set_sensitive(sensitive)

    def _on_replace_all_button_clicked(self, *args):
        """Replace all."""

        self._replace_all_button.grab_focus()

        count = 0
        page, row, doc, pos, docs, wrap = self._prepare(True)
        while True:
            page.project.set_find_target(None, docs, wrap)
            self._set_pattern(page)
            self._set_replacement(page)
            count += page.project.replace_all()
            self.emit('update')
            if wrap or page == self._first_passed_page:
                break
            if self._first_passed_page is None:
                self._first_passed_page = page
            self.emit('next-page')
            page = self.emit('coordinate-request')[0]

        self._page = None
        self._row  = None
        self._doc  = None
        self._match_span = None
        self._first_passed_page = None
        self._last_is_next = None

        text_buffer = self._text_view.get_buffer()
        text_buffer.set_text('')
        self._text_view.set_sensitive(False)
        self._add_pattern()
        self._add_replacement()

        pattern = self._pattern_entry.get_text()
        replacement = self._replacement_entry.get_text()
        self.emit('message', _('Replaced %d occurences of "%s" with "%s"') % (
            count, pattern, replacement))

    def _on_replace_button_clicked(self, *args):
        """Replace current match."""

        page = self.emit('coordinate-request')[0]
        if page != self._page:
            return

        self._replace_button.grab_focus()
        self._set_replacement(self._page)
        orig_len = len(self._get_text(self._page, self._row, self._doc))
        self._page.project.replace()
        new_len = len(self._get_text(self._page, self._row, self._doc))
        self.emit('update')
        self._add_replacement()

        shift = new_len - orig_len
        self._match_span[1] += shift

        try:
            (self.previous, self.next)[self._last_is_next]()
        except Default:
            pass

    def _on_text_buffer_changed(self, *args):
        """Set replace button sensitivity."""

        self._replace_button.set_sensitive(False)

    def _set_replacement(self, page):
        """
        Set find replacement.

        Raise Default if no replacement.
        """
        replacement = self._replacement_entry.get_text()
        page.project.set_find_replacement(replacement)

    def _succeed(self, page, row, doc, match_span, next):
        """Update data and text view."""

        FindDialog._succeed(self, page, row, doc, match_span, next)

        self._replace_button.set_sensitive(True)
