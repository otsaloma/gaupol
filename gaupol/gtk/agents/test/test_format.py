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


from gaupol.gtk.index import *
from gaupol.gtk import unittest


class TestFormatAgent(unittest.TestCase):

    def setup_method(self, method):

        self.application = self.get_application()
        page = self.application.get_current_page()
        page.view.set_focus(0, gaupol.gtk.COLUMN.MAIN_TEXT)
        page.view.select_rows([0, 1, 2])

    def test_on_toggle_dialogue_lines_activate(self):

        self.application.on_toggle_dialogue_lines_activate()

    def test_on_toggle_italicization_activate(self):

        self.application.on_toggle_italicization_activate()

    def test_on_use_lower_case_activate(self):

        self.application.on_use_lower_case_activate()

    def test_on_use_sentence_case_activate(self):

        self.application.on_use_sentence_case_activate()

    def test_on_use_title_case_activate(self):

        self.application.on_use_title_case_activate()

    def test_on_use_upper_case_activate(self):

        self.application.on_use_upper_case_activate()
