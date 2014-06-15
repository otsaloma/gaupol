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


class TestAddFramerateDialog(gaupol.TestCase):

    def run_dialog(self):
        self.dialog.run()
        self.dialog.destroy()

    def setup_method(self, method):
        directory = os.path.abspath(os.path.dirname(__file__))
        directory = os.path.abspath(os.path.join(directory, ".."))
        sys.path.insert(0, directory)
        module = __import__("custom-framerates", {}, {}, [])
        self.dialog = module.AddFramerateDialog(Gtk.Window())
        self.dialog.show()

    def test__on_response(self):
        self.dialog.response(Gtk.ResponseType.OK)

    def test_get_framerate(self):
        assert self.dialog.get_framerate() == 0.0


class TestPreferencesDialog(gaupol.TestCase):

    def run_dialog(self):
        self.dialog.run()
        self.dialog.destroy()

    def setup_method(self, method):
        directory = os.path.abspath(os.path.dirname(__file__))
        directory = os.path.abspath(os.path.join(directory, ".."))
        sys.path.insert(0, directory)
        module = __import__("custom-framerates", {}, {}, [])
        self.framerates = (20.0, 21.0, 22.0, 23.0)
        self.dialog = module.PreferencesDialog(self.framerates, Gtk.Window())
        self.dialog.show()

    @aeidon.deco.monkey_patch(gaupol.util, "run_dialog")
    def test__on_add_button_clicked(self):
        gaupol.util.run_dialog = lambda *args: Gtk.ResponseType.OK
        orig_framerates = self.dialog.get_framerates()
        self.dialog._add_button.emit("clicked")
        framerates = self.dialog.get_framerates()
        assert len(framerates) == len(orig_framerates) + 1
        assert 0.0 in framerates

    def test__on_remove_button_clicked(self):
        orig_framerates = self.dialog.get_framerates()
        selection = self.dialog._tree_view.get_selection()
        selection.unselect_all()
        path = gaupol.util.tree_row_to_path(0)
        selection.select_path(path)
        self.dialog._remove_button.emit("clicked")
        framerates = self.dialog.get_framerates()
        assert len(framerates) == len(orig_framerates) - 1

    def test_get_framerates(self):
        framerates = self.dialog.get_framerates()
        assert framerates == self.framerates


class TestCustomFrameratesExtension(gaupol.TestCase):

    def setup_method(self, method):
        directory = os.path.abspath(os.path.dirname(__file__))
        directory = os.path.abspath(os.path.join(directory, ".."))
        sys.path.insert(0, directory)
        module = __import__("custom-framerates", {}, {}, [])
        self.extension = module.CustomFrameratesExtension()
        self.application = self.new_application()
        self.extension.setup(self.application)

    def teardown_method(self, method):
        self.extension.teardown(self.application)
        gaupol.TestCase.teardown_method(self, self.application)

    def test_setup(self):
        assert hasattr(aeidon.framerates, "FPS_48_000")

    @aeidon.deco.monkey_patch(gaupol.util, "run_dialog")
    def test_show_preferences_dialog(self):
        gaupol.util.run_dialog = lambda *args: Gtk.ResponseType.CLOSE
        self.extension.show_preferences_dialog(self.application.window)

    def test_teardown(self):
        self.extension.teardown(self.application)
        assert not hasattr(aeidon.framerates, "FPS_48_000")
        self.extension.setup(self.application)

    def test_teardown__custom(self):
        page = self.application.get_current_page()
        page.project.set_framerate(aeidon.framerates.FPS_48_000)
        self.extension.teardown(self.application)
        self.extension.setup(self.application)

    def test_teardown__custom_no_pages(self):
        page = self.application.get_current_page()
        page.project.set_framerate(aeidon.framerates.FPS_48_000)
        while self.application.pages:
            page = self.application.get_current_page()
            self.application.close(page, confirm=False)
        self.extension.teardown(self.application)
        self.extension.setup(self.application)
