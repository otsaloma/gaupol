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

import gaupol
import os
import sys

from gi.repository import Gtk


class TestSidePane(gaupol.TestCase):

    def setup_method(self, method):
        directory = os.path.abspath(os.path.dirname(__file__))
        directory = os.path.abspath(os.path.join(directory, ".."))
        sys.path.insert(0, directory)
        module = __import__("side-pane", {}, {}, [])
        options = {"width": 200, "page": "", "visible": True}
        gaupol.conf.register_extension("side_pane", options)
        self.application = self.new_application()
        self.side_pane = module.SidePane(self.application)
        self.page1 = Gtk.TextView()
        self.page2 = Gtk.TextView()
        self.side_pane.add_page(self.page1, "test1", "Test 1")
        self.side_pane.add_page(self.page2, "test2", "Test 2")

    def test_add_page(self):
        text_view = Gtk.TextView()
        self.side_pane.add_page(text_view, "test", "Test")
        page = self.side_pane.get_current_page()
        assert page is text_view

    def test_hide(self):
        self.side_pane.show()
        self.side_pane.hide()

    def test_remove(self):
        self.side_pane.remove()

    def test_remove_page(self):
        self.side_pane.set_current_page(self.page1)
        self.side_pane.remove_page(self.page1)
        page = self.side_pane.get_current_page()
        assert page is not self.page1

    def test_show(self):
        self.side_pane.hide()
        self.side_pane.show()


class TestSidePaneExtension(gaupol.TestCase):

    def setup_method(self, method):
        directory = os.path.abspath(os.path.dirname(__file__))
        directory = os.path.abspath(os.path.join(directory, ".."))
        sys.path.insert(0, directory)
        module = __import__("side-pane", {}, {}, [])
        self.extension = module.SidePaneExtension()
        self.application = self.new_application()
        self.extension.setup(self.application)

    def teardown_method(self, method):
        self.extension.teardown(self.application)
        gaupol.TestCase.teardown_method(self, self.application)

    def test_setup(self):
        assert hasattr(self.application, "side_pane")

    def test_teardown(self):
        self.extension.teardown(self.application)
        assert not hasattr(self.application, "side_pane")
        self.extension.setup(self.application)
