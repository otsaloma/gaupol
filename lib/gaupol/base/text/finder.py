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


"""String and regular expression finder and replacer."""


import re


class Finder(object):

    """
    String and regular expression finder and replacer.

    Instance variables:

        ignore_case: True to ignore case
        match_span:  Tuple: start position, end position
        pattern:     String or regular expression object
        pos:         Current position
        replacement: String
        text:        Text

    """

    def __init__(self):

        self.ignore_case = False
        self.match_span  = None
        self.pattern     = None
        self.pos         = 0
        self.replacement = None
        self.text        = None

    def next(self):
        """
        Find next match of pattern.

        Raise StopIteration if no next match found.
        Return two-tuple: match start position, match end position.
        """
        if self.pos == len(self.text):
            raise StopIteration

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
            if not match:
                raise StopIteration
            if match.span() == self.match_span:
                if match.span() == (self.pos, self.pos):
                    self.pos = min(len(self.text), self.pos + 1)
                    return self.next()
            self.match_span = match.span()

        self.pos = self.match_span[1]
        return self.match_span

    def previous(self):
        """
        Find previous match of pattern.

        Raise StopIteration if no previous match found.
        Return two-tuple: match start position, match end position.
        """
        if self.pos == 0:
            raise StopIteration

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
                    candidate_match = iterator.next()
                    if candidate_match.end() <= self.pos:
                        match = candidate_match
                    else:
                        break
                except StopIteration:
                    break
            if match is None:
                raise StopIteration
            if match.span() == self.match_span:
                if match.span() == (self.pos, self.pos):
                    self.pos = max(0, self.pos - 1)
                    return self.previous()
            self.match_span = match.span()

        self.pos = self.match_span[0]
        return self.match_span

    def replace(self):
        """Replace current match."""

        a, z = self.match_span

        if isinstance(self.pattern, basestring):
            self.text = self.text[:a] + self.replacement + self.text[z:]
        else:
            text_body = self.text[a:]
            text_body = self.pattern.sub(self.replacement, text_body, 1)
            self.text = self.text[:a] + text_body

        self.pos = min(self.pos, len(self.text))

    def replace_all(self):
        """
        Replace all occurences of pattern.

        Return amount of substitutions made.
        """
        self.pos = 0
        count = 0
        try:
            while True:
                self.next()
                self.replace()
                count += 1
        except StopIteration:
            self.pos = min(self.pos, len(self.text))
            return count

    def set_regex(self, pattern, flags=0):
        """
        Set and use regular expression.

        re.UNICODE is automatically added to flags.
        """
        self.pattern = re.compile(pattern, flags|re.UNICODE)

    def set_text(self, text):
        """Set text."""

        self.text = text
        self.match_span = None
        self.pos = 0
