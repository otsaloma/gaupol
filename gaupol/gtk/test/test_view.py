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

from gaupol.gtk import conf, cons
from gaupol.gtk.unittest import TestCase
from .. import view


class TestView(TestCase):

    def run(self):

        window = gtk.Window()
        window.connect("delete-event", gtk.main_quit)
        window.set_position(gtk.WIN_POS_CENTER)
        window.set_default_size(200, 50)
        window.add(self.view)
        window.show_all()
        gtk.main()

    def setup_method(self, method):

        self.view = view.View(cons.MODE.FRAME)
        store = self.view.get_model()
        store.append([1, 2, 3, 1, "test\ntest", "test\ntest"])
        store.append([2, 6, 7, 1, "test\ntest", "test\ntest"])
        store.append([3, 8, 9, 1, "test\ntest", "test\ntest"])

    def test__on_conf_editor_notify_font(self):

        conf.editor.use_default_font = False
        conf.editor.font = "Serif 12"

    def test__on_conf_editor_notify_length_unit(self):

        conf.editor.length_unit = cons.LENGTH_UNIT.CHAR
        conf.editor.length_unit = cons.LENGTH_UNIT.EM

    def test__on_conf_editor_notify_show_lengths_cell(self):

        conf.editor.show_lengths_cell = True
        conf.editor.show_lengths_cell = False
        conf.editor.show_lengths_cell = True
        conf.editor.show_lengths_cell = False

    def test__on_conf_editor_notify_use_default_font(self):

        conf.editor.use_default_font = True
        conf.editor.use_default_font = False
        conf.editor.use_default_font = True
        conf.editor.use_default_font = False

    def test__on_cursor_changed(self):

        self.view.emit("cursor-changed")

    def test_get_focus(self):

        self.view.set_focus(2, None)
        assert self.view.get_focus() == (2, None)
        self.view.set_focus(1, 3)
        assert self.view.get_focus() == (1, 3)

    def test_get_selected_rows(self):

        self.view.select_rows([])
        assert self.view.get_selected_rows() == []
        self.view.select_rows([1, 2])
        assert self.view.get_selected_rows() == [1, 2]

    def test_scroll_to_row(self):

        self.view.scroll_to_row(1)
        self.view.scroll_to_row(2)

    def test_select_rows(self):

        self.view.select_rows([])
        assert self.view.get_selected_rows() == []
        self.view.select_rows([1, 2])
        assert self.view.get_selected_rows() == [1, 2]

    def test_set_focus(self):

        self.view.set_focus(2, None)
        assert self.view.get_focus() == (2, None)
        self.view.set_focus(1, 3)
        assert self.view.get_focus() == (1, 3)

    def test_update_headers(self):

        self.view.update_headers()
