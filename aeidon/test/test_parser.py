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

import aeidon
import re


class TestParser(aeidon.TestCase):

    def setup_method(self, method):
        self.parser = aeidon.Parser(re.compile(r"<.+?>"),
                                    lambda x: x.strip())

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

        self.parser.set_text(text)
        self.parser.set_regex(r"\b")
        self.parser.replacement = "-"
        self.parser.replace_all()
        assert self.parser.get_text() == (
            "<i>-One- -only- -risks- -it-, <b>-because-</b>\n"
            "-one-'-s- -survival- -depends- -on- -it-.</i>")

    def test_replace_all__string(self):
        text = ("<i>One only risks it, <b>because</b>\n"
                "one's survival depends on it.</i>")

        self.parser.set_text(text)
        self.parser.pattern = "e"
        self.parser.replacement = ""
        self.parser.replace_all()
        assert self.parser.get_text() == (
            "<i>On only risks it, <b>bcaus</b>\n"
            "on's survival dpnds on it.</i>")

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
