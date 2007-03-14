# Copyright (C) 2007 Osmo Salomaa
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


from gaupol import cons, scriptlib
from gaupol.unittest import TestCase, reversion_test


class TestTextAgent(TestCase):

    def setup_method(self, method):

        self.project = self.get_project()

        self.project.main_texts[0] = \
            "<i>- which... paper?</i>\n" + \
            "<i>- figaro-pravda a.k.a. the paper.</i>"
        self.project.main_texts[1] = \
            "room 344. have you registered\n" + \
            "at residents control..."
        self.project.main_texts[2] = \
            "you must, even if you're...\n" + \
            "...a festival visitor."

        self.project.main_texts[3] = \
            "Room 344."
        self.project.main_texts[4] = \
            "Room 344. Have you registered at residents control?"
        self.project.main_texts[5] = \
            "Room 344. Have you registered at residents control?\n" + \
            "Room 344. Have you registered at residents control?\n" + \
            "Room 344. Have you registered at residents control?"
        self.project.main_texts[6] = \
            "Room 344.\n" + \
            "Room 344.\n" + \
            "Room 344."
        self.project.main_texts[7] = \
            "- Room 344.\n" + \
            "- Room 344.\n" + \
            "- Room 344."

    @reversion_test
    def test_capitalize(self):

        pattern = scriptlib.get_capitalize_after("latin")
        rows = self.project.capitalize([0, 1, 2], cons.DOCUMENT.MAIN, pattern)

        assert rows == [0, 1]
        assert self.project.main_texts[0] == \
            "<i>- Which... paper?</i>\n" + \
            "<i>- Figaro-pravda a.k.a. the paper.</i>"
        assert self.project.main_texts[1] == \
            "Room 344. Have you registered\n" + \
            "at residents control..."
        assert self.project.main_texts[2] == \
            "you must, even if you're...\n" + \
            "...a festival visitor."

    @reversion_test
    def test_format_lines(self):

        rows = self.project.format_lines(
            rows=[3, 4, 5, 6],
            doc=cons.DOCUMENT.MAIN,
            dialogue_pattern=scriptlib.get_dialogue_separator("latin"),
            clause_pattern=scriptlib.get_clause_separator("latin-english"),
            ok_dialogue=3,
            ok_clauses=2,
            max_length=32,
            length_func=len,
            legal_length=32,
            legal_lines=2,
            require_reduction=True)

        assert rows == [4, 5, 6]
        assert self.project.main_texts[3] == "Room 344."
        assert self.project.main_texts[4] == \
            "Room 344. Have you registered\n" + \
            "at residents control?"
        assert self.project.main_texts[5] == \
            "Room 344. Have you registered\n" + \
            "at residents control? Room 344.\n" + \
            "Have you registered at residents\n" + \
            "control? Room 344. Have you\n" + \
            "registered at residents control?"
        assert self.project.main_texts[6] == \
            "Room 344.\n" + \
            "Room 344. Room 344."
        assert self.project.main_texts[7] == \
            "- Room 344.\n" + \
            "- Room 344.\n" + \
            "- Room 344."
