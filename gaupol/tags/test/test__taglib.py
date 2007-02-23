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


import re

from gaupol.unittest import TestCase
from .. import _taglib


class TestTagLibrary(TestCase):

    def _decode(self, text):

        text = self.cls.pre_decode(text)
        for seq in self.cls.decode_tags:
            regex = re.compile(*seq[:2])
            count = (seq[3] if len(seq) == 4 else 1)
            for i in range(count):
                text = regex.sub(seq[2], text)
        text = self.cls.post_decode(text)
        return text

    def _encode(self, text):

        text = self.cls.pre_encode(text)
        for seq in self.cls.encode_tags:
            regex = re.compile(*seq[:2])
            count = (seq[3] if len(seq) == 4 else 1)
            for i in range(count):
                text = regex.sub(seq[2], text)
        text = self.cls.post_encode(text)
        return text

    def setup_method(self, method):

        self.cls = _taglib.TagLibrary()

    def test_tag(self):

        if self.cls.tag is not None:
            re.compile(*self.cls.tag)

    def test_italic_tag(self):

        if self.cls.italic_tag is not None:
            re.compile(*self.cls.italic_tag)

    def test_decode(self):

        text = \
            "All things weird are normal\n" + \
            "in this whore of cities."
        assert self._decode(text) == text

    def test_encode(self):

        # Remove all tags: italic.
        text = \
            "<i>All things weird are normal\n" + \
            "in this whore of cities.</i>"
        assert self._encode(text) == \
            "All things weird are normal\n" + \
            "in this whore of cities."

        # Remove all tags: bold.
        text = \
            "<b>All</b> things weird are normal\n" + \
            "in this whore of cities."
        assert self._encode(text) == \
            "All things weird are normal\n" + \
            "in this whore of cities."

        # Remove all tags: underline.
        text = \
            "All things weird are normal\n" + \
            "in this whore of <u>cities</u>."
        assert self._encode(text) == \
            "All things weird are normal\n" + \
            "in this whore of cities."

        # Remove all tags: font
        text = \
            '<font="Sans">All things weird are normal\n' + \
            'in this whore of cities.</font>'
        assert self._encode(text) == \
            "All things weird are normal\n" + \
            "in this whore of cities."

        # Remove all tags: color
        text = \
            '<color="#ffffff">All</color> things weird are normal\n' + \
            'in this whore of cities.'
        assert self._encode(text) == \
            "All things weird are normal\n" + \
            "in this whore of cities."

        # Remove all tags: size
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
        assert self.cls.italicize(text) == text

    def test_remove_redundant(self):

        text = \
            "All things weird are normal\n" + \
            "in this whore of cities."
        assert self.cls.remove_redundant(text) == text
