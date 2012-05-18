# -*- coding: utf-8-unix -*-

# Copyright (C) 2005-2008,2010 Osmo Salomaa
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

import aeidon
import gaupol
from gi.repository import Gtk


class TestSpellCheckAgent(gaupol.TestCase):

    def setup_method(self, method):
        self.application = self.new_application()

    @aeidon.deco.monkey_patch(gaupol.util, "flash_dialog")
    def test__on_check_spelling_activate(self):
        gaupol.util.flash_dialog = lambda *args: Gtk.ResponseType.OK
        gaupol.conf.spell_check.language = "en"
        self.application.get_action("check_spelling").activate()

    @aeidon.deco.monkey_patch(gaupol.util, "flash_dialog")
    def test__on_check_spelling_activate__value_error(self):
        gaupol.util.flash_dialog = lambda *args: Gtk.ResponseType.OK
        gaupol.conf.spell_check.language = "xx"
        self.application.get_action("check_spelling").activate()

    @aeidon.deco.monkey_patch(gaupol.util, "flash_dialog")
    def test__on_configure_spell_check_activate(self):
        gaupol.util.flash_dialog = lambda *args: Gtk.ResponseType.OK
        self.application.get_action("configure_spell_check").activate()

    @aeidon.deco.monkey_patch(gaupol.TextAssistant, "show")
    def test__on_correct_texts_activate(self):
        gaupol.TextAssistant.show = lambda *args: None
        self.application.get_action("correct_texts").activate()
