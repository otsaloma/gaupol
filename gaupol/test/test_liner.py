# Copyright (C) 2006-2007 Osmo Salomaa
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
import re


class TestLiner(gaupol.TestCase):

    def setup_method(self, method):

        self.liner = gaupol.Liner(re.compile(r"<.+?>"))
        self.liner.break_points.append((re.compile(r" (- )"), r"\n\1"))
        self.liner.break_points.append((re.compile(r"([.,?!]) "), r"\1\n"))

    def test_break_lines__01(self):

        text = ("- Isn't he off on Saturdays? "
                "- Didn't he tell you?")
        self.liner.set_text(text)
        assert self.liner.break_lines() == (
            "- Isn't he off on Saturdays?\n"
            "- Didn't he tell you?")

    def test_break_lines__02(self):

        text = ("- Isn't he off on Saturdays? "
                "- He changed shifts. "
                "- Didn't he tell you? "
                "- Can you give him this when he next comes?")
        self.liner.set_text(text)
        assert self.liner.break_lines() == (
            "- Isn't he off on Saturdays?\n"
            "- He changed shifts. - Didn't he tell you?\n"
            "- Can you give him this when he next comes?")

    def test_break_lines__03(self):

        text = ("Isn't he off on Saturdays? "
                "He changed shifts.")
        self.liner.set_text(text)
        assert self.liner.break_lines() == (
            "Isn't he off on Saturdays?\n"
            "He changed shifts.")

    def test_break_lines__04(self):

        text = ("Isn't he off on Saturdays? "
                "He changed shifts. "
                "Didn't he tell you?")
        self.liner.set_text(text)
        assert self.liner.break_lines() == (
            "Isn't he off on Saturdays?\n"
            "He changed shifts. Didn't he tell you?")

    def test_break_lines__05(self):

        text = "Isn't he off on Saturdays"
        self.liner.set_text(text)
        assert self.liner.break_lines() == text

    def test_break_lines__06(self):

        text = ("Isn't he off on Saturdays "
                "He changed shifts "
                "Didn't he tell you?")
        self.liner.set_text(text)
        assert self.liner.break_lines() == (
            "Isn't he off on Saturdays He\n"
            "changed shifts Didn't he tell you?")

    def test_break_lines__07(self):

        text = ("Isn't he off on Saturdays "
                "He changed shifts "
                "Didn't he tell you "
                "Can you give him this when he next comes")
        self.liner.set_text(text)
        assert self.liner.break_lines() == (
            "Isn't he off on Saturdays He changed\n"
            "shifts Didn't he tell you Can you\n"
            "give him this when he next comes")

    def test_break_lines__08(self):

        text = "test " * 50
        self.liner.set_text(text)
        assert self.liner.break_lines() == (
            "test test test test test test test test\n"
            "test test test test test test test test\n"
            "test test test test test test test test\n"
            "test test test test test test test test test\n"
            "test test test test test test test test\n"
            "test test test test test test test test test")

    def test_break_lines__09(self):

        text = "test " * 60
        self.liner.set_text(text)
        assert self.liner.break_lines() == (
            "test test test test test test test\n"
            "test test test test test test test test\n"
            "test test test test test test test\n"
            "test test test test test test test test\n"
            "test test test test test test test\n"
            "test test test test test test test test\n"
            "test test test test test test test\n"
            "test test test test test test test test")

    def test_break_lines__10(self):

        text = "testtesttesttest " * 101
        self.liner.set_text(text)
        assert self.liner.break_lines()

    def test_is_legal(self):

        text = "<i>I got to the restaurant a little early.</i>"
        self.liner.set_text(text)
        assert self.liner.is_legal()

        text = "He'soffdutytodayHe'soffdutytodayHe'soffdutytoday."
        self.liner.set_text(text)
        assert self.liner.is_legal()

        text = "<i>I got to the restaurant a little early little early.</i>"
        self.liner.set_text(text)
        assert not self.liner.is_legal()

    def test_set_length_func(self):

        get_length = lambda x: len(x)**2 + 1
        self.liner.set_length_func(get_length)
        assert self.liner._length_func == get_length
        assert self.liner._space_length == 2

    def test_set_text(self):

        self.liner.set_text(" <i>foo</i> ")
        assert self.liner.text == "foo"
