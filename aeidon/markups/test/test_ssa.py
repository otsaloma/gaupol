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


class TestSubStationAlpha(aeidon.TestCase):

    text = ("All things weird are normal\n"
            "in this whore of cities.")

    def setup_method(self, method):
        self.markup = aeidon.markups.new(aeidon.formats.SSA)

    def test_bolden(self):
        assert self.markup.bolden(self.text) == (
            "{\\b1}All things weird are normal\n"
            "in this whore of cities.{\\b0}")

    def test_colorize(self):
        assert self.markup.colorize(self.text, "ccff00") == (
            "{\\c&H00ffcc&}All things weird are normal\n"
            "in this whore of cities.")

    def test_decode__bold(self):
        text = ("{\\b1}All things weird are normal\n"
                "in this whore of cities.{\\b0}")
        assert self.markup.decode(text) == (
            "<b>All things weird are normal\n"
            "in this whore of cities.</b>")

    def test_decode__color(self):
        text = ("All things weird are normal\n"
                "in {\\c&Hff&}this whore of cities.")
        assert self.markup.decode(text) == (
            "All things weird are normal\n"
            "in <color=#ff0000>this whore of cities.</color>")

    def test_decode__combined(self):
        text = ("{\\b1\\i1}All things weird are normal\n"
                "in this{\\i0\\b0} whore of cities.")
        assert self.markup.decode(text) == (
            "<b><i>All things weird are normal\n"
            "in this</i></b> whore of cities.")

    def test_decode__font(self):
        text = ("All things {\\fnsans}weird{\\r} are normal\n"
                "in this whore of cities.")
        assert self.markup.decode(text) == (
            "All things <font=sans>weird</font> are normal\n"
            "in this whore of cities.")

    def test_decode__italic(self):
        text = ("{\\i1}All{\\r} things weird are normal\n"
                "in this whore of cities.")
        assert self.markup.decode(text) == (
            "<i>All</i> things weird are normal\n"
            "in this whore of cities.")

    def test_decode__reset(self):
        text = ("{\\b1\\i1}All{\\i0} things weird are normal\n"
                "{\\fs12}in this whore of cities{\\r}.")
        assert self.markup.decode(text) == (
            "<b><i>All</i> things weird are normal\n"
            "<size=12>in this whore of cities</size></b>.")

    def test_decode__size(self):
        text = ("All things weird are normal\n"
                "{\\fs12}in this whore of cities.")
        assert self.markup.decode(text) == (
            "All things weird are normal\n"
            "<size=12>in this whore of cities.</size>")

    def test_encode__bold(self):
        text = ("<b>All things weird are normal\n"
                "in this whore of cities.</b>")
        assert self.markup.encode(text) == (
            "{\\b1}All things weird are normal\n"
            "in this whore of cities.{\\b0}")

    def test_encode__color(self):
        text = ("<color=#ccccff>All things weird are normal\n"
                "in this whore of cities.</color>")
        assert self.markup.encode(text) == (
            "{\\c&Hffcccc&}All things weird are normal\n"
            "in this whore of cities.")

    def test_encode__font(self):
        text = ("<font=sans>All things weird are normal\n"
                "in this whore of cities.</font>")
        assert self.markup.encode(text) == (
            "{\\fnsans}All things weird are normal\n"
            "in this whore of cities.")

    def test_encode__italic(self):
        text = ("All <i>things</i> weird are normal\n"
                "in <i>this</i> whore of cities.")
        assert self.markup.encode(text) == (
            "All {\\i1}things{\\i0} weird are normal\n"
            "in {\\i1}this{\\i0} whore of cities.")

    def test_encode__size(self):
        text = ("All things weird are normal\n"
                "in this whore of <size=12>cities</size>.")
        assert self.markup.encode(text) == (
            "All things weird are normal\n"
            "in this whore of {\\fs12}cities.")

    def test_encode__underline(self):
        text = ("All things weird are normal\n"
                "<u>in this whore of cities.</u>")
        assert self.markup.encode(text) == self.text

    def test_fontify(self):
        assert self.markup.fontify(self.text, "sans") == (
            "{\\fnsans}All things weird are normal\n"
            "in this whore of cities.")

    def test_italic_tag(self):
        assert self.markup.italic_tag.match("{\\i1}")
        assert self.markup.italic_tag.match("{\\i0}")

    def test_italicize(self):
        assert self.markup.italicize(self.text, (0, 3)) == (
            "{\\i1}All{\\i0} things weird are normal\n"
            "in this whore of cities.")

    def test_scale(self):
        assert self.markup.scale(self.text, 12) == (
            "{\\fs12}All things weird are normal\n"
            "in this whore of cities.")

    def test_tag(self):
        assert self.markup.tag.match("{\\b500}")
        assert self.markup.tag.match("{\\c&H&}")
