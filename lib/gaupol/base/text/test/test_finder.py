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


import re

from gaupol.base.text.finder import Finder
from gaupol.test             import Test


ORIG_TEXT = \
"""One only risks it, because
one's survival depends on it."""


class TestFinder(Test):

    def setup_method(self, method):

        self.finder = Finder()
        self.finder.set_text(ORIG_TEXT)

    def test_next_regex_basic(self):

        self.finder.set_regex(r'\bit\b', re.MULTILINE)
        assert self.finder.next() == (15, 17)
        assert self.finder.match_span == (15, 17)
        assert self.finder.pos == 17
        assert self.finder.next() == (53, 55)
        assert self.finder.match_span == (53, 55)
        assert self.finder.pos == 55
        try:
            self.finder.next()
            raise AssertionError
        except StopIteration:
            pass

    def test_next_regex_ignore_case(self):

        self.finder.set_regex(r'o', re.MULTILINE|re.IGNORECASE)
        assert self.finder.next() == (0, 1)
        assert self.finder.match_span == (0, 1)
        assert self.finder.pos == 1

    def test_next_regex_last(self):

        self.finder.set_regex(r'\.', re.MULTILINE)
        assert self.finder.next() == (55, 56)
        assert self.finder.match_span == (55, 56)
        assert self.finder.pos == 56

    def test_next_string_basic(self):

        self.finder.pattern = 'it'
        assert self.finder.next() == (15, 17)
        assert self.finder.match_span == (15, 17)
        assert self.finder.pos == 17
        assert self.finder.next() == (53, 55)
        assert self.finder.match_span == (53, 55)
        assert self.finder.pos == 55
        try:
            self.finder.next()
            raise AssertionError
        except StopIteration:
            pass

    def test_next_string_ignore_case(self):

        self.finder.ignore_case = True
        self.finder.pattern = 'o'
        assert self.finder.next() == (0, 1)
        assert self.finder.match_span == (0, 1)
        assert self.finder.pos == 1

    def test_next_string_last(self):

        self.finder.pattern = '.'
        assert self.finder.next() == (55, 56)
        assert self.finder.match_span == (55, 56)
        assert self.finder.pos == 56

    def test_previous_regex_basic(self):

        self.finder.pos = len(ORIG_TEXT)
        self.finder.set_regex(r'\bit\b', re.MULTILINE)
        assert self.finder.previous() == (53, 55)
        assert self.finder.match_span == (53, 55)
        assert self.finder.pos == 53
        assert self.finder.previous() == (15, 17)
        assert self.finder.match_span == (15, 17)
        assert self.finder.pos == 15
        try:
            self.finder.previous()
            raise AssertionError
        except StopIteration:
            pass

    def test_previous_regex_ignore_case(self):

        self.finder.pos = len(ORIG_TEXT)
        self.finder.set_regex(r'o', re.MULTILINE|re.IGNORECASE)
        assert self.finder.previous() == (50, 51)
        assert self.finder.match_span == (50, 51)
        assert self.finder.pos == 50

    def test_previous_regex_last(self):

        self.finder.pos = len(ORIG_TEXT)
        self.finder.set_regex(r'\.', re.MULTILINE)
        assert self.finder.previous() == (55, 56)
        assert self.finder.match_span == (55, 56)
        assert self.finder.pos == 55

    def test_previous_string_basic(self):

        self.finder.pos = len(ORIG_TEXT)
        self.finder.pattern = 'it'
        assert self.finder.previous() == (53, 55)
        assert self.finder.match_span == (53, 55)
        assert self.finder.pos == 53
        assert self.finder.previous() == (15, 17)
        assert self.finder.match_span == (15, 17)
        assert self.finder.pos == 15
        try:
            self.finder.previous()
            raise AssertionError
        except StopIteration:
            pass

    def test_previous_string_ignore_case(self):

        self.finder.pos = len(ORIG_TEXT)
        self.finder.ignore_case = True
        self.finder.pattern = 'O'
        assert self.finder.previous() == (50, 51)
        assert self.finder.match_span == (50, 51)
        assert self.finder.pos == 50

    def test_previous_string_last(self):

        self.finder.pos = len(ORIG_TEXT)
        self.finder.pattern = '.'
        assert self.finder.previous() == (55, 56)
        assert self.finder.match_span == (55, 56)
        assert self.finder.pos == 55

    def test_replace_regex(self):

        self.finder.set_regex(r'\w', re.MULTILINE)
        self.finder.replacement = '_'
        self.finder.pos = len(self.finder.text)
        self.finder.previous()
        self.finder.replace()
        assert self.finder.text == \
            "One only risks it, because\n" \
            "one's survival depends on i_."
        self.finder.previous()
        self.finder.replace()
        assert self.finder.text == \
            "One only risks it, because\n" \
            "one's survival depends on __."

    def test_replace_string(self):

        self.finder.pattern = 'it'
        self.finder.replacement = '__'
        self.finder.next()
        self.finder.replace()
        assert self.finder.text == \
            "One only risks __, because\n" \
            "one's survival depends on it."
        self.finder.next()
        self.finder.replace()
        assert self.finder.text == \
            "One only risks __, because\n" \
            "one's survival depends on __."

    def test_replace_all_regex(self):

        self.finder.set_regex(r'\W', re.MULTILINE)
        self.finder.replacement = '_'
        assert self.finder.replace_all() == 12
        assert self.finder.text == \
            "One_only_risks_it__because_" \
            "one_s_survival_depends_on_it_"

    def test_replace_all_string(self):

        self.finder.ignore_case = True
        self.finder.pattern = 'o'
        self.finder.replacement = '__'
        assert self.finder.replace_all() == 4
        assert self.finder.text == \
            "__ne __nly risks it, because\n" \
            "__ne's survival depends __n it."

    def test_set_regex(self):

        self.finder.set_regex('test', re.DOTALL)
        assert self.finder.pattern.pattern == 'test'
        assert self.finder.pattern.flags == re.DOTALL|re.UNICODE

    def test_set_text(self):

        self.finder.set_text('test')
        assert self.finder.text == 'test'
        assert self.finder.match_span == None
        assert self.finder.pos == 0
