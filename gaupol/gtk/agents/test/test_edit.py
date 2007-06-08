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


import gtk

from gaupol.gtk import const
from gaupol.gtk.index import *
from gaupol.gtk import unittest


class TestEditAgent(unittest.TestCase):

    def setup_method(self, method):

        self.application = self.get_application()
        self.delegate = self.application.undo.im_self

    def test_on_clear_texts_activate(self):

        page = self.application.get_current_page()
        page.view.set_focus(0, gaupol.gtk.COLUMN.MAIN_TEXT)
        page.view.select_rows([0, 1, 2])
        self.application.on_clear_texts_activate()

    def test_on_copy_texts_activate(self):

        page = self.application.get_current_page()
        page.view.set_focus(0, gaupol.gtk.COLUMN.MAIN_TEXT)
        page.view.select_rows([0, 1, 2])
        self.application.on_copy_texts_activate()

    def test_on_cut_texts_activate(self):

        page = self.application.get_current_page()
        page.view.set_focus(0, gaupol.gtk.COLUMN.MAIN_TEXT)
        page.view.select_rows([0, 1, 2])
        self.application.on_cut_texts_activate()

    def test_on_edit_headers_activate(self):

        page = self.application.get_current_page()
        page.project.save(gaupol.gtk.DOCUMENT.MAIN, (
            page.project.main_file.path,
            gaupol.gtk.FORMAT.SUBVIEWER2,
            "ascii",
            page.project.main_file.newline))

        responder = iter((gtk.RESPONSE_OK, gtk.RESPONSE_CANCEL))
        respond = lambda *args: responder.next()
        self.application.flash_dialog = respond
        self.application.on_edit_headers_activate()
        self.application.on_edit_headers_activate()

    def test_on_edit_next_value_activate(self):

        page = self.application.get_current_page()
        page.view.set_focus(0, SHOW)
        self.application.on_edit_next_value_activate()
        page.view.set_focus(0, gaupol.gtk.COLUMN.MAIN_TEXT)
        self.application.on_edit_next_value_activate()

    def test_on_edit_preferences_activate(self):

        self.application.on_edit_preferences_activate()
        self.delegate._on_pref_dialog_response()

    def test_on_edit_value_activate(self):

        page = self.application.get_current_page()
        page.view.set_focus(0, SHOW)
        self.application.on_edit_value_activate()
        page.view.set_focus(0, gaupol.gtk.COLUMN.MAIN_TEXT)
        self.application.on_edit_value_activate()

    def test_on_insert_subtitles_activate(self):

        responder = iter((gtk.RESPONSE_OK, gtk.RESPONSE_CANCEL))
        respond = lambda *args: responder.next()
        self.application.flash_dialog = respond
        self.application.on_insert_subtitles_activate()
        self.application.on_insert_subtitles_activate()

    def test_on_invert_selection_activate(self):

        self.application.on_invert_selection_activate()

    def test_on_merge_subtitles_activate(self):

        page = self.application.get_current_page()
        page.view.set_focus(0, gaupol.gtk.COLUMN.MAIN_TEXT)
        page.view.select_rows([0, 1])
        self.application.on_merge_subtitles_activate()

    def test_on_paste_texts_activate(self):

        page = self.application.get_current_page()
        page.view.set_focus(0, gaupol.gtk.COLUMN.MAIN_TEXT)
        page.view.select_rows([0, 1, 2])
        self.application.on_copy_texts_activate()

        page.view.set_focus(0, gaupol.gtk.COLUMN.MAIN_TEXT)
        self.application.on_paste_texts_activate()
        page.view.set_focus(len(page.project.times) - 1, gaupol.gtk.COLUMN.MAIN_TEXT)
        self.application.on_paste_texts_activate()

    def test_on_project_action_done(self):

        page = self.application.get_current_page()
        page.project.remove_subtitles([0])

    def test_on_project_action_redone(self):

        page = self.application.get_current_page()
        page.project.remove_subtitles([0])
        self.application.undo()
        self.application.redo()

    def test_on_project_action_undone(self):

        page = self.application.get_current_page()
        page.project.remove_subtitles([0])
        self.application.undo()

    def test_on_redo_action_activate(self):

        page = self.application.get_current_page()
        page.project.remove_subtitles([0])
        self.application.on_undo_action_activate()
        self.application.on_redo_action_activate()

    def test_on_redo_button_clicked(self):

        page = self.application.get_current_page()
        page.project.remove_subtitles([0])
        self.application.on_undo_button_clicked()
        self.application.on_redo_button_clicked()

    def test_on_remove_subtitles_activate(self):

        page = self.application.get_current_page()
        page.view.select_rows([0, 1, 2])
        self.application.on_remove_subtitles_activate()

    def test_on_select_all_activate(self):

        self.application.on_select_all_activate()

    def test_on_split_subtitle_activate(self):

        page = self.application.get_current_page()
        page.view.set_focus(0, gaupol.gtk.COLUMN.MAIN_TEXT)
        self.application.on_split_subtitle_activate()

    def test_on_undo_action_activate(self):

        page = self.application.get_current_page()
        page.project.remove_subtitles([0])
        self.application.on_undo_action_activate()

    def test_on_undo_button_clicked(self):

        page = self.application.get_current_page()
        page.project.remove_subtitles([0])
        self.application.on_undo_button_clicked()

    def test_redo(self):

        page = self.application.get_current_page()
        page.project.remove_subtitles([0])
        self.application.undo()
        self.application.redo()

    def test_undo(self):

        page = self.application.get_current_page()
        page.project.remove_subtitles([0])
        self.application.undo()
