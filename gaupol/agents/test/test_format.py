# -*- coding: utf-8-unix -*-

# Copyright (C) 2005-2008 Osmo Salomaa
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

import gaupol


class TestFormatAgent(gaupol.TestCase):

    def setup_method(self, method):
        self.application = self.new_application()
        page = self.application.get_current_page()
        page.view.set_focus(0, page.view.columns.MAIN_TEXT)
        page.view.select_rows((0, 1, 2))

    def test__on_toggle_dialogue_dashes_activate(self):
        self.application.get_action("toggle_dialogue_dashes").activate()

    def test__on_toggle_italicization_activate(self):
        self.application.get_action("toggle_italicization").activate()

    def test__on_use_lower_case_activate(self):
        self.application.get_action("use_lower_case").activate()

    def test__on_use_sentence_case_activate(self):
        self.application.get_action("use_sentence_case").activate()

    def test__on_use_title_case_activate(self):
        self.application.get_action("use_title_case").activate()

    def test__on_use_upper_case_activate(self):
        self.application.get_action("use_upper_case").activate()
