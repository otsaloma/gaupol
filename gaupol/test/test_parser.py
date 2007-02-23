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


import re

from gaupol.unittest import TestCase
from .. import parser


ORIG_TEXT = \
"""<i>One only risks it, <b>because</b>
one's survival depends on it.</i>"""


class TestParser(TestCase):

    def setup_method(self, method):

        self.parser = parser.Parser(re.compile(r"<.*?>"))
        self.parser.set_text(ORIG_TEXT)

    def test_get_text(self):

        assert self.parser.get_text() == ORIG_TEXT

        text = \
            "<i>One only risks it, because</i>\n" + \
            "<i>one's survival depends on it.</i>"
        self.parser.set_text(text)
        assert self.parser.get_text() == text

    def test_replace_all_regex(self):

        cases = (
            (r"^", r"--",
                "<i>--One only risks it, <b>because</b>\n" + \
                "--one's survival depends on it.</i>"),
            (r"\A", r"--",
                "<i>--One only risks it, <b>because</b>\n" + \
                "one's survival depends on it.</i>"),
            (r"$", r"--",
                "<i>One only risks it, <b>because--</b>\n" + \
                "one's survival depends on it.--</i>"),
            (r"\Z", r"--",
                "<i>One only risks it, <b>because</b>\n" + \
                "one's survival depends on it.--</i>"),
            (r"\s", r"",
                "<i>Oneonlyrisksit,<b>because</b>" + \
                "one'ssurvivaldependsonit.</i>"),
            (r"\b", r"-",
                 "<i>-One- -only- -risks- -it-, <b>-because-</b>\n" + \
                 "-one-'-s- -survival- -depends- -on- -it-.</i>"),
            (r"\b$", r"-",
                 "<i>One only risks it, <b>because-</b>\n" + \
                 "one's survival depends on it.</i>"),
            (r"(\w)\w{3}", r"\1\1\1\1",
                "<i>One oooo rrrrs it, <b>bbbbuse</b>\n" + \
                "one's ssssiiii ddddnds on it.</i>"))

        for pattern, replacement, text in cases:
            self.parser = parser.Parser(re.compile(r"<.*?>"))
            self.parser.set_text(ORIG_TEXT)
            self.parser.set_regex(pattern)
            self.parser.replacement = replacement
            self.parser.replace_all()
            assert self.parser.get_text() == text

    def test_replace_all_string(self):

        cases = (
            ("i", "-",
                "<i>One only r-sks -t, <b>because</b>\n" + \
                "one's surv-val depends on -t.</i>"),
            ("O", "--",
                "<i>--ne only risks it, <b>because</b>\n" + \
                "one's survival depends on it.</i>"),
            ("O", "",
                "<i>ne only risks it, <b>because</b>\n" + \
                "one's survival depends on it.</i>"),
            ("b", "--",
                "<i>One only risks it, <b>--ecause</b>\n" + \
                "one's survival depends on it.</i>"),
            ("b", "",
                "<i>One only risks it, <b>ecause</b>\n" + \
                "one's survival depends on it.</i>"),
            ("e", "--",
                "<i>On-- only risks it, <b>b--caus--</b>\n" + \
                "on--'s survival d--p--nds on it.</i>"),
            ("e", "",
                "<i>On only risks it, <b>bcaus</b>\n" + \
                "on's survival dpnds on it.</i>"),
            ("o", "--",
                "<i>One --nly risks it, <b>because</b>\n" + \
                "--ne's survival depends --n it.</i>"),
            ("o", "",
                "<i>One nly risks it, <b>because</b>\n" + \
                "ne's survival depends n it.</i>"),
            (".", "--",
                "<i>One only risks it, <b>because</b>\n" + \
                "one's survival depends on it--</i>"),
            (".", "",
                "<i>One only risks it, <b>because</b>\n" + \
                "one's survival depends on it</i>"))

        for pattern, replacement, text in cases:
            self.parser = parser.Parser(re.compile(r"<.*?>"))
            self.parser.set_text(ORIG_TEXT)
            self.parser.pattern = pattern
            self.parser.replacement = replacement
            self.parser.replace_all()
            assert self.parser.get_text() == text

    def test_set_text(self):

        self.parser.set_text(ORIG_TEXT)
        assert not self.parser.margins
        assert self.parser.tags
        assert self.parser.text == \
            "One only risks it, because\n" + \
            "one's survival depends on it."

        text = \
            "<i>One only risks it, because</i>\n" + \
            "<i>one's survival depends on it.</i>"
        self.parser.set_text(text)
        assert self.parser.margins == ["<i>", "</i>"]
        assert not self.parser.tags
        assert self.parser.text == \
            "One only risks it, because\n" + \
            "one's survival depends on it."
