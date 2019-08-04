# -*- coding: utf-8 -*-

# Copyright (C) 2019 Osmo Salomaa
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

from gi.repository import Gtk


class TestSpellChecker(aeidon.TestCase):

    def run_checker(self):
        text_view = Gtk.TextView()
        text_buffer = text_view.get_buffer()
        text_buffer.set_text("It's a humanoid weapon-system\ncreated by the URM Technarchy.")
        self.checker.attach(text_view)
        window = Gtk.Window()
        window.connect("delete-event", Gtk.main_quit)
        window.set_position(Gtk.WindowPosition.CENTER)
        window.set_default_size(400, 200)
        window.add(text_view)
        window.show_all()
        Gtk.main()

    def setup_method(self, method):
        language = self.get_spell_check_language("en")
        self.checker = gaupol.SpellChecker(language)
