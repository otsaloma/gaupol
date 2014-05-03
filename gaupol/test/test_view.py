# -*- coding: utf-8 -*-

# Copyright (C) 2005-2010 Osmo Salomaa
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
import random

from gi.repository import Gtk


class TestView(gaupol.TestCase):

    def run__view_frame(self):
        self.setup_frame()
        window = Gtk.Window()
        window.connect("delete-event", Gtk.main_quit)
        window.set_position(Gtk.WindowPosition.CENTER)
        window.set_default_size(200, 200)
        window.add(self.view)
        window.show_all()
        Gtk.main()

    def run__view_time(self):
        self.setup_time()
        window = Gtk.Window()
        window.connect("delete-event", Gtk.main_quit)
        window.set_position(Gtk.WindowPosition.CENTER)
        window.set_default_size(200, 200)
        window.add(self.view)
        window.show_all()
        Gtk.main()

    def setup_frame(self):
        self.view = gaupol.View(aeidon.modes.FRAME)
        store = self.view.get_model()
        self.project = self.new_project()
        for i, subtitle in enumerate(self.project.subtitles):
            store.append((i,
                          subtitle.start_frame,
                          subtitle.end_frame,
                          subtitle.duration_frame,
                          subtitle.main_text,
                          subtitle.tran_text,))

    def setup_method(self, method):
        random.choice((self.setup_frame, self.setup_time))()
        self.conf = gaupol.conf.editor

    def setup_time(self):
        self.view = gaupol.View(aeidon.modes.TIME)
        store = self.view.get_model()
        self.project = self.new_project()
        for i, subtitle in enumerate(self.project.subtitles):
            store.append((i,
                          subtitle.start_time,
                          subtitle.end_time,
                          subtitle.duration_seconds,
                          subtitle.main_text,
                          subtitle.tran_text,))

    def test__on_conf_editor_notify_custom_font(self):
        self.conf.use_custom_font = True
        self.conf.custom_font = "Serif 12"

    def test__on_conf_editor_notify_length_unit(self):
        for unit in gaupol.length_units:
            self.conf.length_unit = unit

    def test__on_conf_editor_notify_show_lengths_cell(self):
        self.conf.show_lengths_cell = True
        self.conf.show_lengths_cell = False

    def test__on_conf_editor_notify_use_custom_font(self):
        self.conf.custom_font = "Serif 12"
        self.conf.use_custom_font = True

    def test__on_columns_changed(self):
        for column in self.view.get_columns():
            column.set_visible(False)
        for column in self.view.get_columns():
            column.set_visible(True)

    def test__on_cursor_changed(self):
        self.view.emit("cursor-changed")
        self.view.emit("cursor-changed")

    def test_connect_selection_changed(self):
        def on_changed(*args): pass
        self.view.connect_selection_changed(on_changed)

    def test_disconnect_selection_changed(self):
        def on_changed(*args): pass
        self.view.connect_selection_changed(on_changed)
        self.view.disconnect_selection_changed(on_changed)

    def test_get_focus(self):
        get_focus = self.view.get_focus
        self.view.set_focus(2, None)
        assert get_focus() == (2, None)
        self.view.set_focus(1, 3)
        assert get_focus() == (1, 3)

    def test_get_selected_rows(self):
        get_selected_rows = self.view.get_selected_rows
        self.view.select_rows(())
        assert get_selected_rows() == ()
        self.view.select_rows((1, 2))
        assert get_selected_rows() == (1, 2)

    def test_is_position_column(self):
        is_position = self.view.is_position_column
        assert is_position(self.view.columns.START)
        assert is_position(self.view.columns.END)
        assert is_position(self.view.columns.DURATION)
        assert not is_position(self.view.columns.NUMBER)
        assert not is_position(self.view.columns.MAIN_TEXT)
        assert not is_position(self.view.columns.TRAN_TEXT)

    def test_is_text_column(self):
        is_text = self.view.is_text_column
        assert is_text(self.view.columns.MAIN_TEXT)
        assert is_text(self.view.columns.TRAN_TEXT)
        assert not is_text(self.view.columns.NUMBER)
        assert not is_text(self.view.columns.START)
        assert not is_text(self.view.columns.END)
        assert not is_text(self.view.columns.DURATION)

    def test_scroll_to_row(self):
        self.view.scroll_to_row(1)
        self.view.scroll_to_row(2)

    def test_select_rows(self):
        get_selected_rows = self.view.get_selected_rows
        self.view.select_rows(())
        assert get_selected_rows() == ()
        self.view.select_rows((1, 2))
        assert get_selected_rows() == (1, 2)

    def test_set_focus(self):
        get_focus = self.view.get_focus
        self.view.set_focus(2, None)
        assert get_focus() == (2, None)
        self.view.set_focus(1, 3)
        assert get_focus() == (1, 3)
        self.view.set_focus(-1, 4)
        n = len(self.project.subtitles)
        assert get_focus() == (n - 1, 4)

    def test_update_headers(self):
        self.view.update_headers()
        self.view.set_focus(1, 3)
        self.view.update_headers()
        self.view.set_focus(2, 4)
        self.view.update_headers()
