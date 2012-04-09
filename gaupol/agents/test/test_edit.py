# -*- coding: utf-8-unix -*-

# Copyright (C) 2005-2008,2010 Osmo Salomaa
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

import aeidon
import gaupol
from gi.repository import Gtk


class TestEditAgent(gaupol.TestCase):

    def setup_method(self, method):
        self.application = self.new_application()
        self.delegate = self.application.undo.__self__

    def test_on_clear_texts_activate(self):
        page = self.application.get_current_page()
        page.view.set_focus(0, page.view.columns.MAIN_TEXT)
        page.view.select_rows((0, 1, 2))
        self.application.get_action("clear_texts").activate()

    def test_on_copy_texts_activate(self):
        page = self.application.get_current_page()
        page.view.set_focus(0, page.view.columns.MAIN_TEXT)
        page.view.select_rows((0, 1, 2))
        self.application.get_action("copy_texts").activate()

    def test_on_cut_texts_activate(self):
        page = self.application.get_current_page()
        page.view.set_focus(0, page.view.columns.MAIN_TEXT)
        page.view.select_rows((0, 1, 2))
        self.application.get_action("cut_texts").activate()

    @aeidon.deco.monkey_patch(gaupol.util, "flash_dialog")
    def test_on_edit_headers_activate(self):
        gaupol.util.flash_dialog = lambda *args: Gtk.ResponseType.OK
        path = self.new_temp_file(aeidon.formats.SUBVIEWER2)
        self.application.open_main(path)
        self.application.get_action("edit_headers").activate()

    def test__on_edit_next_value_activate(self):
        page = self.application.get_current_page()
        page.view.set_focus(0, page.view.columns.MAIN_TEXT)
        self.application.get_action("edit_next_value").activate()

    def test_on_edit_preferences_activate(self):
        self.application.get_action("edit_preferences").activate()
        self.application.get_action("edit_preferences").activate()
        self.delegate._pref_dialog.response(Gtk.ResponseType.CLOSE)

    def test__on_edit_value_activate(self):
        page = self.application.get_current_page()
        page.view.set_focus(0, page.view.columns.MAIN_TEXT)
        self.application.get_action("edit_value").activate()

    def test_on_extend_selection_to_beginning_activate(self):
        page = self.application.get_current_page()
        page.view.select_rows((4, 5))
        self.application.get_action("extend_selection_to_beginning").activate()

    def test_on_extend_selection_to_end_activate(self):
        page = self.application.get_current_page()
        page.view.select_rows((4, 5))
        self.application.get_action("extend_selection_to_end").activate()

    @aeidon.deco.monkey_patch(gaupol.util, "flash_dialog")
    def test_on_insert_subtitles_activate(self):
        gaupol.util.flash_dialog = lambda *args: Gtk.ResponseType.OK
        page = self.application.get_current_page()
        page.view.set_focus(0, page.view.columns.MAIN_TEXT)
        self.application.get_action("insert_subtitles").activate()

    def test_on_invert_selection_activate(self):
        self.application.get_action("invert_selection").activate()

    def test_on_merge_subtitles_activate(self):
        page = self.application.get_current_page()
        page.view.set_focus(0, page.view.columns.MAIN_TEXT)
        page.view.select_rows((0, 1))
        self.application.get_action("merge_subtitles").activate()

    def test_on_paste_texts_activate(self):
        page = self.application.get_current_page()
        page.view.set_focus(0, page.view.columns.MAIN_TEXT)
        page.view.select_rows((0, 1, 2))
        self.application.get_action("copy_texts").activate()
        page.view.set_focus(0, page.view.columns.MAIN_TEXT)
        self.application.get_action("paste_texts").activate()

    def test_on_paste_texts_activate__subtitles_added(self):
        page = self.application.get_current_page()
        page.view.set_focus(0, page.view.columns.MAIN_TEXT)
        page.view.select_rows((0, 1, 2))
        self.application.get_action("copy_texts").activate()
        row = len(page.project.subtitles) - 1
        page.view.set_focus(row, page.view.columns.MAIN_TEXT)
        self.application.get_action("paste_texts").activate()

    def test_on_project_action_done(self):
        page = self.application.get_current_page()
        page.project.remove_subtitles((0,))

    def test_on_project_action_redone(self):
        page = self.application.get_current_page()
        page.project.remove_subtitles((0,))
        self.application.undo()
        self.application.redo()

    def test_on_project_action_undone(self):
        page = self.application.get_current_page()
        page.project.remove_subtitles((0,))
        self.application.undo()

    def test_on_redo_action_activate(self):
        page = self.application.get_current_page()
        page.project.remove_subtitles((0,))
        self.application.get_action("undo_action").activate()
        self.application.get_action("redo_action").activate()

    def test_on_remove_subtitles_activate(self):
        page = self.application.get_current_page()
        page.view.select_rows((0, 1, 2))
        self.application.get_action("remove_subtitles").activate()

    def test_on_select_all_activate(self):
        self.application.get_action("select_all").activate()

    def test_on_split_subtitle_activate(self):
        page = self.application.get_current_page()
        page.view.set_focus(0, page.view.columns.MAIN_TEXT)
        self.application.get_action("split_subtitle").activate()

    def test_on_undo_action_activate(self):
        page = self.application.get_current_page()
        page.project.remove_subtitles((0,))
        self.application.get_action("undo_action").activate()

    def test_on_view_renderer_edited__position_frame(self):
        page = self.application.get_current_page()
        self.application.get_action("show_frames").activate()
        for col in filter(page.view.is_position_column, page.view.columns):
            column = page.view.get_column(col)
            renderer = column.get_cells()[0]
            renderer.emit("edited", 1, 0)
            renderer.emit("edited", 1, "k")

    def test_on_view_renderer_edited__position_time(self):
        page = self.application.get_current_page()
        self.application.get_action("show_times").activate()
        for col in filter(page.view.is_position_column, page.view.columns):
            column = page.view.get_column(col)
            renderer = column.get_cells()[0]
            renderer.emit("edited", 1, "00:00:00.000")

    def test_on_view_renderer_edited__text(self):
        page = self.application.get_current_page()
        self.application.get_action("show_times").activate()
        for col in filter(page.view.is_text_column, page.view.columns):
            column = page.view.get_column(col)
            renderer = column.get_cells()[0]
            renderer.emit("edited", 1, "test")

    def test_on_view_renderer_editing_canceled__position(self):
        page = self.application.get_current_page()
        for col in filter(page.view.is_position_column, page.view.columns):
            column = page.view.get_column(col)
            renderer = column.get_cells()[0]
            renderer.emit("editing-canceled")

    def test_on_view_renderer_editing_canceled__text(self):
        page = self.application.get_current_page()
        for col in filter(page.view.is_text_column, page.view.columns):
            column = page.view.get_column(col)
            renderer = column.get_cells()[0]
            renderer.emit("editing-canceled")

    def test_on_view_renderer_editing_started__position(self):
        page = self.application.get_current_page()
        for col in filter(page.view.is_text_column, page.view.columns):
            column = page.view.get_column(col)
            page.view.set_cursor(1, column, True)
            gaupol.util.iterate_main()

    def test_on_view_renderer_editing_started__position(self):
        page = self.application.get_current_page()
        for col in filter(page.view.is_position_column, page.view.columns):
            column = page.view.get_column(col)
            page.view.set_cursor(1, column, True)
            gaupol.util.iterate_main()

    def test_redo(self):
        page = self.application.get_current_page()
        page.project.remove_subtitles((0,))
        self.application.undo()
        self.application.redo()

    def test_undo(self):
        page = self.application.get_current_page()
        page.project.remove_subtitles((0,))
        self.application.undo()
