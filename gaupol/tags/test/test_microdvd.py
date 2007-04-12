# Copyright (C) 2005-2007 Osmo Salomaa
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
from .. import microdvd


class TestMicroDVD(TestTagLibrary):

    def setup_method(self, method):

        self.taglib = microdvd.MicroDVD()

    def test_decode(self):

        # Style x3 (single line)
        text = \
            "{y:biu}All things weird are normal\n" + \
            "in this whore of cities."
        assert self.taglib.decode(text) == \
            "<b><i><u>All things weird are normal</u></i></b>\n" + \
            "in this whore of cities."

        # Style x2 (single line)
        text = \
            "All things {y:bi}weird are normal\n" + \
            "in this whore of cities."
        assert self.taglib.decode(text) == \
            "All things <b><i>weird are normal</i></b>\n" + \
            "in this whore of cities."

        # Style x1 (single line)
        text = \
            "All things weird are normal\n" + \
            "in this {y:i}whore of cities."
        assert self.taglib.decode(text) == \
            "All things weird are normal\n" + \
            "in this <i>whore of cities.</i>"

        # Style x1x2 (single lines)
        text = \
            "{y:i}All things weird are normal\n" + \
            "{y:i}in this whore of cities."
        assert self.taglib.decode(text) == \
            "<i>All things weird are normal</i>\n" + \
            "<i>in this whore of cities.</i>"

        # Style x3 (whole subtitle)
        text = \
            "{Y:biu}All things weird are normal\n" + \
            "in this whore of cities."
        assert self.taglib.decode(text) == \
            "<b><i><u>All things weird are normal\n" + \
            "in this whore of cities.</u></i></b>"

        # Style x2 (whole subtitle)
        text = \
            "All things {Y:bi}weird are normal\n" + \
            "in this whore of cities."
        assert self.taglib.decode(text) == \
            "All things <b><i>weird are normal\n" + \
            "in this whore of cities.</i></b>"

        # Style x1 (whole subtitle)
        text = \
            "All things weird are normal\n" + \
            "in this {Y:i}whore of cities."
        assert self.taglib.decode(text) == \
            "All things weird are normal\n" + \
            "in this <i>whore of cities.</i>"

        # Color (single line)
        text = \
            "{c:$ffffff}All things weird are normal\n" + \
            "in this whore of cities."
        assert self.taglib.decode(text) == \
            '<color="#ffffff">All things weird are normal</color>\n' + \
            'in this whore of cities.'

        # Color (whole subtitle)
        text = \
            "{C:$ffffff}All things weird are normal\n" + \
            "in this whore of cities."
        assert self.taglib.decode(text) == \
            '<color="#ffffff">All things weird are normal\n' + \
            'in this whore of cities.</color>'

        # Font (single line)
        text = \
            "All things {f:Sans}weird are normal\n" + \
            "in this whore of cities."
        assert self.taglib.decode(text) == \
            'All things <font="Sans">weird are normal</font>\n' + \
            'in this whore of cities.'

        # Font (whole subtitle)
        text = \
            "All things {F:Sans}weird are normal\n" + \
            "in this whore of cities."
        assert self.taglib.decode(text) == \
            'All things <font="Sans">weird are normal\n' + \
            'in this whore of cities.</font>'

        # Size (single line)
        text = \
            "All things weird are normal\n" + \
            "in this {s:12}whore of cities."
        assert self.taglib.decode(text) == \
            'All things weird are normal\n' + \
            'in this <size="12">whore of cities.</size>'

        # Size (whole subtitle)
        text = \
            "All things weird are normal\n" + \
            "in this {S:12}whore of cities."
        assert self.taglib.decode(text) == \
            'All things weird are normal\n' + \
            'in this <size="12">whore of cities.</size>'

        # Remove all other tags: position
        text = \
            "{P:0}All things weird are normal\n" + \
            "in this whore of cities."
        assert self.taglib.decode(text) == \
            "All things weird are normal\n" + \
            "in this whore of cities."

        # Remove all other tags: coordinate
        text = \
            "{o:5,5}All things weird are normal\n" + \
            "in this whore of cities."
        assert self.taglib.decode(text) == \
            "All things weird are normal\n" + \
            "in this whore of cities."

    def test_encode(self):

        # Style (affecting a single line subtitle fully)
        text = "<i>All things weird are normal</i>"
        assert self.taglib.encode(text) == \
            "{Y:i}All things weird are normal"

        # Style (affecting only one line)
        text = \
            "<b>All things weird are normal</b>\n" + \
            "in this whore of cities."
        assert self.taglib.encode(text) == \
            "{y:b}All things weird are normal\n" + \
            "in this whore of cities."

        # Style (affecting whole subtitle)
        text = \
            "<u>All things weird are normal</u>\n" + \
            "<u>in this whore of cities.</u>"
        assert self.taglib.encode(text) == \
            "{Y:u}All things weird are normal\n" + \
            "in this whore of cities."

    def test_encode_non_style(self):

        # Color (affecting a single line subtitle fully)
        text = '<color="#ffffff">All things weird are normal</color>'
        assert self.taglib.encode(text) == \
            "{C:$ffffff}All things weird are normal"

        # Color (affecting only one line)
        text = \
            'All things <color="#ffffff">weird are normal</color>\n' + \
            'in this whore of cities.'
        assert self.taglib.encode(text) == \
            "All things {c:$ffffff}weird are normal\n" + \
            "in this whore of cities."

        # Color (affecting whole subtitle)
        text = \
            'All things <color="#ffffff">weird are normal\n' + \
            'in this whore of cities.</color>'
        assert self.taglib.encode(text) == \
            "All things {C:$ffffff}weird are normal\n" + \
            "in this whore of cities."

        # Font (affecting a single line subtitle fully)
        text = '<font="Sans">All things weird are normal</font>'
        assert self.taglib.encode(text) == \
            "{F:Sans}All things weird are normal"

        # Font (affecting only one line)
        text = \
            '<font="Sans">All things</font> weird are normal\n' + \
            'in this whore of cities.'
        assert self.taglib.encode(text) == \
            "{f:Sans}All things weird are normal\n" + \
            "in this whore of cities."

        # Font (affecting whole subtitle)
        text = \
            '<font="Sans">All things weird are normal\n' + \
            'in this whore</font> of cities.'
        assert self.taglib.encode(text) == \
            "{F:Sans}All things weird are normal\n" + \
            "in this whore of cities."

        # Size (affecting a single line subtitle fully)
        text = '<size="12">All things weird are normal</size>'
        assert self.taglib.encode(text) == \
            "{S:12}All things weird are normal"

        # Size (affecting only one line)
        text = \
            'All things weird are normal\n' + \
            'in this <size="12">whore of cities.</size>'
        assert self.taglib.encode(text) == \
            "All things weird are normal\n" + \
            "in this {s:12}whore of cities."

        # Size (affecting whole subtitle)
        text = \
            'All things <size="12">weird are normal\n' + \
            'in this whore of cities.</size>'
        assert self.taglib.encode(text) == \
            "All things {S:12}weird are normal\n" + \
            "in this whore of cities."

    def test_italicize(self):

        text = \
            "All things weird are normal\n" + \
            "in this whore of cities."
        assert self.taglib.italicize(text) == \
            "{Y:i}All things weird are normal\n" + \
            "in this whore of cities."
