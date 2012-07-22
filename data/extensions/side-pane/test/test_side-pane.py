# -*- coding: utf-8-unix -*-

# Copyright (C) 2011 Osmo Salomaa
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

import gaupol
import os
import sys
import traceback

from gi.repository import Gtk


class TestSidePane(gaupol.TestCase):

    def setup_method(self, method):
        directory = os.path.abspath(os.path.dirname(__file__))
        directory = os.path.abspath(os.path.join(directory, ".."))
        sys.path.insert(0, directory)
        try: mobj = __import__("side-pane", {}, {}, [])
        except ImportError:
            return traceback.print_exc()
        finally: sys.path.pop(0)
        gaupol.conf.register_extension("side_pane",
                                       {"width": 200,
                                        "page": "",
                                        "visible": True})

        self.application = self.new_application()
        self.side_pane = mobj.SidePane(self.application)

    def test__on_header_close_button_clicked(self):
        side_vbox = self.side_pane._paned.get_child1()
        header_hbox = side_vbox.get_children()[0]
        button = header_hbox.get_children()[-1]
        button.emit("clicked")
        assert not side_vbox.props.visible

    def test_add_page(self):
        text_view = Gtk.TextView()
        self.side_pane.add_page(text_view, "test", "Test")
        page = self.side_pane.get_current_page()
        assert page is text_view

    def test_get_current_page(self):
        text_view = Gtk.TextView()
        self.side_pane.add_page(text_view, "test", "Test")
        page = self.side_pane.get_current_page()
        assert page is text_view

    def test_hide(self):
        self.side_pane.show()
        self.side_pane.hide()
        side_vbox = self.side_pane._paned.get_child1()
        assert not side_vbox.props.visible

    def test_remove(self):
        text_view = Gtk.TextView()
        self.side_pane.add_page(text_view, "test", "Test")
        self.side_pane.remove()

    def test_remove_page(self):
        text_view = Gtk.TextView()
        self.side_pane.add_page(text_view, "test", "Test")
        page = self.side_pane.get_current_page()
        assert page is text_view
        self.side_pane.remove_page(text_view)
        page = self.side_pane.get_current_page()
        assert page is None

    def test_set_current_page(self):
        text_view_1 = Gtk.TextView()
        text_view_2 = Gtk.TextView()
        self.side_pane.add_page(text_view_1, "test_1", "Test 1")
        self.side_pane.add_page(text_view_2, "test_2", "Test 2")
        self.side_pane.set_current_page(text_view_1)
        assert self.side_pane._conf.page == "test_1"
        self.side_pane.set_current_page(text_view_2)
        assert self.side_pane._conf.page == "test_2"

    def test_show(self):
        self.side_pane.hide()
        self.side_pane.show()
        side_vbox = self.side_pane._paned.get_child1()
        assert side_vbox.props.visible


class TestSidePaneExtension(gaupol.TestCase):

    def setup_method(self, method):
        directory = os.path.abspath(os.path.dirname(__file__))
        directory = os.path.abspath(os.path.join(directory, ".."))
        sys.path.insert(0, directory)
        try: mobj = __import__("side-pane", {}, {}, [])
        except ImportError:
            return traceback.print_exc()
        finally: sys.path.pop(0)
        self.extension = mobj.SidePaneExtension()
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
