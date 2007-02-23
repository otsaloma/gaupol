# Copyright (C) 2005-2007 Osmo Salomaa
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


from gaupol.gtk import conf, cons
from gaupol.gtk.index import *
from gaupol.gtk.unittest import TestCase


class TestPage(TestCase):

    def setup_method(self, method):

        self.page = self.get_page()

    def test__get_positions(self):

        self.page.edit_mode = cons.MODE.FRAME
        positions = self.page._get_positions()
        assert positions == self.page.project.frames

        self.page.edit_mode = cons.MODE.TIME
        positions = self.page._get_positions()
        assert positions == self.page.project.times

    def test__init_signal_handlers(self):

        self.page.project.open_main(self.get_subrip_path(), "ascii")
        self.page.project.remove_subtitles([0, 1])
        self.page.project.set_text(0, cons.DOCUMENT.TRAN, "test")

        conf.editor.limit_undo = True
        conf.editor.undo_levels = 10
        conf.editor.limit_undo = False

    def test__init_widgets(self):

        self.page.tab_widget.get_data("button").emit("clicked")

    def test__on_project_main_file_opened(self):

        self.page.project.open_main(self.get_subrip_path(), "ascii")
        self.page.assert_store()

    def test__on_project_main_texts_changed(self):

        self.page.project.set_text(0, cons.DOCUMENT.MAIN, "test")
        self.page.assert_store()

    def test__on_project_positions_changed(self):

        self.page.project.set_position(0, 0, "00:00:00,000")
        self.page.assert_store()

    def test__on_project_subtitles_changed(self):

        self.page.project.set_position(0, 0, "99:59:59,999")
        self.page.assert_store()

    def test__on_project_subtitles_inserted(self):

        self.page.project.insert_blank_subtitles([0, 1])
        self.page.assert_store()

    def test__on_project_subtitles_removed(self):

        self.page.project.remove_subtitles([2, 3])
        self.page.assert_store()

    def test__on_project_translation_file_opened(self):

        path = self.get_subrip_path()
        self.page.project.open_translation(path, "ascii")
        self.page.assert_store()

    def test__on_project_translation_texts_changed(self):

        self.page.project.set_text(0, cons.DOCUMENT.TRAN, "test")
        self.page.assert_store()

    def test_assert_store(self):

        self.page.assert_store()

    def test_document_to_text_column(self):

        assert self.page.document_to_text_column(cons.DOCUMENT.MAIN) == MTXT
        assert self.page.document_to_text_column(cons.DOCUMENT.TRAN) == TTXT

    def test_get_main_basename(self):

        self.page.project.main_file.path = "/tmp/root.srt"
        assert self.page.get_main_basename() == "root.srt"

    def test_get_main_corename(self):

        self.page.project.main_file.path = "/tmp/root.srt"
        assert self.page.get_main_corename() == "root"

    def test_get_translation_basename(self):

        self.page.project.tran_file.path = "/tmp/root.sub"
        assert self.page.get_translation_basename() == "root.sub"

    def test_get_translation_corename(self):

        self.page.project.tran_file.path = "/tmp/root.sub"
        assert self.page.get_translation_corename() == "root"

    def test_reload_view(self):

        rows = range(len(self.page.project.times))
        self.page.reload_view(rows, [SHOW, HIDE, DURN, MTXT, TTXT])
        self.page.assert_store()

    def test_reload_view_all(self):

        self.page.reload_view_all()
        self.page.assert_store()

    def test_text_column_to_document(self):

        assert self.page.text_column_to_document(MTXT) == cons.DOCUMENT.MAIN
        assert self.page.text_column_to_document(TTXT) == cons.DOCUMENT.TRAN

    def test_update_tab_label(self):

        self.page.project.save(cons.DOCUMENT.MAIN)
        self.page.project.save(cons.DOCUMENT.TRAN)
        title = self.page.update_tab_label()
        assert title == self.page.get_main_basename()

        self.page.project.remove_subtitles([1])
        title = self.page.update_tab_label()
        assert title == "*" + self.page.get_main_basename()
