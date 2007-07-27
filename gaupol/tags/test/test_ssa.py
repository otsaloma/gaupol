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
from .. import ssa


class TestSubStationAlpha(TestTagLibrary):

    def setup_method(self, method):

        self.taglib = ssa.SubStationAlpha()

    def test_decode(self):

        # Bold
        text = \
            "{\\b1}All things weird are normal\n" + \
            "in this whore of cities."
        assert self.taglib.decode(text) == \
            "<b>All things weird are normal\n" + \
            "in this whore of cities.</b>"

        # Italic
        text = \
            "All things {\\i1}weird{\\r} are normal\n" + \
            "in this whore of cities."
        assert self.taglib.decode(text) == \
            "All things <i>weird</i> are normal\n" + \
            "in this whore of cities."

        # Color
        text = \
            "{\\c&Hffffff&}All things weird are normal\n" + \
            "in this whore of cities."
        assert self.taglib.decode(text) == \
            '<color="#ffffff">All things weird are normal\n' + \
            'in this whore of cities.</color>'

        # Font
        text = \
            "All things {\\fnSans}weird are normal\n" + \
            "in this whore{\\r} of cities."
        assert self.taglib.decode(text) == \
            'All things <font="Sans">weird are normal\n' + \
            'in this whore</font> of cities.'

        # Size
        text = \
            "All things weird are normal\n" + \
            "in this {\\fs12}whore of cities."
        assert self.taglib.decode(text) == \
            'All things weird are normal\n' + \
            'in this <size="12">whore of cities.</size>'

        # Multiple
        text = \
            "{\\i1\\b1\\fs12}All things weird{\\i0} are normal\n" + \
            "in this whore{\\b0} of cities."
        assert self.taglib.decode(text) == \
            '<i><b><size="12">All things weird</i> are normal\n' + \
            'in this whore</b> of cities.</size>'

        # Remove all else.
        text = \
            "{\\s1}All things weird are normal\n" + \
            "in this whore of cities."
        assert self.taglib.decode(text) == \
            "All things weird are normal\n" + \
            "in this whore of cities."

    def test_encode(self):

        # Bold
        text = \
            "<b>All things weird are normal\n" + \
            "in this whore of cities.</b>"
        assert self.taglib.encode(text) == \
            "{\\b1}All things weird are normal\n" + \
            "in this whore of cities."

        # Italics
        text = \
            "All things <i>weird are normal\n" + \
            "in this whore</i> of cities."
        assert self.taglib.encode(text) == \
            "All things {\\i1}weird are normal\n" + \
            "in this whore{\\i0} of cities."

        # Color
        text = \
            '<color="#ffffff">All things weird are normal\n' + \
            'in this whore of cities.</color>'
        assert self.taglib.encode(text) == \
            "{\\c&Hffffff&}All things weird are normal\n" + \
            "in this whore of cities."

        # Font
        text = \
            '<font="Sans">All things weird are normal\n' + \
            'in this whore</font> of cities.'
        assert self.taglib.encode(text) == \
            "{\\fnSans}All things weird are normal\n" + \
            "in this whore{\\r} of cities."

        # Size
        text = \
            'All things <size="12">weird are normal\n' + \
            'in this whore of cities.</size>'
        assert self.taglib.encode(text) == \
            "All things {\\fs12}weird are normal\n" + \
            "in this whore of cities."

    def test_italicize(self):

        text = \
            "All things weird are normal\n" + \
            "in this whore of cities."
        assert self.taglib.italicize(text) == \
            "{\\i1}All things weird are normal\n" + \
            "in this whore of cities."
