# Copyright (C) 2005-2006 Osmo Salomaa
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


import gtk

from gaupol.gtk         import cons
from gaupol.gtk.colcons import *
from gaupol.gtk.page    import Page
from gaupol.test        import Test


class TestPage(Test):

    def setup_method(self, method):

        self.page = Page()
        self.page.project = self.get_project()
        self.page.init_tab_widget()
        self.page.reload_all()

    def test_get_positions(self):

        self.page.edit_mode = cons.Mode.FRAME
        positions = self.page._get_positions()
        assert positions == self.page.project.frames

        self.page.edit_mode = cons.Mode.TIME
        positions = self.page._get_positions()
        assert positions == self.page.project.times

    def test_assert_store(self):

        self.page.assert_store()

    def test_document_to_text_column(self):

        col = self.page.document_to_text_column(MAIN)
        assert col == MTXT

        col = self.page.document_to_text_column(TRAN)
        assert col == TTXT

    def test_get_names(self):

        self.page.project.main_file.path = '/tmp/root.srt'
        assert self.page.get_main_basename() == 'root.srt'
        assert self.page.get_main_corename() == 'root'
        assert self.page.get_main_filename() == '/tmp/root.srt'

        self.page.project.tran_file.path = '/tmp/root.sub'
        assert self.page.get_translation_basename() == 'root.sub'
        assert self.page.get_translation_corename() == 'root'

    def test_init_tab_widget(self):

        widget = self.page.init_tab_widget()
        assert isinstance(widget, gtk.Widget)

    def test_reload_after(self):

        self.page.project.remove_subtitles([3])
        self.page.reload_after(3)
        self.page.assert_store()

        self.page.project.insert_subtitles([3])
        self.page.reload_after(3)
        self.page.assert_store()

    def test_reload_all(self):

        self.page.reload_all()
        self.page.assert_store()

    def test_reload_columns(self):

        self.page.reload_columns([NUMB])
        self.page.assert_store()

        self.page.project.set_frame(0, 0, 1)
        self.page.reload_columns([SHOW, HIDE, DURN], [0])
        self.page.assert_store()

        self.page.project.set_text(1, MAIN, 'test')
        self.page.project.set_text(2, TRAN, 'test')
        self.page.reload_columns([MTXT, TTXT], [1, 2])
        self.page.assert_store()

    def  test_reload_rows(self):

        self.page.project.set_text(5, TRAN, 'test')
        self.page.reload_rows([5])
        self.page.assert_store()

    def test_text_column_to_document(self):

        doc = self.page.text_column_to_document(MTXT)
        assert doc == MAIN

        doc = self.page.text_column_to_document(TTXT)
        assert doc == TRAN

    def test_update_tab_labels(self):

        self.page.project.save_main_file()
        self.page.project.save_translation_file()
        title = self.page.update_tab_labels()
        assert title == self.page.get_main_basename()

        self.page.project.set_text(1, MAIN, 'test')
        title = self.page.update_tab_labels()
        assert title == '*' + self.page.get_main_basename()
