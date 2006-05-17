# Copyright (C) 2005-2006 Osmo Salomaa
#
# This file is part of Gaupol.
#
# Gaupol is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Gaupol is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Gaupol; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA


import re

from gaupol.base.text.finder import Finder
from gaupol.test             import Test


TEXT = '''\
One only risks it, because
one\'s survival depends on it.'''


class TestFinder(Test):

    def get_finder(self):

        finder = Finder()
        finder.text = TEXT
        return finder

    def test_init(self):

        Finder()

    def test_next(self):

        finder = self.get_finder()
        finder.pattern = 'it'
        assert finder.next() == (15, 17)
        assert finder.match_span == (15, 17)
        assert finder.pos == 17
        assert finder.next() == (53, 55)
        assert finder.match_span == (53, 55)
        assert finder.pos == 55
        try:
            finder.next()
            raise AssertionError
        except StopIteration:
            pass

        finder = self.get_finder()
        finder.ignore_case = True
        finder.pattern = 'o'
        assert finder.next() == (0, 1)
        assert finder.match_span == (0, 1)
        assert finder.pos == 1

        finder = self.get_finder()
        finder.pattern = '.'
        assert finder.next() == (55, 56)
        assert finder.match_span == (55, 56)
        assert finder.pos == 56

        finder = self.get_finder()
        finder.set_regex(r'\bit\b', re.MULTILINE)
        assert finder.next() == (15, 17)
        assert finder.match_span == (15, 17)
        assert finder.pos == 17
        assert finder.next() == (53, 55)
        assert finder.match_span == (53, 55)
        assert finder.pos == 55
        try:
            finder.next()
            raise AssertionError
        except StopIteration:
            pass

        finder = self.get_finder()
        finder.set_regex(r'o', re.MULTILINE|re.IGNORECASE)
        assert finder.next() == (0, 1)
        assert finder.match_span == (0, 1)
        assert finder.pos == 1

        finder = self.get_finder()
        finder.set_regex(r'\.', re.MULTILINE)
        assert finder.next() == (55, 56)
        assert finder.match_span == (55, 56)
        assert finder.pos == 56

        finder = self.get_finder()
        finder.set_regex(r'\W', re.MULTILINE)
        assert finder.next() == (3, 4)
        assert finder.match_span == (3, 4)
        assert finder.pos == 4
        assert finder.next() == (8, 9)
        assert finder.match_span == (8, 9)
        assert finder.pos == 9

    def test_previous(self):

        finder = self.get_finder()
        finder.pos = len(TEXT)
        finder.pattern = 'it'
        assert finder.previous() == (53, 55)
        assert finder.match_span == (53, 55)
        assert finder.pos == 53
        assert finder.previous() == (15, 17)
        assert finder.match_span == (15, 17)
        assert finder.pos == 15
        try:
            finder.previous()
            raise AssertionError
        except StopIteration:
            pass

        finder = self.get_finder()
        finder.pos = len(TEXT)
        finder.ignore_case = True
        finder.pattern = 'O'
        assert finder.previous() == (50, 51)
        assert finder.match_span == (50, 51)
        assert finder.pos == 50

        finder = self.get_finder()
        finder.pos = len(TEXT)
        finder.pattern = '.'
        assert finder.previous() == (55, 56)
        assert finder.match_span == (55, 56)
        assert finder.pos == 55

        finder = self.get_finder()
        finder.pos = len(TEXT)
        finder.set_regex(r'\bit\b', re.MULTILINE)
        assert finder.previous() == (53, 55)
        assert finder.match_span == (53, 55)
        assert finder.pos == 53
        assert finder.previous() == (15, 17)
        assert finder.match_span == (15, 17)
        assert finder.pos == 15
        try:
            finder.previous()
            raise AssertionError
        except StopIteration:
            pass

        finder = self.get_finder()
        finder.pos = len(TEXT)
        finder.set_regex(r'o', re.MULTILINE|re.IGNORECASE)
        assert finder.previous() == (50, 51)
        assert finder.match_span == (50, 51)
        assert finder.pos == 50

        finder = self.get_finder()
        finder.pos = len(TEXT)
        finder.set_regex(r'\.', re.MULTILINE)
        assert finder.previous() == (55, 56)
        assert finder.match_span == (55, 56)
        assert finder.pos == 55

    def test_replace(self):

        finder = self.get_finder()
        finder.pattern = 'it'
        finder.replacement = '__'
        finder.next()
        finder.replace()
        assert finder.text == \
            'One only risks __, because\n' \
            'one\'s survival depends on it.'
        finder.next()
        finder.replace()
        assert finder.text == \
            'One only risks __, because\n' \
            'one\'s survival depends on __.'

        finder = self.get_finder()
        finder.set_regex(r'\w', re.MULTILINE)
        finder.replacement = '_'
        finder.pos = len(finder.text)
        finder.previous()
        finder.replace()
        assert finder.text == \
            'One only risks it, because\n' \
            'one\'s survival depends on i_.'
        finder.previous()
        finder.replace()
        assert finder.text == \
            'One only risks it, because\n' \
            'one\'s survival depends on __.'

    def test_replace_all(self):

        finder = self.get_finder()
        finder.ignore_case = True
        finder.pattern = 'o'
        finder.replacement = '__'
        assert finder.replace_all() == 4
        assert finder.text == \
            '__ne __nly risks it, because\n' \
            '__ne\'s survival depends __n it.'

        finder = self.get_finder()
        finder.set_regex(r'\W', re.MULTILINE)
        finder.replacement = '_'
        assert finder.replace_all() == 12
        assert finder.text == \
            'One_only_risks_it__because_' \
            'one_s_survival_depends_on_it_'

    def test_set_regex(self):

        finder = self.get_finder()
        finder.set_regex('test', re.DOTALL)
        assert finder.pattern.pattern == 'test'
        assert finder.pattern.flags == re.DOTALL|re.UNICODE
