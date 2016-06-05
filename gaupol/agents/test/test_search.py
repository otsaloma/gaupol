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

import gaupol

from gi.repository import Gtk


class TestSearchAgent(gaupol.TestCase):

    def setup_method(self, method):
        self.application = self.new_application()
        self.delegate = self.application._on_find_next_activate.__self__

    def test__on_find_and_replace_activate(self):
        self.application.get_action("find-and-replace").activate()
        self.application.get_action("find-and-replace").activate()

    def test__on_find_next_activate(self):
        self.application.get_action("find-and-replace").activate()
        self.delegate._search_dialog._pattern_entry.set_text("a")
        self.application.get_action("find-next").activate()
        self.delegate._search_dialog.response(Gtk.ResponseType.CLOSE)
        self.application.get_action("find-next").activate()

    def test__on_find_previous_activate(self):
        self.application.get_action("find-and-replace").activate()
        self.delegate._search_dialog._pattern_entry.set_text("a")
        self.application.get_action("find-previous").activate()
        self.delegate._search_dialog.response(Gtk.ResponseType.CLOSE)
        self.application.get_action("find-previous").activate()
