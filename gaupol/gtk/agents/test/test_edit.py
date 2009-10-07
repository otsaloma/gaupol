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

import gaupol.gtk
import gtk


class TestEditAgent(gaupol.gtk.TestCase):

    def setup_method(self, method):

        self.application = self.get_application()
        self.delegate = self.application.undo.im_self

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

    def test_on_edit_headers_activate(self):

        path = self.new_temp_file(gaupol.formats.SUBVIEWER2)
        self.application.open_main_file(path)
        respond = lambda *args: gtk.RESPONSE_OK
        self.application.flash_dialog = respond
        self.application.get_action("edit_headers").activate()

    def test_on_edit_preferences_activate(self):

        self.application.get_action("edit_preferences").activate()
        self.application.get_action("edit_preferences").activate()
        self.delegate._pref_dialog.response(gtk.RESPONSE_CLOSE)

    def test_on_extend_selection_to_beginning_activate(self):

        page = self.application.get_current_page()
        page.view.select_rows((4, 5))
        self.application.get_action("extend_selection_to_beginning").activate()

    def test_on_extend_selection_to_end_activate(self):

        page = self.application.get_current_page()
        page.view.select_rows((4, 5))
        self.application.get_action("extend_selection_to_end").activate()

    def test_on_insert_subtitles_activate(self):

        respond = lambda *args: gtk.RESPONSE_OK
        self.application.flash_dialog = respond
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

    def test_on_view_renderer_edited(self):

        page = self.application.get_current_page()
        self.application.get_action("show_times").activate()
        columns = page.view.columns
        for col in filter(page.view.is_position_column, columns):
            column = page.view.get_column(col)
            renderer = column.get_cell_renderers()[0]
            renderer.emit("edited", 1, "00:00:00.000")
        self.application.get_action("show_frames").activate()
        columns = page.view.columns
        for col in filter(page.view.is_position_column, columns):
            column = page.view.get_column(col)
            renderer = column.get_cell_renderers()[0]
            renderer.emit("edited", 1, 0)
            renderer.emit("edited", 1, "k")
        for col in filter(page.view.is_text_column, columns):
            column = page.view.get_column(col)
            renderer = column.get_cell_renderers()[0]
            renderer.emit("edited", 1, "test")

    def test_on_view_renderer_editing_canceled(self):

        page = self.application.get_current_page()
        columns = page.view.columns
        for col in filter(page.view.is_position_column, columns):
            column = page.view.get_column(col)
            renderer = column.get_cell_renderers()[0]
            renderer.emit("editing-canceled")
        for col in filter(page.view.is_text_column, columns):
            column = page.view.get_column(col)
            renderer = column.get_cell_renderers()[0]
            renderer.emit("editing-canceled")

    def test_on_view_renderer_editing_started(self):

        page = self.application.get_current_page()
        columns = page.view.columns
        for col in filter(page.view.is_position_column, columns):
            column = page.view.get_column(col)
            page.view.set_cursor(1, column, True)
            gaupol.gtk.util.iterate_main()
        for col in filter(page.view.is_text_column, columns):
            column = page.view.get_column(col)
            page.view.set_cursor(1, column, True)
            gaupol.gtk.util.iterate_main()

    def test_redo(self):

        page = self.application.get_current_page()
        page.project.remove_subtitles((0,))
        self.application.undo()
        self.application.redo()

    def test_undo(self):

        page = self.application.get_current_page()
        page.project.remove_subtitles((0,))
        self.application.undo()
