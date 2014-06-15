# -*- coding: utf-8 -*-

# Copyright (C) 2011 Osmo Salomaa
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
import os
import sys

from gi.repository import Gtk


class TestAddBookmarkDialog(gaupol.TestCase):

    def run_dialog(self):
        self.dialog.run()
        self.dialog.destroy()

    def setup_method(self, method):
        directory = os.path.abspath(os.path.dirname(__file__))
        directory = os.path.abspath(os.path.join(directory, ".."))
        sys.path.insert(0, directory)
        module = __import__("bookmarks", {}, {}, [])
        self.application = self.new_application()
        self.page = self.application.get_current_page()
        self.page.view.select_rows((1,))
        self.dialog = module.AddBookmarkDialog(Gtk.Window(), self.page)
        self.dialog.show()

    def test_get_description(self):
        self.dialog._description_entry.set_text("test")
        assert self.dialog.get_description() == "test"

    def test_get_row(self):
        self.dialog._subtitle_spin.set_value(3)
        assert self.dialog.get_row() == 2


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
        directory = os.path.join(directory, "..", "..", "side-pane")
        directory = os.path.abspath(directory)
        sys.path.insert(0, directory)
        module = __import__("side-pane", {}, {}, [])
        return(module)

    def setup_method(self, method):
        self.application = self.new_application()
        module_sp = self.import_side_pane()
        self.extension_sp = module_sp.SidePaneExtension()
        self.extension_sp.setup(self.application)
        directory = os.path.abspath(os.path.dirname(__file__))
        directory = os.path.abspath(os.path.join(directory, ".."))
        sys.path.insert(0, directory)
        module = __import__("bookmarks", {}, {}, [])
        self.extension = module.BookmarksExtension()
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
        self.application.get_action("add_bookmark").activate()

    def test__on_edit_bookmarks_activate(self):
        self.application.get_action("edit_bookmarks").activate()

    def test__on_next_bookmark_activate(self):
        self.application.get_action("next_bookmark").activate()
        self.application.get_action("next_bookmark").activate()
        self.application.get_action("next_bookmark").activate()

    def test__on_previous_bookmark_activate(self):
        self.application.get_action("previous_bookmark").activate()
        self.application.get_action("previous_bookmark").activate()
        self.application.get_action("previous_bookmark").activate()

    def test_update(self):
        self.extension.update(self.application, self.page)
