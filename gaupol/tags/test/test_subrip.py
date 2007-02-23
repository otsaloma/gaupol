# Copyright (C) 2005-2006 Osmo Salomaa
#
# This file is part of Gaupol.
#
# Gaupol is free software; you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.
#
# Gaupol is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# Gaupol; if not, write to the Free Software Foundation, Inc., 51 Franklin
# Street, Fifth Floor, Boston, MA 02110-1301, USA.


from .test__taglib import TestTagLibrary
from .. import subrip


class TestSubRip(TestTagLibrary):

    def setup_method(self, method):

        self.cls = subrip.SubRip

    def test_decode(self):

        # Uppercase bold
        text = \
            "<B>All things weird are normal\n" + \
            "in this whore of cities.</B>"
        assert self._decode(text) == \
            "<b>All things weird are normal\n" + \
            "in this whore of cities.</b>"

        # Uppercase italic
        text = \
            "<I>All</I> things weird are normal\n" + \
            "in this whore of cities."
        assert self._decode(text) == \
            "<i>All</i> things weird are normal\n" + \
            "in this whore of cities."

        # Uppercase underline
        text = \
            "All things weird are normal\n" + \
            "in this whore of <U>cities</U>."
        assert self._decode(text) == \
            "All things weird are normal\n" + \
            "in this whore of <u>cities</u>."

    def test_encode(self):

        # Keep style tags: italic.
        text = \
            "<i>All things weird are normal\n" + \
            "in this whore of cities.</i>"
        assert self._encode(text) == text

        # Keep style tags: bold.
        text = \
            "<b>All</b> things weird are normal\n" + \
            "in this whore of cities.</b>"
        assert self._encode(text) == text

        # Keep style tags: underline.
        text = \
            "All things weird are normal\n" + \
            "in this whore of <u>cities</u>."
        assert self._encode(text) == text

        # All unsupported tags: font
        text = \
            '<font="Sans">All things weird are normal\n' + \
            'in this whore of cities.</font>'
        assert self._encode(text) == \
            "All things weird are normal\n" + \
            "in this whore of cities."

        # All unsupported tags: color
        text = \
            '<color="#ffffff">All</color> things weird are normal\n' + \
            'in this whore of cities.'
        assert self._encode(text) == \
            "All things weird are normal\n" + \
            "in this whore of cities."

        # All unsupported tags: size
        text = \
            'All things weird are normal\n' + \
            'in this whore of <size="12">cities</size>.'
        assert self._encode(text) == \
            "All things weird are normal\n" + \
            "in this whore of cities."

    def test_italicize(self):

        text = \
            "All things weird are normal\n" + \
            "in this whore of cities."
        assert self.cls.italicize(text) == \
            "<i>All things weird are normal\n" + \
            "in this whore of cities.</i>"

    def test_remove_redundant(self):

        text = \
            "<i>All things weird are normal</i>\n" + \
            "<i>in this whore of cities.</i>"
        assert self.cls.remove_redundant(text) == text

        text = \
            "All things weird are normal\n" + \
            "in this</i>... <i>whore of cities."
        assert self.cls.remove_redundant(text) == \
            "All things weird are normal\n" + \
            "in this... whore of cities."
