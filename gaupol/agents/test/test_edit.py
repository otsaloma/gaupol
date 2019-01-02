# -*- coding: utf-8 -*-

# Copyright (C) 2005 Osmo Salomaa
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

import gaupol

from gi.repository import Gtk
from unittest.mock import patch


class TestEditAgent(gaupol.TestCase):

    def setup_method(self, method):
        self.application = self.new_application()

    def test__on_clear_texts_activate(self):
        page = self.application.get_current_page()
        page.view.set_focus(0, page.view.columns.MAIN_TEXT)
        page.view.select_rows((0,1,2))
        self.application.get_action("clear-texts").activate()

    def test__on_copy_texts_activate(self):
        page = self.application.get_current_page()
        page.view.set_focus(0, page.view.columns.MAIN_TEXT)
        page.view.select_rows((0,1,2))
        self.application.get_action("copy-texts").activate()

    def test__on_cut_texts_activate(self):
        page = self.application.get_current_page()
        page.view.set_focus(0, page.view.columns.MAIN_TEXT)
        page.view.select_rows((0,1,2))
        self.application.get_action("cut-texts").activate()
        assert page.project.subtitles[0].main_text == ""
        assert page.project.subtitles[1].main_text == ""
        assert page.project.subtitles[2].main_text == ""

    def test__on_edit_next_value_activate(self):
        page = self.application.get_current_page()
        page.view.set_focus(0, page.view.columns.MAIN_TEXT)
        self.application.get_action("edit-next-value").activate()

    def test__on_edit_preferences_activate(self):
        self.application.get_action("edit-preferences").activate()
        self.application.get_action("edit-preferences").activate()

    def test__on_edit_value_activate(self):
        page = self.application.get_current_page()
        page.view.set_focus(0, page.view.columns.MAIN_TEXT)
        self.application.get_action("edit-value").activate()

    def test__on_end_earlier_activate(self):
        self.application.get_action("end-earlier").activate()
        self.application.get_action("end-earlier").activate()
        self.application.get_action("end-earlier").activate()

    def test__on_end_later_activate(self):
        self.application.get_action("end-later").activate()
        self.application.get_action("end-later").activate()
        self.application.get_action("end-later").activate()

    def test__on_extend_selection_to_beginning_activate(self):
        page = self.application.get_current_page()
        page.view.select_rows((4,5))
        self.application.get_action("extend-selection-to-beginning").activate()
        rows = page.view.get_selected_rows()
        assert rows == tuple(range(0, 6))

    def test__on_extend_selection_to_end_activate(self):
        page = self.application.get_current_page()
        page.view.select_rows((4,5))
        self.application.get_action("extend-selection-to-end").activate()
        rows = page.view.get_selected_rows()
        assert rows == tuple(range(4, len(page.project.subtitles)))

    @patch("gaupol.util.flash_dialog", lambda *args: Gtk.ResponseType.OK)
    def test__on_insert_subtitles_activate(self):
        page = self.application.get_current_page()
        page.view.set_focus(0, page.view.columns.MAIN_TEXT)
        self.application.get_action("insert-subtitles").activate()

    def test__on_invert_selection_activate(self):
        page = self.application.get_current_page()
        page.view.select_rows((0,1,2))
        self.application.get_action("invert-selection").activate()
        rows = page.view.get_selected_rows()
        assert rows == tuple(range(3, len(page.project.subtitles)))
        self.application.get_action("invert-selection").activate()
        rows = page.view.get_selected_rows()
        assert rows == (0,1,2)

    def test__on_merge_subtitles_activate(self):
        page = self.application.get_current_page()
        n = len(page.project.subtitles)
        page.view.set_focus(0, page.view.columns.MAIN_TEXT)
        page.view.select_rows((0,1))
        self.application.get_action("merge-subtitles").activate()
        assert len(page.project.subtitles) == n-1

    def test__on_paste_texts_activate(self):
        page = self.application.get_current_page()
        page.view.set_focus(0, page.view.columns.MAIN_TEXT)
        page.view.select_rows((0,1,2))
        self.application.get_action("copy-texts").activate()
        page.view.set_focus(0, page.view.columns.MAIN_TEXT)
        self.application.get_action("paste-texts").activate()

    def test__on_redo_action_activate(self):
        page = self.application.get_current_page()
        n = len(page.project.subtitles)
        page.project.remove_subtitles((0,))
        self.application.get_action("undo-action").activate()
        self.application.get_action("redo-action").activate()
        assert len(page.project.subtitles) == n-1

    def test__on_remove_subtitles_activate(self):
        page = self.application.get_current_page()
        n = len(page.project.subtitles)
        page.view.select_rows((0,1,2))
        self.application.get_action("remove-subtitles").activate()
        assert len(page.project.subtitles) == n-3

    def test__on_select_all_activate(self):
        page = self.application.get_current_page()
        self.application.get_action("select-all").activate()
        rows = page.view.get_selected_rows()
        assert rows == tuple(range(0, len(page.project.subtitles)))

    def test__on_split_subtitle_activate(self):
        page = self.application.get_current_page()
        n = len(page.project.subtitles)
        page.view.set_focus(0, page.view.columns.MAIN_TEXT)
        self.application.get_action("split-subtitle").activate()
        assert len(page.project.subtitles) == n + 1

    def test__on_start_earlier_activate(self):
        self.application.get_action("start-earlier").activate()
        self.application.get_action("start-earlier").activate()
        self.application.get_action("start-earlier").activate()

    def test__on_start_later_activate(self):
        self.application.get_action("start-later").activate()
        self.application.get_action("start-later").activate()
        self.application.get_action("start-later").activate()

    def test__on_undo_action_activate(self):
        page = self.application.get_current_page()
        n = len(page.project.subtitles)
        page.project.remove_subtitles((0,))
        self.application.get_action("undo-action").activate()
        assert len(page.project.subtitles) == n

    def test_redo(self):
        page = self.application.get_current_page()
        n = len(page.project.subtitles)
        page.project.remove_subtitles((0,))
        self.application.undo()
        self.application.redo()
        assert len(page.project.subtitles) == n-1

    def test_undo(self):
        page = self.application.get_current_page()
        n = len(page.project.subtitles)
        page.project.remove_subtitles((0,))
        self.application.undo()
        assert len(page.project.subtitles) == n
