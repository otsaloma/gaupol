# Copyright (C) 2005-2007 Osmo Salomaa
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
# A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# Gaupol.  If not, see <http://www.gnu.org/licenses/>.

import gaupol.gtk

from gaupol.gtk import unittest


class TestPage(unittest.TestCase):

    def setup_method(self, method):

        self.page = self.get_page()

    def test__assert_store(self):

        self.page._assert_store()

    def test__on_project_main_file_opened(self):

        path = self.get_subrip_path()
        self.page.project.open_main(path, "ascii")

    def test__on_project_main_texts_changed(self):

        self.page.project.set_text(0, gaupol.gtk.DOCUMENT.MAIN, "test")

    def test__on_project_positions_changed(self):

        self.page.project.set_start(0, "00:00:00,000")

    def test__on_project_subtitles_changed(self):

        self.page.project.set_start(0, "99:59:59,999")

    def test__on_project_subtitles_inserted(self):

        self.page.project.insert_blank_subtitles([0, 1])

    def test__on_project_subtitles_removed(self):

        self.page.project.remove_subtitles([2, 3])

    def test__on_project_translation_file_opened(self):

        path = self.get_subrip_path()
        self.page.project.open_translation(path, "ascii")

    def test__on_project_translation_texts_changed(self):

        self.page.project.set_text(0, gaupol.gtk.DOCUMENT.TRAN, "test")

    def test__on_tab_event_box_enter_notify_event(self):

        self.page._on_tab_event_box_enter_notify_event()

    def test_get_main_basename(self):

        self.page.project.main_file.path = "/tmp/root.srt"
        name = self.page.get_main_basename()
        assert name == "root.srt"
        self.page.project.main_file = None
        name = self.page.get_main_basename()
        assert name == self.page.untitle

    def test_get_translation_basename(self):

        self.page.project.tran_file.path = "/tmp/root.sub"
        name = self.page.get_translation_basename()
        assert name == "root.sub"
        self.page.project.main_file.path = "/tmp/root.srt"
        self.page.project.tran_file = None
        name = self.page.get_translation_basename()
        assert name == "root translation"
        self.page.project.main_file = None
        name = self.page.get_translation_basename()
        assert name == "%s translation" % self.page.untitle

    def test_reload_view(self):

        rows = range(len(self.page.project.subtitles))
        cols = gaupol.gtk.COLUMN.members[:]
        cols.remove(gaupol.gtk.COLUMN.NUMBER)
        self.page.reload_view(rows, cols)

    def test_reload_view_all(self):

        self.page.reload_view_all()

    def test_update_tab_label(self):

        title = self.page.update_tab_label()
        assert title == self.page.get_main_basename()
        self.page.project.remove_subtitles([1])
        title = self.page.update_tab_label()
        assert title == "*" + self.page.get_main_basename()
