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

from gi.repository import Gtk


class TestSpellCheckDialog(gaupol.TestCase):

    def run_dialog(self):
        self.dialog.run()
        self.dialog.destroy()

    def setup_method(self, method):
        # Don't interact with the config files at all.
        aeidon.SpellChecker.add_to_personal = aeidon.SpellChecker.add_to_session
        aeidon.SpellChecker.read_replacements = lambda *args: None
        aeidon.SpellChecker.write_replacements = lambda *args: None
        language = self.get_spell_check_language("en")
        gaupol.conf.spell_check.language = language
        self.application = self.new_application()
        for page in self.application.pages:
            for subtitle in page.project.subtitles:
                subtitle.main_text = subtitle.main_text.replace("a", "x")
                subtitle.tran_text = subtitle.tran_text.replace("a", "x")
            page.reload_view_all()
        self.dialog = gaupol.SpellCheckDialog(self.application.window, self.application)
        self.dialog.show()

    def test__on_add_button_clicked(self):
        self.dialog._add_button.emit("clicked")

    def test__on_ignore_all_button_clicked(self):
        self.dialog._ignore_all_button.emit("clicked")

    def test__on_ignore_button_clicked(self):
        self.dialog._ignore_button.emit("clicked")

    def test__on_replace_all_button_clicked(self):
        self.dialog._replace_all_button.emit("clicked")

    def test__on_replace_button_clicked(self):
        self.dialog._replace_button.emit("clicked")

    def test__on_response(self):
        self.dialog._replace_button.emit("clicked")
        self.dialog.response(Gtk.ResponseType.CLOSE)
