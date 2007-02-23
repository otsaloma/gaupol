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


import gobject
import gtk

from gaupol.gtk.unittest import TestCase
from .. import multiline


class TestCellTextView(TestCase):

    def setup_method(self, method):

        self.text_view = multiline._CellTextView()

    def test_editing_done(self):

        self.text_view.editing_done()

    def test_get_text(self):

        self.text_view.set_text("test")
        assert self.text_view.get_text() == "test"

    def test_set_text(self):

        self.text_view.set_text("test")
        assert self.text_view.get_text() == "test"


class TestMultilineCellRenderer(TestCase):

    def run(self):

        tree_view = gtk.TreeView()
        tree_view.set_headers_visible(False)
        store = gtk.ListStore(gobject.TYPE_STRING)
        store.append(["test\ntest test"])
        tree_view.set_model(store)
        self.renderer.props.editable = True
        column = gtk.TreeViewColumn("", self.renderer, text=0)
        tree_view.append_column(column)

        window = gtk.Window()
        window.connect("delete-event", gtk.main_quit)
        window.set_position(gtk.WIN_POS_CENTER)
        window.set_default_size(240, 70)
        window.add(tree_view)
        window.show_all()
        gtk.main()

    def setup_method(self, method):

        self.renderer = multiline.MultilineCellRenderer()

    def test___init__(self):

        pass
