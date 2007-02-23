# Copyright (C) 2006-2007 Osmo Salomaa
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
from .. import liner


class TestLiner(TestCase):

    def setup_method(self, method):

        self.liner = liner.Liner(re.compile(r"<.*?>"))

    def test__get_length(self):

        assert self.liner._get_length([3]) == 3
        assert self.liner._get_length([2, 3, 4]) == 11

    def test_format(self):

        text = \
            "- Isn't he off on Saturdays? " + \
            "- He changed shifts. " + \
            "- Didn't he tell you?"
        self.liner.set_text(text)
        assert self.liner.format() == \
            "- Isn't he off on Saturdays?\n" + \
            "- He changed shifts.\n" + \
            "- Didn't he tell you?"

        text = \
            "- Isn't he off on Saturdays? " + \
            "- He changed shifts. " + \
            "- Didn't he tell you? " + \
            "- Can you give him this when he next comes?"
        self.liner.set_text(text)
        assert self.liner.format() == \
            "- Isn't he off on Saturdays?\n" + \
            "- He changed shifts. - Didn't he tell you?\n" + \
            "- Can you give him this when he next comes?"

        text = \
            "Isn't he off on Saturdays? " + \
            "He changed shifts."
        self.liner.set_text(text)
        assert self.liner.format() == \
            "Isn't he off on Saturdays?\n" + \
            "He changed shifts."

        text = \
            "Isn't he off on Saturdays? " + \
            "He changed shifts. " + \
            "Didn't he tell you?"
        self.liner.set_text(text)
        assert self.liner.format() == \
            "Isn't he off on Saturdays?\n" + \
            "He changed shifts. Didn't he tell you?"

        text = "Isn't he off on Saturdays"
        self.liner.set_text(text)
        assert self.liner.format() == text

        text = \
            "Isn't he off on Saturdays " + \
            "He changed shifts " + \
            "Didn't he tell you?"
        self.liner.set_text(text)
        assert self.liner.format() == \
            "Isn't he off on Saturdays He\n" + \
            "changed shifts Didn't he tell you?"

        text = \
            "Isn't he off on Saturdays " + \
            "He changed shifts " + \
            "Didn't he tell you " + \
            "Can you give him this when he next comes"
        self.liner.set_text(text)
        assert self.liner.format() == \
            "Isn't he off on Saturdays He changed\n" + \
            "shifts Didn't he tell you Can you\n" + \
            "give him this when he next comes"

        text = "test " * 50
        self.liner.set_text(text)
        assert self.liner.format() == \
            "test test test test test test test test\n" + \
            "test test test test test test test test\n" + \
            "test test test test test test test test\n" + \
            "test test test test test test test test\n" + \
            "test test test test test test test test test\n" + \
            "test test test test test test test test test"

        text = "test " * 60
        self.liner.set_text(text)
        assert self.liner.format() == \
            "test test test test test test test test\n" + \
            "test test test test test test test test\n" + \
            "test test test test test test test test test\n" + \
            "test test test test test test test test\n" + \
            "test test test test test test test test test\n" + \
            "test test test test test test test test test\n" + \
            "test test test test test test test test test"

    def test_is_legal(self):

        text = "<i>I got to the restaurant a little early.</i>"
        self.liner.set_text(text)
        assert self.liner.is_legal()

        text = "<i>I got to the restaurant a little early little early.</i>"
        self.liner.set_text(text)
        assert not self.liner.is_legal()

        text = "He'soffdutytodayHe'soffdutytodayHe'soffdutytoday."
        self.liner.set_text(text)
        assert self.liner.is_legal()

    def test_set_length_func(self):

        def get_length(arg):
            return len(arg)**2 + 1
        self.liner.set_length_function(get_length)
        assert self.liner._length_func == get_length
        assert self.liner._space_length == 2

    def test_set_text(self):

        self.liner.set_text(" <i>foo</i> ")
        assert self.liner.text == "foo"
