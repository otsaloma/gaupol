# -*- coding: utf-8 -*-

# Copyright (C) 2011 Osmo Salomaa
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
import re


class TestLiner(aeidon.TestCase):

    def setup_method(self, method):
        self.liner = aeidon.Liner(re.compile(r"<.+?>"))
        self.liner.set_penalties((
            dict(pattern=r"( )- ",
                 flags=re.DOTALL|re.MULTILINE,
                 group=1,
                 value=-1000),

            dict(pattern=r"[,.;:!?]( )",
                 flags=re.DOTALL|re.MULTILINE,
                 group=1,
                 value=-100),

            dict(pattern=r"\b(by|the|into|a)( )",
                 flags=re.DOTALL|re.MULTILINE,
                 group=2,
                 value=1000)))

    def test_break_lines__1(self):
        text = "Hello."
        self.liner.set_text(text)
        assert self.liner.break_lines() == "Hello."

    def test_break_lines__2(self):
        text = ("- Isn't he off on Saturdays? "
                "- Didn't he tell you?")

        self.liner.set_text(text)
        assert self.liner.break_lines() == (
            "- Isn't he off on Saturdays?\n"
            "- Didn't he tell you?")

    def test_break_lines__3(self):
        text = ("Close by the king's castle "
                "lay a great dark forest.")

        self.liner.set_text(text)
        assert self.liner.break_lines() == (
            "Close by the king's castle\n"
            "lay a great dark forest.")

    def test_break_lines__4(self):
        text = ("The king's child went out "
                "into the forest and sat down "
                "by the side of the cool fountain.")

        self.liner.set_text(text)
        assert self.liner.break_lines() == (
            "The king's child went out\n"
            "into the forest and sat down\n"
            "by the side of the cool fountain.")

    def test_break_lines__5(self):
        text = ("The king's child went out "
                "into the forest and sat down by the side "
                "of the cool fountain; and when "
                "she was bored she took a golden ball, "
                "and threw it up high and caught it; "
                "and this ball was her favorite plaything.")

        self.liner.set_text(text)
        assert self.liner.break_lines() == (
            "The king's child went out\n"
            "into the forest and sat down by the side\n"
            "of the cool fountain; and when she\n"
            "was bored she took a golden ball,\n"
            "and threw it up high and caught it; and\n"
            "this ball was her favorite plaything.")
