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


"""Text parser that allows text editing while keeping tags intact."""


# This parser is experimental and not enough tested.
#
# Possible problems with the "replace" and "substitute" methods:
# - Tags might overlap after shifting. (Is that a problem?)
# - Tags that were in the middle of a match might end up in the wrong place.


try:
    from psyco.classes import *
except ImportError:
    pass


STR, POS = 0, 1


class TextParser(object):

    """
    Text parser that allows text editing while keeping tags intact.

    Parser can be used by first setting text to it, then performing operations
    on the pure text and finally getting the full text back.

    text: Text without tags
    tags: List of tags, [[tag_string, start_pos], ...]
    """

    def __init__(self, re_tag=None):

        self.text   = None
        self.re_tag = re_tag
        self.tags   = None

    def get_text(self):
        """Reassemble text and return it."""

        text = self.text[:]

        for entry in self.tags:
            tag, start = entry
            text = text[:start] + tag + text[start:]

        return text

    def replace(self, pattern, replacement):
        """Perform simple string replacement on text."""

        while True:

            start = self.text.find(pattern)
            if start == -1:
                break

            # Perform replace.
            self.text = self.text.replace(pattern, replacement)

            # Shift tags.
            shift = len(replacement) - len(pattern)
            shift_start = start + len(replacement)

            for i in range(len(self.tags)):
                if self.tags[i][POS] >= shift_start:
                    self.tags[i][POS] += shift

    def set_text(self, text):
        """Set text and parse it for tags."""

        self.tags = []

        if self.re_tag is None:
            self.text = text
            return

        for match in self.re_tag.finditer(text):
            start, end = match.span()
            self.tags.append([text[start:end], start])

        self.text = re_tag.sub('', text)

    def substitute(self, regex, replacement):
        """Perform a regular expression substitution on text."""

        while True:

            match = regex.match(text)
            if match is None:
                break

            start, end = match.span()

            # Perform substitution.
            self.text = regex.sub(replacement, self.text)

            # Shift tags.
            shift = len(replacement) - (end - start)
            shift_start = start + len(replacement)

            for i in range(len(self.tags)):
                if self.tags[i][POS] >= shift_start:
                    self.tags[i][POS] += shift
