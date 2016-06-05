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
from unittest.mock import patch


class TestSpellCheckAgent(gaupol.TestCase):

    def setup_method(self, method):
        self.application = self.new_application()

    @patch("gaupol.util.flash_dialog", lambda *args: Gtk.ResponseType.OK)
    def test__on_check_spelling_activate(self):
        gaupol.conf.spell_check.language = "en"
        self.application.get_action("check-spelling").activate()

    @patch("gaupol.util.flash_dialog", lambda *args: Gtk.ResponseType.OK)
    def test__on_configure_spell_check_activate(self):
        self.application.get_action("configure-spell-check").activate()

    @patch("gaupol.TextAssistant.show", lambda *args: None)
    def test__on_correct_texts_activate(self):
        self.application.get_action("correct-texts").activate()
