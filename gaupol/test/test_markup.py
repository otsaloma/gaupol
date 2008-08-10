# Copyright (C) 2005-2008 Osmo Salomaa
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


class TestMarkup(gaupol.TestCase):

    text = "All things weird are normal\n" \
           "in this whore of cities."

    def setup_method(self, method):

        self.markup = gaupol.Markup()

    def test_bolden(self):

        args = (self.markup.bolden, self.text)
        self.raises(NotImplementedError, *args)

    def test_clean(self):

        text = self.markup.clean(self.text)
        assert text == self.text

    def test_colorize(self):

        args = (self.markup.colorize, self.text, "ff00ff")
        self.raises(NotImplementedError, *args)

    def test_decode(self):

        text = self.markup.decode(self.text)
        assert text == self.text

    def test_encode__b(self):

        text = "<b>All</b> things weird are normal\n" \
               "in this whore of cities."
        assert self.markup.encode(text) == self.text

    def test_encode__color(self):

        text = '<color=#ffffff>All</color> things weird are normal\n' \
               'in this whore of cities.'
        assert self.markup.encode(text) == self.text

    def test_encode__font(self):

        text = '<font=Sans>All things weird are normal\n' \
               'in this whore of cities.</font>'
        assert self.markup.encode(text) == self.text

    def test_encode__i(self):

        text = "<i>All things weird are normal\n" \
               "in this whore of cities.</i>"
        assert self.markup.encode(text) == self.text

    def test_encode__size(self):

        text = 'All things weird are normal\n' \
               'in this whore of <size=12>cities</size>.'
        assert self.markup.encode(text) == self.text

    def test_encode__u(self):

        text = "All things weird are normal\n" \
               "in this whore of <u>cities</u>."
        assert self.markup.encode(text) == self.text

    def test_fontify(self):

        args = (self.markup.fontify, self.text, "sans")
        self.raises(NotImplementedError, *args)

    def test_italic_tag(self):

        assert self.markup.italic_tag is None

    def test_italicize(self):

        args = (self.markup.italicize, self.text)
        self.raises(NotImplementedError, *args)

    def test_sizen(self):

        args = (self.markup.sizen, self.text, 12)
        self.raises(NotImplementedError, *args)

    def test_tag(self):

        assert self.markup.tag is None

    def test_underline(self):

        args = (self.markup.underline, self.text)
        self.raises(NotImplementedError, *args)
