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

# pylint: disable-msg=W0104


from gaupol import unittest
from .. import taglib


class TestTagLibrary(unittest.TestCase):

    plain_text = \
        "All things weird are normal\n" + \
        "in this whore of cities."

    def setup_method(self, method):

        self.taglib = taglib.TagLibrary()

    def test_italic_tag(self):

        if self.taglib.italic_tag is not None:
            self.taglib.italic_tag.findall("test")

    def test_tag(self):

        if self.taglib.tag is not None:
            self.taglib.tag.findall("test")

    def test_decode(self):

        text = self.taglib.decode(self.plain_text)
        assert text == self.plain_text

    def test_encode(self):

        # Remove all tags: italic.
        text = \
            "<i>All things weird are normal\n" + \
            "in this whore of cities.</i>"
        assert self.taglib.encode(text) == self.plain_text

        # Remove all tags: bold.
        text = \
            "<b>All</b> things weird are normal\n" + \
            "in this whore of cities."
        assert self.taglib.encode(text) == self.plain_text

        # Remove all tags: underline.
        text = \
            "All things weird are normal\n" + \
            "in this whore of <u>cities</u>."
        assert self.taglib.encode(text) == self.plain_text

        # Remove all tags: font.
        text = \
            '<font="Sans">All things weird are normal\n' + \
            'in this whore of cities.</font>'
        assert self.taglib.encode(text) == self.plain_text

        # Remove all tags: color.
        text = \
            '<color="#ffffff">All</color> things weird are normal\n' + \
            'in this whore of cities.'
        assert self.taglib.encode(text) == self.plain_text

        # Remove all tags: size.
        text = \
            'All things weird are normal\n' + \
            'in this whore of <size="12">cities</size>.'
        assert self.taglib.encode(text) == self.plain_text
