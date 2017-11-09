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

from aeidon.markups.test.test_microdvd import TestMicroDVD


class TestMPL2(TestMicroDVD):

    text = ("All things weird are normal\n"
            "in this whore of cities.")

    def setup_method(self, method):
        self.markup = aeidon.markups.new(aeidon.formats.MPL2)

    def test_bolden(self):
        assert self.markup.bolden(self.text, (0, 27)) == (
            "\\All things weird are normal\n"
            "in this whore of cities.")

    def test_decode__bold(self):
        text = ("\\All things weird are normal\n"
                "\\in this whore of cities.")
        assert self.markup.decode(text) == (
            "<b>All things weird are normal</b>\n"
            "<b>in this whore of cities.</b>")

    def test_decode__italic(self):
        text = ("/All things weird are normal\n"
                "in this whore of cities.")
        assert self.markup.decode(text) == (
            "<i>All things weird are normal</i>\n"
            "in this whore of cities.")

    def test_decode__multiple(self):
        text = ("/_All things weird are normal\n"
                "\\/_in this whore of cities.")
        assert self.markup.decode(text) == (
            "<i><u>All things weird are normal</u></i>\n"
            "<b><i><u>in this whore of cities.</u></i></b>")

    def test_decode__duplicate(self):
        text = ("//All things weird are normal\n"
                "/_/_in this whore of cities.")
        assert self.markup.decode(text) == (
            "<i>All things weird are normal</i>\n"
            "<i><u>in this whore of cities.</u></i>")

    def test_decode__underline(self):
        text = ("All things weird are normal\n"
                "_in this whore of cities.")
        assert self.markup.decode(text) == (
            "All things weird are normal\n"
            "<u>in this whore of cities.</u>")

    def test_encode__bold(self):
        text = ("<b>All things weird are normal\n"
                "in this whore of cities.</b>")
        assert self.markup.encode(text) == (
            "\\All things weird are normal\n"
            "\\in this whore of cities.")

    def test_encode__italic(self):
        text = ("All <i>things</i> weird are normal\n"
                "in <i>this</i> whore of cities.")
        assert self.markup.encode(text) == (
            "All things weird are normal\n"
            "in this whore of cities.")

    def test_encode__underline(self):
        text = ("All things weird are normal\n"
                "<u>in this whore of cities</u>.")
        assert self.markup.encode(text) == (
            "All things weird are normal\n"
            "_in this whore of cities.")

    def test_italic_tag(self):
        assert self.markup.italic_tag.match("/")
        assert self.markup.italic_tag.match("{Y:i}")
        assert self.markup.italic_tag.match("{y:i}")

    def test_italicize(self):
        assert self.markup.italicize(self.text) == (
            "/All things weird are normal\n"
            "/in this whore of cities.")

    def test_tag(self):
        assert self.markup.tag.match("\\")
        assert self.markup.tag.match("/")
        assert self.markup.tag.match("_")
        assert self.markup.tag.match("{y:ibu}")
        assert self.markup.tag.match("{c:$000000}")

    def test_underline(self):
        assert self.markup.underline(self.text, (0, 3)) == (
            "All things weird are normal\n"
            "in this whore of cities.")
