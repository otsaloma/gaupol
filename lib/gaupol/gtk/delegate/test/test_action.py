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


from gaupol.gtk         import cons
from gaupol.gtk.app     import Application
from gaupol.gtk.colcons import *
from gaupol.test        import Test


class TestActionDelegate(Test):

    def setup_method(self, method):

        self.app = Application()
        self.app.open_main_files([self.get_subrip_path()])

    def teardown_method(self, method):

        Test.teardown_method(self, method)
        self.app._window.destroy()

    def test_redo_and_undo_insert(self):

        page = self.app.get_current_page()
        page.project.insert_subtitles([1])
        page.assert_store()
        self.app.undo()
        page.assert_store()
        self.app.redo()
        page.assert_store()

    def test_redo_and_undo_multiple(self):

        page = self.app.get_current_page()
        page.project.set_text(0, MAIN, 'test')
        page.project.set_text(1, MAIN, 'test')
        page.project.insert_subtitles([1])
        page.project.set_text(1, MAIN, 'test')
        page.project.set_text(3, MAIN, 'test')
        page.project.insert_subtitles([4])
        page.project.set_text(4, MAIN, 'test')
        page.project.remove_subtitles([5])
        page.project.set_text(5, MAIN, 'test')
        page.assert_store()

        while page.project.can_undo():
            self.app.undo()
            page.assert_store()

        while page.project.can_redo():
            self.app.redo()
            page.assert_store()

        self.app.undo(9)
        page.assert_store()
        self.app.redo(9)
        page.assert_store()

    def test_redo_and_undo_remove(self):

        page = self.app.get_current_page()
        page.project.remove_subtitles([1])
        page.assert_store()
        self.app.undo()
        page.assert_store()
        self.app.redo()
        page.assert_store()

    def test_redo_and_undo_update(self):

        page = self.app.get_current_page()
        page.project.set_text(0, MAIN, 'test')
        page.assert_store()
        self.app.undo()
        page.assert_store()
        self.app.redo()
        page.assert_store()
