# -*- coding: utf-8 -*-

# Copyright (C) 2005 Osmo Salomaa
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""String and regular expression finder and replacer."""

import re

__all__ = ("Finder",)


class Finder:

    """
    String and regular expression finder and replacer.

    :ivar ignore_case: ``True`` to ignore case when finding matches
    :ivar match: Regular expression object for the latest match of pattern
    :ivar match_span: Tuple of start and end position for match
    :ivar pattern: String or regular expression object to find
    :ivar pos: Current offset from the beginning of the text
    :ivar replacement: Plain- or regular expression replacement string
    :ivar text: Target text to find matches of pattern in
    """

    def __init__(self):
        """Initialize a :class:`Finder` instance."""
        self.ignore_case = False
        self.match = None
        self.match_span = None
        self.pattern = None
        self.pos = None
        self.replacement = None
        self.text = None

    def next(self):
        """
        Find the next match of pattern.

        Raise :exc:`StopIteration` if no next match found.
        Return tuple of match start, end position.
        """
        if self.pos is None:
            # Start new search from beginning.
            self.pos = 0
        if isinstance(self.pattern, str):
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
        else: # Regular expression
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

    def previous(self):
        """
        Find the previous match of pattern.

        Raise :exc:`StopIteration` if no previous match found.
        Return tuple of match start, end position.
        """
        if self.pos is None:
            # Start new search from end.
            self.pos = len(self.text)
        if isinstance(self.pattern, str):
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
        else: # Regular expression
            iterator = self.pattern.finditer(self.text)
            match = None
            while True:
                try:
                    candidate = next(iterator)
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

    def replace(self, next=True):
        """
        Replace the current match of pattern.

        `next` should be ``True`` to finish at end of match, ``False`` for
        beginning. Raise :exc:`re.error` if bad replacement.
        """
        a, z = self.match_span
        orig_length = len(self.text)
        replacement = self.replacement
        if not isinstance(self.pattern, str):
            replacement = self.match.expand(self.replacement)
        self.text = self.text[:a] + replacement + self.text[z:]
        shift = len(self.text) - orig_length
        self.pos = (z + shift) if next else a
        # Adapt match span to new text length to avoid
        # getting stuck with zero-length regular expressions.
        if next and (self.match_span[0] == self.match_span[1]):
            self.match_span = (self.pos, self.pos)

    def replace_all(self):
        """
        Replace all occurences of pattern.

        Raise :exc:`re.error` if bad replacement.
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
                break
            self.replace()
            count += 1
        return count

    def set_regex(self, pattern, flags=re.DOTALL|re.MULTILINE):
        """
        Set and use regular expression as pattern.

        The default value for `flags` is ``DOTALL`` and ``MULTILINE``.
        ``IGNORECASE`` is automatically added to flags if :attr:`ignore_case`
        is ``True``. Raise :exc:`re.error` if bad pattern.
        """
        if self.ignore_case:
            flags = flags | re.IGNORECASE
        self.pattern = re.compile(pattern, flags)

    def set_text(self, text):
        """Set the target text to search in and reset position."""
        self.text = text
        self.match = None
        self.match_span = None
        self.pos = None
