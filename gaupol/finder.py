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


"""String and regular expression finder and replacer."""


import gaupol
import re

__all__ = ["Finder"]


class Finder(object):

    """String and regular expression finder and replacer.

    Instance variables:
     * ignore_case: True to ignore case
     * match: Regular expression match object
     * match_span: Tuple of start and end position
     * pattern: String or regular expression object to find
     * pos: Current offset in text
     * replacement: Replacement string
     * text: Target text
    """

    __metaclass__ = gaupol.Contractual

    def __init__(self):

        self.ignore_case = False
        self.match = None
        self.match_span = None
        self.pattern = None
        self.pos = None
        self.replacement = None
        self.text = None

    def _invariant(self):
        if self.pos is not None:
            assert (0 <= self.pos <= len(self.text))

    def next_require(self):
        assert self.pattern is not None

    def next_ensure(self, value):
        for pos in value:
            assert (0 <= pos <= len(self.text))

    def next(self):
        """Find the next match of pattern.

        Raise StopIteration if no next match found.
        Return tuple of match start, end position.
        """
        if isinstance(self.pattern, basestring):
            text = self.text
            pattern = self.pattern
            if self.ignore_case:
                text = text.lower()
                pattern = pattern.lower()
            try:
                index = text.index(pattern, self.pos)
            except ValueError:
                raise StopIteration
            self.match_span = (index, index + len(pattern))
        else:
            match = self.pattern.search(self.text, self.pos)
            if match is None:
                raise StopIteration
            # Avoid getting stuck with zero-length regular expressions.
            if match.span() == self.match_span == (self.pos, self.pos):
                if self.pos == len(self.text):
                    raise StopIteration
                self.pos += 1
                return self.next()
            self.match = match
            self.match_span = match.span()

        self.pos = self.match_span[1]
        return self.match_span

    def previous_require(self):
        assert self.pattern is not None

    def previous_ensure(self, value):
        for pos in value:
            assert (0 <= pos <= len(self.text))

    def previous(self):
        """Find the previous match of pattern.

        Raise StopIteration if no previous match found.
        Return tuple of match start, end position.
        """
        if isinstance(self.pattern, basestring):
            text = self.text
            pattern = self.pattern
            if self.ignore_case:
                text = text.lower()
                pattern = pattern.lower()
            try:
                index = text.rindex(pattern, 0, self.pos)
            except ValueError:
                raise StopIteration
            self.match_span = (index, index + len(pattern))
        else:
            iterator = self.pattern.finditer(self.text)
            match = None
            while True:
                try:
                    candidate = iterator.next()
                    if candidate.end() > self.pos:
                        raise StopIteration
                except StopIteration:
                    break
                match = candidate
            if match is None:
                raise StopIteration
            # Avoid getting stuck with zero-length regular expressions.
            if match.span() == self.match_span == (self.pos, self.pos):
                if self.pos == 0:
                    raise StopIteration
                self.pos -= 1
                return self.previous()
            self.match = match
            self.match_span = match.span()

        self.pos = self.match_span[0]
        return self.match_span

    def replace_require(self, next=True):
        assert self.match_span is not None
        assert self.pattern is not None
        assert self.replacement is not None

    def replace(self, next=True):
        """Replace the current match.

        next should be True to finish at end of match, False for beginning.
        Raise re.error if bad replacement.
        """
        a, z = self.match_span
        orig_length = len(self.text)
        replacement = self.replacement
        if not isinstance(self.pattern, basestring):
            replacement = self.match.expand(self.replacement)
        self.text = self.text[:a] + replacement + self.text[z:]

        shift = len(self.text) - orig_length
        self.pos = ((z + shift) if next else a)

        # Adapt match span to new text length to avoid getting stuck with
        # zero-length regular expressions.
        if next and self.match_span[0] == self.match_span[1]:
            self.match_span = (self.pos, self.pos)

    def replace_all_require(self):
        assert self.pattern is not None
        assert self.replacement is not None

    def replace_all(self):
        """Replace all occurences of pattern.

        Raise re.error if bad replacement.
        Return the amount of substitutions made.
        """
        self.pos = 0
        self.match = None
        self.match_span = None
        count = 0
        while True:
            try:
                self.next()
            except StopIteration:
                self.pos = len(self.text)
                self.match_span = None
                return count
            self.replace()
            count += 1
        return count

    def set_regex(self, pattern, flags=0):
        """Set and use regular expression.

        DOTALL, MULTILINE and UNICODE are automatically added to flags.
        IGNORECASE is automatically added to flags if self.ignore_case is True.
        Raise re.error if bad pattern.
        """
        if self.ignore_case:
            flags = flags | re.IGNORECASE
        flags = flags | re.DOTALL | re.MULTILINE | re.UNICODE
        self.pattern = re.compile(pattern, flags)

    def set_text(self, text, next=True):
        """Set the text to search in.

        next should be True to start at beginning, False for end.
        """
        self.text = text
        self.match = None
        self.match_span = None
        self.pos = (0 if next else len(text))
