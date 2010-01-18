# Copyright (C) 2005-2008 Osmo Salomaa
#
# This file is part of Gaupol.
#
# Gaupol is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# Gaupol is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# Gaupol. If not, see <http://www.gnu.org/licenses/>.

import gaupol


class TestPage(gaupol.TestCase):

    def setup_method(self, method):

        self.page = self.new_page()

    def test__on_conf_editor_notify_limit_undo(self):

        gaupol.conf.editor.limit_undo = True
        gaupol.conf.editor.undo_levels = 1
        gaupol.conf.editor.limit_undo = False

    def test__on_conf_editor_notify_undo_levels(self):

        gaupol.conf.editor.limit_undo = True
        gaupol.conf.editor.undo_levels = 1
        gaupol.conf.editor.undo_levels = 100

    def test__on_project_main_file_opened(self):

        path = self.new_subrip_file()
        self.page.project.open_main(path, "ascii")

    def test__on_project_main_texts_changed(self):

        doc = aeidon.documents.MAIN
        self.page.project.set_text(0, doc, "test")

    def test__on_project_positions_changed(self):

        self.page.project.shift_positions(None, 3.0)

    def test__on_project_subtitles_changed(self):

        project = self.page.project
        rows = range(len(self.page.project.subtitles))
        self.page._on_project_subtitles_changed(project, rows)

    def test__on_project_subtitles_inserted(self):

        self.page.project.insert_subtitles((0, 1))

    def test__on_project_subtitles_removed(self):

        self.page.project.remove_subtitles((2, 3))

    def test__on_project_translation_file_opened(self):

        path = self.new_subrip_file()
        self.page.project.open_translation(path, "ascii")

    def test__on_project_translation_texts_changed(self):

        doc = aeidon.documents.TRAN
        self.page.project.set_text(0, doc, "test")

    def test_document_to_text_column(self):

        doc = aeidon.documents.MAIN
        col = self.page.document_to_text_column(doc)
        assert col == self.page.view.columns.MAIN_TEXT
        doc = aeidon.documents.TRAN
        col = self.page.document_to_text_column(doc)
        assert col == self.page.view.columns.TRAN_TEXT
        function = self.page.document_to_text_column
        self.raises(ValueError, function, None)

    def test_get_main_basename(self):

        self.page.project.main_file.path = "/tmp/root.srt"
        name = self.page.get_main_basename()
        assert name == "root.srt"
        self.page.project.main_file = None
        name = self.page.get_main_basename()
        assert name == self.page.untitle

    def test_get_translation_basename(self):

        translate = aeidon.i18n._
        self.page.project.tran_file.path = "/tmp/root.sub"
        name = self.page.get_translation_basename()
        assert name == "root.sub"
        self.page.project.main_file.path = "/tmp/root.srt"
        self.page.project.tran_file = None
        name = self.page.get_translation_basename()
        assert name == translate("%s translation") % "root"
        self.page.project.main_file = None
        name = self.page.get_translation_basename()
        assert name == translate("%s translation") % self.page.untitle

    def test_reload_view(self):

        rows = range(len(self.page.project.subtitles))
        fields = [x for x in gaupol.fields]
        fields.remove(gaupol.fields.NUMBER)
        self.page.reload_view(rows, fields)

    def test_reload_view_all(self):

        self.page.reload_view_all()

    def test_text_column_to_document(self):

        col = self.page.view.columns.MAIN_TEXT
        doc = self.page.text_column_to_document(col)
        assert doc == aeidon.documents.MAIN
        col = self.page.view.columns.TRAN_TEXT
        doc = self.page.text_column_to_document(col)
        assert doc == aeidon.documents.TRAN
        function = self.page.text_column_to_document
        self.raises(ValueError, function, None)

    def test_update_tab_label(self):

        title = self.page.update_tab_label()
        assert title == self.page.get_main_basename()
        self.page.project.remove_subtitles([1])
        title = self.page.update_tab_label()
        assert title == "*%s" % self.page.get_main_basename()
