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


import gaupol.gtk
import gtk
import random

from gaupol.gtk import unittest
from .. import view


class TestView(unittest.TestCase):

    def run__frame(self):

        self.setup_time()
        window = gtk.Window()
        window.connect("delete-event", gtk.main_quit)
        window.set_position(gtk.WIN_POS_CENTER)
        window.set_default_size(200, 200)
        window.add(self.view)
        window.show_all()
        gtk.main()

    def run__time(self):

        self.setup_frame()
        window = gtk.Window()
        window.connect("delete-event", gtk.main_quit)
        window.set_position(gtk.WIN_POS_CENTER)
        window.set_default_size(200, 200)
        window.add(self.view)
        window.show_all()
        gtk.main()

    def setup_frame(self):

        # pylint: disable-msg=W0201
        self.view = view.View(gaupol.gtk.MODE.FRAME)
        store = self.view.get_model()
        project = self.get_project()
        for subtitle in project.subtitles:
            store.append([0,
                subtitle.start_frame,
                subtitle.end_frame,
                subtitle.duration_frame,
                subtitle.main_text,
                subtitle.tran_text,])

    def setup_method(self, method):

        index = random.randint(0, 1)
        (self.setup_time, self.setup_frame)[index]()

    def setup_time(self):

        # pylint: disable-msg=W0201
        self.view = view.View(gaupol.gtk.MODE.TIME)
        store = self.view.get_model()
        project = self.get_project()
        for subtitle in project.subtitles:
            store.append([0,
                subtitle.start_time,
                subtitle.end_time,
                subtitle.duration_time,
                subtitle.main_text,
                subtitle.tran_text,])

    def test__on_conf_editor_notify_font(self):

        gaupol.gtk.conf.editor.use_default_font = False
        gaupol.gtk.conf.editor.font = "Serif 12"

    def test__on_conf_editor_notify_length_unit(self):

        gaupol.gtk.conf.editor.length_unit = gaupol.gtk.LENGTH_UNIT.CHAR
        gaupol.gtk.conf.editor.length_unit = gaupol.gtk.LENGTH_UNIT.EM

    def test__on_conf_editor_notify_show_lengths_cell(self):

        gaupol.gtk.conf.editor.show_lengths_cell = True
        gaupol.gtk.conf.editor.show_lengths_cell = False
        gaupol.gtk.conf.editor.show_lengths_cell = True
        gaupol.gtk.conf.editor.show_lengths_cell = False

    def test__on_conf_editor_notify_use_default_font(self):

        gaupol.gtk.conf.editor.use_default_font = True
        gaupol.gtk.conf.editor.use_default_font = False
        gaupol.gtk.conf.editor.use_default_font = True
        gaupol.gtk.conf.editor.use_default_font = False

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
