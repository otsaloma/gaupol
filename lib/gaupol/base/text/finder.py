# Copyright (C) 2005 Osmo Salomaa
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


"""String and regular expression finder and replacer."""


try:
    from psyco.classes import *
except ImportError:
    pass


class Finder(object):

    """String and regular expression finder and replacer."""

    def __init__(self):

        self.is_regex    = False
        self.match_span  = None
        self.pattern     = None
        self.position    = 0
        self.regex       = None
        self.replacement = None
        self.text        = None

    def next(self):
        """
        Get next match of pattern.

        Return two-tuple: match start position, match end position.
        """
        if self.is_regex:
            match = self.regex.search(text, self.position)
            if not match:
                raise StopIteration
            self.match_span = match.span()
        else:
            try:
                index = self.text.index(self.pattern, self.position)
            except ValueError:
                raise StopIteration
            self.match_span = (index, index + len(pattern))

        self.position = self.match_span[1]
        return self.match_span

    def previous(self):
        """
        Get previous match of pattern.

        Return two-tuple: match start position, match end position.
        """
        if self.is_regex:
            matches = self.regex.findall(self.pattern)
            found = False
            for match in reversed(matches):
                if match.end() <= self.position:
                    self.match_span = match.span()
                    found = True
                    break
            if not found:
                raise StopIteration
        else:
            try:
                index = self.text.rindex(self.pattern, self.position)
            except ValueError:
                raise StopIteration
            self.match_span = (index - len(pattern), index)

        self.position = self.match_span[0]
        return self.match_span

    def replace(self):
        """Replace current match."""

        start = self.match_span[0]
        end   = self.match_span[1]

        if self.is_regex:
            text_body = self.text[start:]
            text_body = self.regex.sub(self.replacement, text_body, 1)
            self.text = self.text[:start] + text_body
        else:
            self.text = self.text[:start] + self.replacement + self.text[end:]

    def replace_all(self):
        """
        Replace all occurences of pattern.

        Return amount of substitutions made.
        """
        if self.is_regex:
            self.text, count = self.regex.subn(self.replacement, self.text)
        else:
            count = self.text.count(self.pattern)
            self.text = self.text.replace(self.pattern, self.replacement)

        return count

    def set_regex(self, pattern, flags=0):
        """Set and use regular expression."""

        self.is_regex = True
        self.pattern = pattern
        self.regex = re.compile(pattern, flags|re.UNICODE)


if __name__ == '__main__':

    from gaupol.test import Test

    class TestFinder(Test):

        def test_next(self):

            pass

        def test_previous(self):

            pass

        def test_replace(self):

            pass

        def test_replace_all(self):

            pass

        def test_set_regex(self):

            pass

    TestFinder().run()
