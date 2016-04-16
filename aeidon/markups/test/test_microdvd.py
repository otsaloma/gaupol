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


class TestMicroDVD(aeidon.TestCase):

    text = ("All things weird are normal\n"
            "in this whore of cities.")

    def setup_method(self, method):
        self.markup = aeidon.markups.new(aeidon.formats.MICRODVD)

    def test_bolden(self):
        assert self.markup.bolden(self.text, (0, 27)) == (
            "{y:b}All things weird are normal\n"
            "in this whore of cities.")

    def test_colorize(self):
        assert self.markup.colorize(self.text, "ccff00") == (
            "{C:$00ffcc}All things weird are normal\n"
            "in this whore of cities.")

    def test_decode__bold(self):
        text = ("{Y:b}All things weird are normal\n"
                "in this whore of cities.")
        assert self.markup.decode(text) == (
            "<b>All things weird are normal\n"
            "in this whore of cities.</b>")

    def test_decode__color(self):
        text = ("All things weird are normal\n"
                "{c:$0000ff}in this whore of cities.")
        assert self.markup.decode(text) == (
            "All things weird are normal\n"
            "<color=#ff0000>in this whore of cities.</color>")

    def test_decode__combined(self):
        text = ("{Y:bi}All things weird are normal\n"
                "{y:u}in this whore of cities.")
        assert self.markup.decode(text) == (
            "<b><i>All things weird are normal\n"
            "<u>in this whore of cities.</u></i></b>")

    def test_decode__font(self):
        text = ("{f:sans}All things weird are normal\n"
                "in this whore of cities.")
        assert self.markup.decode(text) == (
            "<font=sans>All things weird are normal</font>\n"
            "in this whore of cities.")

    def test_decode__italic(self):
        text = ("{y:i}All things weird are normal\n"
                "{y:i}in this whore of cities.")
        assert self.markup.decode(text) == (
            "<i>All things weird are normal</i>\n"
            "<i>in this whore of cities.</i>")

    def test_decode__size(self):
        text = ("All things weird are normal\n"
                "{s:12}in this whore of cities.")
        assert self.markup.decode(text) == (
            "All things weird are normal\n"
            "<size=12>in this whore of cities.</size>")

    def test_decode__underline(self):
        text = ("{Y:u}All things weird are normal\n"
                "in this whore of cities.")
        assert self.markup.decode(text) == (
            "<u>All things weird are normal\n"
            "in this whore of cities.</u>")

    def test_encode__bold(self):
        text = ("<b>All things weird are normal\n"
                "in this whore of cities.</b>")
        assert self.markup.encode(text) == (
            "{Y:b}All things weird are normal\n"
            "in this whore of cities.")

    def test_encode__color(self):
        text = ("<color=#ccccff>All things weird are normal\n"
                "in this whore of cities.</color>")
        assert self.markup.encode(text) == (
            "{C:$ffcccc}All things weird are normal\n"
            "in this whore of cities.")

    def test_encode__font(self):
        text = ("<font=sans>All things weird are normal\n"
                "in this whore of cities.</font>")
        assert self.markup.encode(text) == (
            "{F:sans}All things weird are normal\n"
            "in this whore of cities.")

    def test_encode__italic(self):
        text = ("All <i>things</i> weird are normal\n"
                "in <i>this</i> whore of cities.")
        assert self.markup.encode(text) == (
            "All things weird are normal\n"
            "in this whore of cities.")

    def test_encode__size(self):
        text = ("All things weird are normal\n"
                "<size=12>in this whore of cities</size>.")
        assert self.markup.encode(text) == (
            "All things weird are normal\n"
            "{s:12}in this whore of cities.")

    def test_encode__underline(self):
        text = ("All things weird are normal\n"
                "<u>in this whore of cities</u>.")
        assert self.markup.encode(text) == (
            "All things weird are normal\n"
            "{y:u}in this whore of cities.")

    def test_fontify(self):
        assert self.markup.fontify(self.text, "sans") == (
            "{F:sans}All things weird are normal\n"
            "in this whore of cities.")

    def test_italic_tag(self):
        assert self.markup.italic_tag.match("{Y:i}")
        assert self.markup.italic_tag.match("{y:i}")

    def test_italicize(self):
        assert self.markup.italicize(self.text) == (
            "{Y:i}All things weird are normal\n"
            "in this whore of cities.")

    def test_scale(self):
        assert self.markup.scale(self.text, 12) == (
            "{S:12}All things weird are normal\n"
            "in this whore of cities.")

    def test_tag(self):
        assert self.markup.tag.match("{y:ibu}")
        assert self.markup.tag.match("{c:$000000}")

    def test_underline(self):
        assert self.markup.underline(self.text, (0, 3)) == (
            "All things weird are normal\n"
            "in this whore of cities.")
