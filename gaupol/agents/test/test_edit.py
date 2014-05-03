# -*- coding: utf-8 -*-

# Copyright (C) 2005-2008,2010,2013 Osmo Salomaa
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

import aeidon
import gaupol

from gi.repository import Gtk


class TestEditAgent(gaupol.TestCase):

    def setup_method(self, method):
        self.application = self.new_application()
        self.delegate = self.application.undo.__self__

    def test__on_clear_texts_activate(self):
        page = self.application.get_current_page()
        page.view.set_focus(0, page.view.columns.MAIN_TEXT)
        page.view.select_rows((0, 1, 2))
        self.application.get_action("clear_texts").activate()

    def test__on_copy_texts_activate(self):
        page = self.application.get_current_page()
        page.view.set_focus(0, page.view.columns.MAIN_TEXT)
        page.view.select_rows((0, 1, 2))
        self.application.get_action("copy_texts").activate()

    def test__on_cut_texts_activate(self):
        page = self.application.get_current_page()
        page.view.set_focus(0, page.view.columns.MAIN_TEXT)
        page.view.select_rows((0, 1, 2))
        self.application.get_action("cut_texts").activate()

    @aeidon.deco.monkey_patch(gaupol.util, "flash_dialog")
    def test__on_edit_headers_activate(self):
        gaupol.util.flash_dialog = lambda *args: Gtk.ResponseType.OK
        path = self.new_temp_file(aeidon.formats.SUBVIEWER2)
        self.application.open_main(path)
        self.application.get_action("edit_headers").activate()

    def test__on_edit_next_value_activate(self):
        page = self.application.get_current_page()
        page.view.set_focus(0, page.view.columns.MAIN_TEXT)
        self.application.get_action("edit_next_value").activate()

    def test__on_edit_preferences_activate(self):
        self.application.get_action("edit_preferences").activate()
        self.application.get_action("edit_preferences").activate()
        self.delegate._pref_dialog.response(Gtk.ResponseType.CLOSE)

    def test__on_edit_value_activate(self):
        page = self.application.get_current_page()
        page.view.set_focus(0, page.view.columns.MAIN_TEXT)
        self.application.get_action("edit_value").activate()

    def test__on_end_earlier_activate(self):
        self.application.get_action("end_earlier").activate()
        self.application.get_action("end_earlier").activate()
        self.application.get_action("end_earlier").activate()

    def test__on_end_later_activate(self):
        self.application.get_action("end_later").activate()
        self.application.get_action("end_later").activate()
        self.application.get_action("end_later").activate()

    def test__on_extend_selection_to_beginning_activate(self):
        page = self.application.get_current_page()
        page.view.select_rows((4, 5))
        self.application.get_action("extend_selection_to_beginning").activate()

    def test__on_extend_selection_to_end_activate(self):
        page = self.application.get_current_page()
        page.view.select_rows((4, 5))
        self.application.get_action("extend_selection_to_end").activate()

    @aeidon.deco.monkey_patch(gaupol.util, "flash_dialog")
    def test__on_insert_subtitles_activate(self):
        gaupol.util.flash_dialog = lambda *args: Gtk.ResponseType.OK
        page = self.application.get_current_page()
        page.view.set_focus(0, page.view.columns.MAIN_TEXT)
        self.application.get_action("insert_subtitles").activate()

    def test__on_invert_selection_activate(self):
        self.application.get_action("invert_selection").activate()
        self.application.get_action("invert_selection").activate()

    def test__on_merge_subtitles_activate(self):
        page = self.application.get_current_page()
        page.view.set_focus(0, page.view.columns.MAIN_TEXT)
        page.view.select_rows((0, 1))
        self.application.get_action("merge_subtitles").activate()

    def test__on_paste_texts_activate(self):
        page = self.application.get_current_page()
        page.view.set_focus(0, page.view.columns.MAIN_TEXT)
        page.view.select_rows((0, 1, 2))
        self.application.get_action("copy_texts").activate()
        page.view.set_focus(0, page.view.columns.MAIN_TEXT)
        self.application.get_action("paste_texts").activate()

    def test__on_paste_texts_activate__subtitles_added(self):
        page = self.application.get_current_page()
        page.view.set_focus(0, page.view.columns.MAIN_TEXT)
        page.view.select_rows((0, 1, 2))
        self.application.get_action("copy_texts").activate()
        row = len(page.project.subtitles) - 1
        page.view.set_focus(row, page.view.columns.MAIN_TEXT)
        self.application.get_action("paste_texts").activate()

    def test__on_project_action_done(self):
        page = self.application.get_current_page()
        page.project.remove_subtitles((0,))

    def test__on_project_action_redone(self):
        page = self.application.get_current_page()
        page.project.remove_subtitles((0,))
        self.application.undo()
        self.application.redo()

    def test__on_project_action_undone(self):
        page = self.application.get_current_page()
        page.project.remove_subtitles((0,))
        self.application.undo()

    def test__on_redo_action_activate(self):
        page = self.application.get_current_page()
        page.project.remove_subtitles((0,))
        self.application.get_action("undo_action").activate()
        self.application.get_action("redo_action").activate()

    def test__on_remove_subtitles_activate(self):
        page = self.application.get_current_page()
        page.view.select_rows((0, 1, 2))
        self.application.get_action("remove_subtitles").activate()

    def test__on_select_all_activate(self):
        self.application.get_action("select_all").activate()

    def test__on_split_subtitle_activate(self):
        page = self.application.get_current_page()
        page.view.set_focus(0, page.view.columns.MAIN_TEXT)
        self.application.get_action("split_subtitle").activate()

    def test__on_start_earlier_activate(self):
        self.application.get_action("start_earlier").activate()
        self.application.get_action("start_earlier").activate()
        self.application.get_action("start_earlier").activate()

    def test__on_start_later_activate(self):
        self.application.get_action("start_later").activate()
        self.application.get_action("start_later").activate()
        self.application.get_action("start_later").activate()

    def test__on_undo_action_activate(self):
        page = self.application.get_current_page()
        page.project.remove_subtitles((0,))
        self.application.get_action("undo_action").activate()

    def test__on_view_renderer_edited__position_frame(self):
        page = self.application.get_current_page()
        self.application.get_action("show_frames").activate()
        for col in filter(page.view.is_position_column, page.view.columns):
            column = page.view.get_column(col)
            renderer = column.get_cells()[0]
            renderer.emit("edited", 1, 0)
            renderer.emit("edited", 1, "xxx")

    def test__on_view_renderer_edited__position_time(self):
        page = self.application.get_current_page()
        self.application.get_action("show_times").activate()
        for col in filter(page.view.is_position_column, page.view.columns):
            column = page.view.get_column(col)
            renderer = column.get_cells()[0]
            renderer.emit("edited", 1, "00:00:00.000")

    def test__on_view_renderer_edited__text(self):
        page = self.application.get_current_page()
        self.application.get_action("show_times").activate()
        for col in filter(page.view.is_text_column, page.view.columns):
            column = page.view.get_column(col)
            renderer = column.get_cells()[0]
            renderer.emit("edited", 1, "test")

    def test__on_view_renderer_editing_canceled__position(self):
        page = self.application.get_current_page()
        for col in filter(page.view.is_position_column, page.view.columns):
            column = page.view.get_column(col)
            renderer = column.get_cells()[0]
            renderer.emit("editing-canceled")

    def test__on_view_renderer_editing_canceled__text(self):
        page = self.application.get_current_page()
        for col in filter(page.view.is_text_column, page.view.columns):
            column = page.view.get_column(col)
            renderer = column.get_cells()[0]
            renderer.emit("editing-canceled")

    def test__on_view_renderer_editing_started__position(self):
        page = self.application.get_current_page()
        for col in filter(page.view.is_position_column, page.view.columns):
            column = page.view.get_column(col)
            page.view.set_cursor(1, column, True)
            gaupol.util.iterate_main()

    def test__on_view_renderer_editing_started__text(self):
        page = self.application.get_current_page()
        for col in filter(page.view.is_text_column, page.view.columns):
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
