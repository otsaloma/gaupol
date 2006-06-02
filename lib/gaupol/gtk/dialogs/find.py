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


import re

import gtk
import gobject

from gaupol.gtk.colcons import *
from gaupol.base.util        import listlib, wwwlib
from gaupol.gtk.cons import *
from gaupol.gtk.util         import config, gtklib
from gaupol.gtk.dialogs.message import InfoDialog


class NotFoundDialog(InfoDialog):

    def __init__(self, parent, pattern):

        InfoDialog.__init__(self, parent, 'Boohoo', pattern)


class FindDialog(gobject.GObject):

    __gsignals__ = {
        'destroyed': (
            gobject.SIGNAL_RUN_LAST,
            None,
            ()
        ),
    }

    def __init__(self, parent, app):

        gobject.GObject.__init__(self)

        widgets = (
            'col_main_check',
            'col_tran_check',
            'dialog',
            'dot_all_check',
            'ignore_case_check',
            'multiline_check',
            'next_button',
            'pattern_combo',
            'previous_button',
            'prj_all_radio',
            'prj_current_radio',
            'regex_check',
            'text_view',
        )
        glade_xml = gtklib.get_glade_xml('find-dialog')
        for name in widgets:
            setattr(self, '_' + name, glade_xml.get_widget(name))

        self._pattern_entry = self._pattern_combo.child

        self._get_current_page = app.get_current_page
        self._get_next_page    = app.get_next_page
        self._get_page_count   = app.get_page_count
        self._set_active_page  = app.set_active_page

        self._page = None
        self._row  = None
        self._doc  = None

        self._misses = 0

        self._init_signals()
        self._init_data()
        self._init_fonts()
        self._init_sizes()

        self._dialog.set_transient_for(parent)
        self._dialog.set_default_response(gtk.RESPONSE_CLOSE)

    def _init_data(self):
        """Initialize default values."""

        self._prj_all_radio.set_active(config.Find.all_projects)
        self._col_main_check.set_active(config.Find.main_col)
        self._col_tran_check.set_active(config.Find.tran_col)

        self._dot_all_check.set_active(config.Find.dot_all)
        self._ignore_case_check.set_active(config.Find.ignore_case)
        self._multiline_check.set_active(config.Find.multiline)
        self._regex_check.set_active(config.Find.regex)

        self._pattern_entry.set_text(config.Find.pattern)
        self._set_patterns()
        self._set_action_sensitivities()
        self._set_option_sensitivities()

    def _init_fonts(self):
        """Initialize fonts."""

        if not config.Editor.use_default_font:
            gtklib.set_widget_font(self._text_view    , config.Editor.font)
            gtklib.set_widget_font(self._pattern_entry, config.Editor.font)

    def _init_signals(self):
        """Initialize signals."""

        connections = (
            ('_col_main_check'   , 'toggled'        ),
            ('_col_tran_check'   , 'toggled'        ),
            ('_dialog'           , 'response'       ),
            ('_dot_all_check'    , 'toggled'        ),
            ('_ignore_case_check', 'toggled'        ),
            ('_multiline_check'  , 'toggled'        ),
            ('_next_button'      , 'clicked'        ),
            ('_pattern_entry'    , 'changed'        ),
            ('_previous_button'  , 'clicked'        ),
            ('_prj_all_radio'    , 'toggled'        ),
            ('_regex_check'      , 'toggled'        ),
            ('_text_view'        , 'focus-out-event'),
        )

        for widget, signal in connections:
            method = '_on%s_%s' % (widget, signal.replace('-', '_'))
            method = getattr(self, method)
            widget = getattr(self, widget)
            widget.connect(signal, method)

    def _init_sizes(self):
        """Initialize widget sizes."""

        # Set text view width to 46 ex and height to 4 lines.
        label = gtk.Label('\n'.join(['x' * 46] * 4))
        if not config.Editor.use_default_font:
            gtklib.set_label_font(label, config.Editor.font)
        width, height = label.size_request()
        self._text_view.set_size_request(width + 4, height + 7)

    def destroy(self):
        """Destroy the dialog."""

        self._dialog.destroy()

    def _get_documents(self):

        docs = []
        if config.Find.main_col:
            docs.append(Document.MAIN)
        if config.Find.tran_col:
            docs.append(Document.TRAN)

        return docs

    def _get_flags(self):

        flags = 0
        if config.Find.dot_all:
            flags = flags|re.DOTALL
        if config.Find.ignore_case:
            flags = flags|re.IGNORECASE
        if config.Find.multiline:
            flags = flags|re.MULTILINE

        return flags

    def _on_col_main_check_toggled(self, check_button):

        config.Find.main_col = check_button.get_active()

    def _on_col_tran_check_toggled(self, check_button):

        config.Find.tran_col = check_button.get_active()

    def _on_dialog_response(self, dialog, response):

        if response == gtk.RESPONSE_HELP:
            wwwlib.browse_url('http://docs.python.org/lib/re-syntax.html')
            return

        self.emit('destroyed')

    def _on_dot_all_check_toggled(self, check_button):

        config.Find.dot_all = check_button.get_active()

    def _on_ignore_case_check_toggled(self, check_button):

        config.Find.ignore_case = check_button.get_active()

    def _on_multiline_check_toggled(self, check_button):

        config.Find.multiline = check_button.get_active()

    def _on_next_button_clicked(self, *args):

        page = self._get_current_page()
        try:
            row = page.view.get_selected_rows()[0]
        except IndexError:
            row = 0
        col = page.view.get_focus()[1]
        if not col in (MTXT, TTXT):
            col = MTXT
        doc = page.text_column_to_document(col)

        pos = 0
        if page == self._page and row == self._row and doc == self._doc:
            text_buffer = self._text_view.get_buffer()
            bounds = text_buffer.get_selection_bounds()
            if bounds:
                pos = bounds[1].get_offset()
            else:
                mark = text_buffer.get_insert()
                pos = text_buffer.get_iter_at_mark(mark).get_offset()

        regex = self._regex_check.get_active()
        pattern = self._pattern_entry.get_text()

        config.Find.pattern = pattern
        config.Find.patterns.insert(0, pattern)
        config.Find.patterns = listlib.unique(config.Find.patterns)
        while len(config.Find.patterns) > 10:
            config.Find.patterns.pop()
        self._set_patterns()

        page.project.set_find_wrap(not config.Find.all_projects)
        if regex:
            page.project.set_find_regex(pattern, self._get_flags())
        else:
            page.project.set_find_string(pattern, config.Find.ignore_case)

        #print '-----'
        #print 'Page:', page
        #print 'Row:', row
        #print 'Doc:', doc
        #print 'Pos:', pos

        docs = self._get_documents()
        try:
            row, doc, match_span = page.project.find_next(row, doc, docs, pos)
        except StopIteration:
            self._misses += 1
            #print 'Misses:', self._misses
            if self._misses < self._get_page_count():
                page = self._get_next_page()
                # FIX: more elegant way of starting from row 0.
                page.view.select_rows([0])
                self._set_active_page(page)
                self._row  = 0
                self._doc  = docs[0]
                return self._on_next_button_clicked()
            self._misses = 0
            dialog = NotFoundDialog(self._dialog, pattern)
            dialog.run()
            dialog.destroy()
            return

        if doc == Document.MAIN:
            text = page.project.main_texts[row]
        elif doc == Document.TRAN:
            text = page.project.tran_texts[row]

        text_buffer = self._text_view.get_buffer()
        text_buffer.set_text(text)
        ins = text_buffer.get_iter_at_offset(match_span[0])
        bound = text_buffer.get_iter_at_offset(match_span[1])
        text_buffer.select_range(ins, bound)
        self._text_view.grab_focus()

        self._misses = 0
        self._page = page
        self._row  = row
        self._doc  = doc

        col = page.document_to_text_column(doc)
        page.view.set_focus(row, col)
        page.view.scroll_to_row(row)

    def _on_pattern_entry_changed(self, *args):

        self._set_action_sensitivities()

    def _on_previous_button_clicked(self, *args): pass

    def _on_prj_all_radio_toggled(self, radio_button):

        config.Find.all_projects = radio_button.get_active()

    def _on_regex_check_toggled(self, check_button):

        config.Find.regex = check_button.get_active()
        self._set_option_sensitivities()

    def _on_text_view_focus_out_event(self, *args):

        pass

    def present(self):
        """Present the dialog."""

        self._pattern_entry.select_region(0, -1)
        self._pattern_entry.grab_focus()
        self._dialog.present()

    def _set_action_sensitivities(self):

        sensitive = bool(self._pattern_entry.get_text())
        if self._get_current_page() is None:
            sensitive = False

        self._next_button.set_sensitive(sensitive)
        self._previous_button.set_sensitive(sensitive)

    def _set_option_sensitivities(self):

        sensitive = config.Find.regex
        self._dot_all_check.set_sensitive(sensitive)
        self._multiline_check.set_sensitive(sensitive)
        self._dialog.set_response_sensitive(gtk.RESPONSE_HELP, sensitive)

    def _set_patterns(self):

        store = self._pattern_combo.get_model()
        store.clear()
        for pattern in config.Find.patterns:
            store.append([pattern])

    def show(self):
        """Show the dialog."""

        self._pattern_entry.select_region(0, -1)
        self._pattern_entry.grab_focus()
        self._dialog.show()


if __name__ == '__main__':

    from gaupol.test import Test

    class TestFindDialog(Test):

        pass

    TestFindDialog().run()
