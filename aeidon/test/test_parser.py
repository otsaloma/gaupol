# -*- coding: utf-8-unix -*-

# Copyright (C) 2005-2009 Osmo Salomaa
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
import re


class TestParser(aeidon.TestCase):

    def setup_method(self, method):
        clean_func = lambda x: x.strip()
        self.parser = aeidon.Parser(re.compile(r"<.+?>"), clean_func)

    def test_get_text__margins(self):
        text = ("<i>You will find allies there,</i>\n"
                "<i>and they will pay more.</i>")

        self.parser.set_text(text)
        assert self.parser.get_text() == text

    def test_get_text__tags(self):
        text = ("<i>You will find allies there,</i>\n"
                "<i>and</i> they <i>will pay more.</i>")

        self.parser.set_text(text)
        assert self.parser.get_text() == text

    def test_replace_all__regex(self):
        text = ("<i>One only risks it, <b>because</b>\n"
                "one's survival depends on it.</i>")

        cases = ((r"^", r"--",
                  ("<i>--One only risks it, <b>because</b>\n"
                   "--one's survival depends on it.</i>")),
                 (r"\A", r"--",
                  ("<i>--One only risks it, <b>because</b>\n"
                   "one's survival depends on it.</i>")),
                 (r"$", r"--",
                  ("<i>One only risks it, <b>because--</b>\n"
                   "one's survival depends on it.--</i>")),
                 (r"\Z", r"--",
                  ("<i>One only risks it, <b>because</b>\n"
                   "one's survival depends on it.--</i>")),
                 (r"\s", r"",
                  ("<i>Oneonlyrisksit,<b>because</b>"
                   "one'ssurvivaldependsonit.</i>")),
                 (r"\b", r"-",
                  ("<i>-One- -only- -risks- -it-, <b>-because-</b>\n"
                   "-one-'-s- -survival- -depends- -on- -it-.</i>")),
                 (r"\b$", r"-",
                  ("<i>One only risks it, <b>because-</b>\n"
                   "one's survival depends on it.</i>")),
                 (r"(\w)\w{3}", r"\1\1\1\1",
                  ("<i>One oooo rrrrs it, <b>bbbbuse</b>\n"
                   "one's ssssiiii ddddnds on it.</i>")),
                 (r"it, be", r"'",
                  ("<i>One only risks <b>'cause</b>\n"
                   "one's survival depends on it.</i>")),
                 (r".", r"",
                  ""),)

        for pattern, replacement, new_text in cases:
            self.parser = aeidon.Parser(re.compile(r"<.+?>"))
            self.parser.set_text(text)
            self.parser.set_regex(pattern)
            self.parser.replacement = replacement
            self.parser.replace_all()
            assert self.parser.get_text() == new_text

    def test_replace_all__string(self):
        text = ("<i>One only risks it, <b>because</b>\n"
                "one's survival depends on it.</i>")

        cases = (("i", "-",
                  ("<i>One only r-sks -t, <b>because</b>\n"
                   "one's surv-val depends on -t.</i>")),
                 ("O", "--",
                  ("<i>--ne only risks it, <b>because</b>\n"
                   "one's survival depends on it.</i>")),
                 ("O", "",
                  ("<i>ne only risks it, <b>because</b>\n"
                   "one's survival depends on it.</i>")),
                 ("b", "--",
                  ("<i>One only risks it, <b>--ecause</b>\n"
                   "one's survival depends on it.</i>")),
                 ("b", "",
                  ("<i>One only risks it, <b>ecause</b>\n"
                   "one's survival depends on it.</i>")),
                 ("e", "--",
                  ("<i>On-- only risks it, <b>b--caus--</b>\n"
                   "on--'s survival d--p--nds on it.</i>")),
                 ("e", "",
                  ("<i>On only risks it, <b>bcaus</b>\n"
                   "on's survival dpnds on it.</i>")),
                 ("o", "--",
                  ("<i>One --nly risks it, <b>because</b>\n"
                   "--ne's survival depends --n it.</i>")),
                 ("o", "",
                  ("<i>One nly risks it, <b>because</b>\n"
                   "ne's survival depends n it.</i>")),
                 (".", "--",
                  ("<i>One only risks it, <b>because</b>\n"
                   "one's survival depends on it--</i>")),
                 (".", "",
                  ("<i>One only risks it, <b>because</b>\n"
                   "one's survival depends on it</i>")),)

        for pattern, replacement, new_text in cases:
            self.parser = aeidon.Parser(re.compile(r"<.+?>"))
            self.parser.set_text(text)
            self.parser.pattern = pattern
            self.parser.replacement = replacement
            self.parser.replace_all()
            assert self.parser.get_text() == new_text

    def test_set_text__margins(self):
        text = ("<i>One only risks it, because</i>\n"
                "<i>one's survival depends on it.</i>")

        self.parser.set_text(text)
        assert self.parser.text == (
            "One only risks it, because\n"
            "one's survival depends on it.")

    def test_set_text__tags(self):
        text = ("<i>One only risks it, <b>because</b>\n"
                "one's survival depends on it.</i>")

        self.parser.set_text(text)
        assert self.parser.text == (
            "One only risks it, because\n"
            "one's survival depends on it.")
