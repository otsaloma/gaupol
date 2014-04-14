# -*- coding: utf-8 -*-

# Copyright (C) 2011-2012 Osmo Salomaa
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
import os
import sys
import traceback

from gi.repository import Gtk


class TestAddBookmarkDialog(gaupol.TestCase):

    def run__dialog(self):
        self.dialog.run()
        self.dialog.destroy()

    def setup_method(self, method):
        directory = os.path.abspath(os.path.dirname(__file__))
        directory = os.path.abspath(os.path.join(directory, ".."))
        sys.path.insert(0, directory)
        try:
            mobj = __import__("bookmarks", {}, {}, [])
        except ImportError:
            return traceback.print_exc()
        finally: sys.path.pop(0)
        self.application = self.new_application()
        self.page = self.application.get_current_page()
        self.page.view.select_rows((1,))
        self.dialog = mobj.AddBookmarkDialog(Gtk.Window(), self.page)
        self.dialog.show()

    def test_get_description(self):
        self.dialog._description_entry.set_text("test")
        text = self.dialog.get_description()
        assert text == "test"

    def test_get_row(self):
        self.dialog._subtitle_spin.set_value(3)
        row = self.dialog.get_row()
        assert row == 2


class TestBookmarksExtension(gaupol.TestCase):

    @aeidon.deco.monkey_patch(gaupol.util, "run_dialog")
    def bookmark_subtitles(self):
        gaupol.util.run_dialog = lambda *args: Gtk.ResponseType.OK
        action = self.application.get_action("add_bookmark")
        for i in range(5):
            self.page.view.select_rows((i,))
            action.activate()

    def import_side_pane(self):
        directory = os.path.abspath(os.path.dirname(__file__))
        directory = os.path.abspath(os.path.join(directory,
                                                 "..",
                                                 "..",
                                                 "side-pane"))

        sys.path.insert(0, directory)
        try:
            mobj = __import__("side-pane", {}, {}, [])
        except ImportError:
            return traceback.print_exc()
        finally: sys.path.pop(0)
        return(mobj)

    def setup_method(self, method):
        self.application = self.new_application()
        mobj_sp = self.import_side_pane()
        self.extension_sp = mobj_sp.SidePaneExtension()
        self.extension_sp.setup(self.application)
        directory = os.path.abspath(os.path.dirname(__file__))
        directory = os.path.abspath(os.path.join(directory, ".."))
        sys.path.insert(0, directory)
        try:
            mobj = __import__("bookmarks", {}, {}, [])
        except ImportError:
            return traceback.print_exc()
        finally: sys.path.pop(0)
        self.extension = mobj.BookmarksExtension()
        self.extension.setup(self.application)
        self.page = self.application.get_current_page()
        self.bookmark_subtitles()
        self.page.view.select_rows((1,))

    def teardown_method(self, method):
        self.extension.teardown(self.application)
        self.extension_sp.teardown(self.application)
        gaupol.TestCase.teardown_method(self, self.application)

    @aeidon.deco.monkey_patch(gaupol.util, "run_dialog")
    def test__on_add_bookmark_activate(self):
        gaupol.util.run_dialog = lambda *args: Gtk.ResponseType.OK
        action = self.application.get_action("add_bookmark")
        action.activate()

    def test__on_application_page_added(self):
        self.application.open_main(self.new_subrip_file())

    def test__on_application_page_closed(self):
        self.application.close(self.page)

    def test__on_application_page_switched(self):
        self.application.open_main(self.new_subrip_file())
        for page in self.application.pages:
            self.application.set_current_page(page)

    def test__on_edit_bookmarks_activate(self):
        action = self.application.get_action("edit_bookmarks")
        action.activate()

    def test__on_next_bookmark_activate(self):
        action = self.application.get_action("next_bookmark")
        action.activate()
        action.activate()
        action.activate()

    def test__on_project_main_file_saved(self):
        self.application.save_main(self.page)

    def test__on_project_subtitles_inserted(self):
        self.page.project.insert_subtitles(list(range(7)))

    def test__on_project_subtitles_removed(self):
        self.bookmark_subtitles()
        self.page.project.remove_subtitles(list(range(7)))

    def test__on_previous_bookmark_activate(self):
        action = self.application.get_action("previous_bookmark")
        action.activate()
        action.activate()
        action.activate()

    def test__on_search_entry_changed(self):
        self.extension._search_entry.set_text("a")
        self.extension._search_entry.set_text("x")

    def test__on_tree_view_selection_changed(self):
        selection = self.extension._tree_view.get_selection()
        selection.select_path(1)
        selection.select_path(2)
        selection.select_path(3)

    def test__read_bookmarks(self):
        path = self.new_subrip_file()
        path_bookmarks = path.replace(".srt", ".gaupol-bookmarks")
        f = open(path_bookmarks, "a")
        f.write("1 test\n")
        f.write("2 test\n")
        f.write("3 test\n")
        f.close()
        self.application.open_main(path)

    def test_setup(self):
        page = self.application.side_pane.get_current_page()
        assert page is self.extension._side_container

    def test_teardown(self):
        self.extension.teardown(self.application)
        page = self.application.side_pane.get_current_page()
        assert page is None
        self.extension.setup(self.application)

    def test_update(self):
        self.extension.update(self.application, self.page)
