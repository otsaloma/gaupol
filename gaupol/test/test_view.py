# -*- coding: utf-8 -*-

# Copyright (C) 2005 Osmo Salomaa
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

    def run_view_frame(self):
        self.setup_frame()
        window = Gtk.Window()
        window.connect("delete-event", Gtk.main_quit)
        window.set_position(Gtk.WindowPosition.CENTER)
        window.set_default_size(200, 200)
        window.add(self.view)
        window.show_all()
        Gtk.main()

    def run_view_time(self):
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
            store.append((i + 1,
                          subtitle.start_frame,
                          subtitle.end_frame,
                          subtitle.duration_frame,
                          subtitle.main_text,
                          subtitle.tran_text))

    def setup_method(self, method):
        random.choice((self.setup_frame, self.setup_time))()
        self.conf = gaupol.conf.editor

    def setup_time(self):
        self.view = gaupol.View(aeidon.modes.TIME)
        store = self.view.get_model()
        self.project = self.new_project()
        for i, subtitle in enumerate(self.project.subtitles):
            store.append((i + 1,
                          subtitle.start_time,
                          subtitle.end_time,
                          subtitle.duration_seconds,
                          subtitle.main_text,
                          subtitle.tran_text))

    def test_select_rows(self):
        self.view.select_rows(())
        assert self.view.get_selected_rows() == ()
        self.view.select_rows((1, 2))
        assert self.view.get_selected_rows() == (1, 2)

    def test_set_focus(self):
        self.view.set_focus(2, None)
        assert self.view.get_focus() == (2, None)
        self.view.set_focus(1, 3)
        assert self.view.get_focus() == (1, 3)
        self.view.set_focus(-1, 4)
        n = len(self.project.subtitles)
        assert self.view.get_focus() == (n-1, 4)
