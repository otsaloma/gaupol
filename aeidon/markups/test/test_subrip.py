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


class TestSubRip(aeidon.TestCase):

    text = ("All things weird are normal\n"
            "in this whore of cities.")

    def setup_method(self, method):
        self.markup = aeidon.markups.new(aeidon.formats.SUBRIP)

    def test_bolden(self):
        assert self.markup.bolden(self.text) == (
            "<b>All things weird are normal\n"
            "in this whore of cities.</b>")

    def test_clean__closing(self):
        text = ("All<i> things</i> weird are normal\n"
                "in <i> this</i> whore of cities.")
        assert self.markup.clean(text) == (
            "All <i>things</i> weird are normal\n"
            "in <i>this</i> whore of cities.")

    def test_clean__opening(self):
        text = ("All <i>things </i>weird are normal\n"
                "in <i>this </i> whore of cities.")
        assert self.markup.clean(text) == (
            "All <i>things</i> weird are normal\n"
            "in <i>this</i> whore of cities.")

    def test_colorize(self):
        assert self.markup.colorize(self.text, "ccffcc") == (
            '<font color="#ccffcc">All things weird are normal\n'
            'in this whore of cities.</font>')

    def test_decode__bold(self):
        text = ("<B>All things weird are normal\n"
                "in this whore of cities.</B>")
        assert self.markup.decode(text) == (
            "<b>All things weird are normal\n"
            "in this whore of cities.</b>")

    def test_decode__color(self):
        text = ('All things weird are normal\n'
                'in <font color="#ccccff">this whore of cities</font>.')
        assert self.markup.decode(text) == (
            "All things weird are normal\n"
            "in <color=#ccccff>this whore of cities</color>.")

    def test_decode__italic(self):
        text = ("<I>All</I> things weird are normal\n"
                "in this whore of cities.")
        assert self.markup.decode(text) == (
            "<i>All</i> things weird are normal\n"
            "in this whore of cities.")

    def test_decode__underline(self):
        text = ("All things weird are normal\n"
                "in this <U>whore</U> of cities.")
        assert self.markup.decode(text) == (
            "All things weird are normal\n"
            "in this <u>whore</u> of cities.")

    def test_encode__bold(self):
        text = ("<b>All things weird are normal\n"
                "in this whore of cities.</b>")
        assert self.markup.encode(text) == text

    def test_encode__color(self):
        text = ("<color=#ccccff>All things weird are normal\n"
                "in this whore of cities.</color>")
        assert self.markup.encode(text) == (
            '<font color="#ccccff">All things weird are normal\n'
            'in this whore of cities.</font>')

    def test_encode__font(self):
        text = ("<font=sans>All things weird are normal\n"
                "in this whore of cities.</font>")
        assert self.markup.encode(text) == self.text

    def test_encode__italic(self):
        text = ("All <i>things</i> weird are normal\n"
                "in <i>this</i> whore of cities.")
        assert self.markup.encode(text) == text

    def test_encode__size(self):
        text = ("All things weird are normal\n"
                "in this whore of <size=12>cities</size>.")
        assert self.markup.encode(text) == self.text

    def test_encode__underline(self):
        text = ("All things weird are normal\n"
                "<u>in this whore of cities.</u>")
        assert self.markup.encode(text) == text

    def test_italic_tag(self):
        assert self.markup.italic_tag.match("<i>")
        assert self.markup.italic_tag.match("</i>")

    def test_italicize(self):
        assert self.markup.italicize(self.text, (0, 3)) == (
            "<i>All</i> things weird are normal\n"
            "in this whore of cities.")

    def test_tag(self):
        assert self.markup.tag.match('<font color="#ffccff">')
        assert self.markup.tag.match('</font>')

    def test_underline(self):
        assert self.markup.underline(self.text, (45, 51)) == (
            "All things weird are normal\n"
            "in this whore of <u>cities</u>.")
