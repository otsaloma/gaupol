# -*- coding: utf-8 -*-

# Copyright (C) 2005-2009 Osmo Salomaa
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


class TestMarkup(aeidon.TestCase):

    text = ("All things weird are normal\n"
            "in this whore of cities.")

    def setup_method(self, method):
        self.markup = aeidon.Markup()

    def test_bolden(self):
        args = (self.markup.bolden, self.text)
        self.assert_raises(NotImplementedError, *args)

    def test_clean(self):
        text = self.markup.clean(self.text)
        assert text == self.text

    def test_colorize(self):
        args = (self.markup.colorize, self.text, "ff00ff")
        self.assert_raises(NotImplementedError, *args)

    def test_decode(self):
        text = self.markup.decode(self.text)
        assert text == self.text

    def test_encode__b(self):
        text = ("<b>All</b> things weird are normal\n"
                "in this whore of cities.")
        assert self.markup.encode(text) == self.text

    def test_encode__color(self):
        text = ('<color=#ffffff>All</color> things weird are normal\n'
                'in this whore of cities.')
        assert self.markup.encode(text) == self.text

    def test_encode__font(self):
        text = ('<font=Sans>All things weird are normal\n'
                'in this whore of cities.</font>')
        assert self.markup.encode(text) == self.text

    def test_encode__i(self):
        text = ("<i>All things weird are normal\n"
                "in this whore of cities.</i>")
        assert self.markup.encode(text) == self.text

    def test_encode__size(self):
        text = ('All things weird are normal\n'
                'in this whore of <size=12>cities</size>.')
        assert self.markup.encode(text) == self.text

    def test_encode__u(self):
        text = ("All things weird are normal\n"
                "in this whore of <u>cities</u>.")
        assert self.markup.encode(text) == self.text

    def test_fontify(self):
        args = (self.markup.fontify, self.text, "sans")
        self.assert_raises(NotImplementedError, *args)

    def test_italic_tag(self):
        assert self.markup.italic_tag is None

    def test_italicize(self):
        args = (self.markup.italicize, self.text)
        self.assert_raises(NotImplementedError, *args)

    def test_scale(self):
        args = (self.markup.scale, self.text, 12)
        self.assert_raises(NotImplementedError, *args)

    def test_tag(self):
        assert self.markup.tag is None

    def test_underline(self):
        args = (self.markup.underline, self.text)
        self.assert_raises(NotImplementedError, *args)
