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


class TestFormatAgent(gaupol.TestCase):

    def setup_method(self, method):
        self.application = self.new_application()
        page = self.application.get_current_page()
        page.view.set_focus(0, page.view.columns.MAIN_TEXT)
        page.view.select_rows((0, 1, 2))

    def test__on_toggle_dialogue_dashes_activate(self):
        self.application.get_action("toggle-dialogue-dashes").activate()

    def test__on_toggle_italicization_activate(self):
        self.application.get_action("toggle-italicization").activate()

    def test__on_use_lower_case_activate(self):
        self.application.get_action("use-lower-case").activate()

    def test__on_use_sentence_case_activate(self):
        self.application.get_action("use-sentence-case").activate()

    def test__on_use_title_case_activate(self):
        self.application.get_action("use-title-case").activate()

    def test__on_use_upper_case_activate(self):
        self.application.get_action("use-upper-case").activate()
