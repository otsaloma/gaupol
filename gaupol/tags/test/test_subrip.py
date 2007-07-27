# Copyright (C) 2005-2007 Osmo Salomaa
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
# A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# Gaupol.  If not, see <http://www.gnu.org/licenses/>.

from .test_taglib import TestTagLibrary
from .. import subrip


class TestSubRip(TestTagLibrary):

    def setup_method(self, method):

        self.taglib = subrip.SubRip()

    def test_decode(self):

        # Uppercase bold
        text = \
            "<B>All things weird are normal\n" + \
            "in this whore of cities.</B>"
        assert self.taglib.decode(text) == \
            "<b>All things weird are normal\n" + \
            "in this whore of cities.</b>"

        # Uppercase italic
        text = \
            "<I>All</I> things weird are normal\n" + \
            "in this whore of cities."
        assert self.taglib.decode(text) == \
            "<i>All</i> things weird are normal\n" + \
            "in this whore of cities."

        # Uppercase underline
        text = \
            "All things weird are normal\n" + \
            "in this whore of <U>cities</U>."
        assert self.taglib.decode(text) == \
            "All things weird are normal\n" + \
            "in this whore of <u>cities</u>."

    def test_encode(self):

        # Italic
        text = \
            "<i>All things weird are normal\n" + \
            "in this whore of cities.</i>"
        assert self.taglib.encode(text) == text

        # Bold
        text = \
            "<b>All</b> things weird are normal\n" + \
            "in this whore of cities.</b>"
        assert self.taglib.encode(text) == text

        # Underline
        text = \
            "All things weird are normal\n" + \
            "in this whore of <u>cities</u>."
        assert self.taglib.encode(text) == text

        # Remove font.
        text = \
            '<font="Sans">All things weird are normal\n' + \
            'in this whore of cities.</font>'
        assert self.taglib.encode(text) == self.plain_text

        # Remove color.
        text = \
            '<color="#ffffff">All</color> things weird are normal\n' + \
            'in this whore of cities.'
        assert self.taglib.encode(text) == self.plain_text

        # Remove size.
        text = \
            'All things weird are normal\n' + \
            'in this whore of <size="12">cities</size>.'
        assert self.taglib.encode(text) == self.plain_text

    def test_italicize(self):

        assert self.taglib.italicize(self.plain_text) == \
            "<i>All things weird are normal\n" + \
            "in this whore of cities.</i>"
