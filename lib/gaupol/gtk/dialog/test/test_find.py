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

from gaupol.gtk             import cons
from gaupol.gtk.icons       import *
from gaupol.gtk.dialog.find import FindDialog
from gaupol.gtk.dialog.find import ReplaceDialog
from gaupol.gtk.dialog.find import _NotFoundInfoDialog
from gaupol.gtk.dialog.find import _ReplaceAllInfoDialog
from gaupol.gtk.error       import Default
from gaupol.gtk.page        import Page
from gaupol.gtk.util        import conf, gtklib
from gaupol.test            import Test


class TestNotFoundInfoDialog(Test):

    def test_run(self):

        gtklib.run(_NotFoundInfoDialog(gtk.Window(), 'test'))


class TestReplaceAllInfoDialog(Test):

    def test_run(self):

        gtklib.run(_ReplaceAllInfoDialog(gtk.Window(), 'test', 'rest', 333))


class TestFindDialog(Test):

    def on_dialog_coordinate_request(self, dialog):

        return self.page, 1, MAIN

    def setup_method(self, method):

        reload(conf)

        self.page = Page()
        self.page.project = self.get_project()
        self.page.init_tab_widget()
        self.page.reload_all()
        self.page.view.select_rows([1, 2, 3])

        self.dialog = FindDialog()
        gtklib.connect(self, 'dialog', 'coordinate-request', False)

    def test_add_pattern(self):

        self.dialog._pattern_entry.set_text('test')
        self.dialog._add_pattern()
        assert conf.find.pattern == 'test'
        assert conf.find.patterns[0] == 'test'

    def test_fail(self):

        self.dialog._pattern_entry.set_text('test')
        self.dialog._fail()

    def test_get_columns(self):

        self.dialog._main_check.set_active(True)
        self.dialog._tran_check.set_active(True)
        cols = self.dialog._get_columns()
        assert cols == [MTXT, TTXT]

    def test_get_documents(self):

        self.dialog._main_check.set_active(True)
        self.dialog._tran_check.set_active(True)
        docs = self.dialog._get_documents(self.page)
        assert docs == [MAIN, TRAN]

    def test_get_flags(self):

        self.dialog._ignore_case_check.set_active(True)
        self.dialog._multiline_check.set_active(True)
        self.dialog._dot_all_check.set_active(True)
        flags = self.dialog._get_flags()
        assert flags == re.IGNORECASE|re.MULTILINE|re.DOTALL

    def test_get_position(self):

        pos = self.dialog._get_position(self.page, 3, TRAN)
        assert pos is None

    def test_get_target(self):

        self.dialog._all_radio.set_active(True)
        target = self.dialog._get_target()
        assert target == cons.Target.ALL

        self.dialog._current_radio.set_active(True)
        target = self.dialog._get_target()
        assert target == cons.Target.CURRENT

    def test_get_text(self):

        text = self.dialog._get_text(self.page, 0, MAIN)
        assert text == self.page.project.main_texts[0]

        text = self.dialog._get_text(self.page, 0, TRAN)
        assert text == self.page.project.tran_texts[0]

    def test_get_wrap(self):

        self.dialog._all_radio.set_active(True)
        wrap = self.dialog._get_wrap()
        assert wrap is False

        self.dialog._current_radio.set_active(True)
        wrap = self.dialog._get_wrap()
        assert wrap is True

        self.dialog._selected_radio.set_active(True)
        wrap = self.dialog._get_wrap()
        assert wrap is True

    def test_prepare(self):

        page, row, doc, pos, docs, wrap = self.dialog._prepare(True)
        assert isinstance(page, Page)
        assert isinstance(row, int)
        assert isinstance(doc, int)
        assert isinstance(pos, int) or pos is None
        assert isinstance(docs, list) or docs is None
        assert isinstance(wrap, bool)

        page, row, doc, pos, docs, wrap = self.dialog._prepare(False)
        assert isinstance(page, Page)
        assert isinstance(row, int)
        assert isinstance(doc, int)
        assert isinstance(pos, int) or pos is None
        assert isinstance(docs, list) or docs is None
        assert isinstance(wrap, bool)

    def test_set_pattern(self):

        self.dialog._pattern_entry.set_text('a')
        self.dialog._set_pattern(self.page)

        self.dialog._pattern_entry.set_text('')
        try:
            self.dialog._set_pattern(self.page)
            raise AssertionError
        except Default:
            pass

    def test_set_text(self):

        self.dialog._set_text(self.page, 0, MAIN, [0, 2])

    def test_close(self):

        self.dialog.close()

    def test_next(self):

        self.dialog._pattern_entry.set_text('a')
        self.dialog.next()

    def test_present(self):

        self.dialog.present()

    def test_previous(self):

        self.dialog._pattern_entry.set_text('a')
        self.dialog.previous()

    def test_show(self):

        self.dialog.show()

    def test_signals(self):

        for name in (
            '_all_radio',
            '_current_radio',
            '_dot_all_check',
            '_ignore_case_check',
            '_main_check',
            '_multiline_check',
            '_regex_check',
            '_tran_check',
        ):
            widget = getattr(self.dialog, name)
            widget.set_active(True)
            widget.set_active(False)
            widget.set_active(True)

        self.dialog._pattern_entry.set_text('a')
        self.dialog._next_button.emit('clicked')
        self.dialog._previous_button.emit('clicked')
        self.dialog._text_view.grab_focus()
        self.dialog._next_button.grab_focus()
        self.dialog._dialog.emit('response', gtk.RESPONSE_CLOSE)


class TestReplaceDialog(TestFindDialog):

    def setup_method(self, method):

        reload(conf)

        self.page = Page()
        self.page.project = self.get_project()
        self.page.init_tab_widget()
        self.page.reload_all()
        self.page.view.select_rows([1, 2, 3])

        self.dialog = ReplaceDialog()
        gtklib.connect(self, 'dialog', 'coordinate-request', False)

    def test_add_replacement(self):

        self.dialog._replacement_entry.set_text('test')
        self.dialog._add_replacement()
        assert conf.find.replacement == 'test'
        assert conf.find.replacements[0] == 'test'

    def test_replace_signals(self):

        self.dialog._pattern_entry.set_text('a')
        self.dialog._replacement_entry.set_text('.')
        self.dialog._next_button.emit('clicked')
        self.dialog._replace_button.emit('clicked')
        self.dialog._replace_button.emit('clicked')
        self.dialog._replace_all_button.emit('clicked')

    def test_set_replacement(self):

        self.dialog._replacement_entry.set_text('a')
        self.dialog._set_replacement(self.page)

        self.dialog._replacement_entry.set_text('')
        try:
            self.dialog._set_replacement(self.page)
            raise AssertionError
        except Default:
            pass
