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


from gaupol.gtk.app           import Application
from gaupol.gtk.colcons       import *
from gaupol.gtk.delegate.edit import EditDelegate
from gaupol.test              import Test


class TestEditDelegate(Test):

    def setup_method(self, method):

        self.app = Application()
        self.app.open_main_files([self.get_subrip_path()])
        self.delegate = EditDelegate(self.app)

    def teardown_method(self, method):

        Test.teardown_method(self, method)
        self.app._window.destroy()

    def test_get_next_cell(self):

        page = self.app.get_current_page()
        get_next = self.delegate._get_next_cell
        max_row = len(page.project.times) - 1

        assert get_next(page, 0      , SHOW, 'Left' ) == (0      , SHOW)
        assert get_next(page, 0      , HIDE, 'Left' ) == (0      , SHOW)
        assert get_next(page, 0      , SHOW, 'Up'   ) == (0      , SHOW)
        assert get_next(page, 1      , SHOW, 'Up'   ) == (0      , SHOW)
        assert get_next(page, 0      , MTXT, 'Right') == (0      , MTXT)
        assert get_next(page, 0      , SHOW, 'Right') == (0      , HIDE)
        assert get_next(page, max_row, SHOW, 'Down' ) == (max_row, SHOW)
        assert get_next(page, 0      , SHOW, 'Down' ) == (1      , SHOW)

    def test_set_sensitivities(self):

        self.delegate._set_sensitivities(True)
        self.delegate._set_sensitivities(False)
        self.delegate._set_sensitivities(True)

    def test_actions(self):

        page = self.app.get_current_page()

        def test(name):
            page.view.set_focus(2, MTXT)
            page.view.select_rows([2, 3])
            getattr(self.app, name)()
            page.assert_store()

        test('on_clear_texts_activate')
        test('on_copy_texts_activate')
        test('on_cut_texts_activate')
        test('on_edit_value_activate')
        test('on_insert_subtitles_activate')
        test('on_invert_selection_activate')
        test('on_paste_texts_activate')
        test('on_remove_subtitles_activate')
        test('on_select_all_activate')
