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


"""Text parser to allow tag-aware editing."""


from gaupol.base.text.finder import Finder


class Parser(Finder):

    """
    Text parser to allow tag-aware editing.

    Purpose of the Parser is to split text to the actual text and its tags,
    allowing the text to be edited while keeping the tags separate and intact.
    Parser can be used by first setting text to it, then performing operations
    on the pure text and finally getting the full text back.
    """

    def __init__(self, re_tag=None):

        Finder.__init__(self)

        self.re_tag = re_tag

        # List of lists: [position, tag]
        self.tags = None

    def get_text(self):
        """Reassemble text and return it."""

        text = self.text[:]
        for pos, tag in self.tags:
            text = text[:pos] + tag + text[pos:]

        return text

    def replace(self):
        """Replace current match."""

        start = self.match_span[0]
        len_before = len(self.text)
        Finder.replace(self)
        shift = len(self.text) - len_before
        self._shift_tags(start, shift)

    def set_text(self, text):
        """Set text and parse it."""

        self.tags = []

        if self.re_tag is None:
            self.text = text
            return

        for match in self.re_tag.finditer(text):
            start, end = match.span()
            self.tags.append([start, text[start:end]])

        self.text = self.re_tag.sub('', text)

    def _shift_tags(self, pos, shift):
        """Shift all tags at position or later."""

        # Get length of tags before position.
        pos_with_tags = pos
        for pos, tag in self.tags:
            if pos <= pos_with_tags:
                pos_with_tags += len(tag)

        # Shift tags.
        for i in range(len(self.tags)):
            if self.tags[i][0] > pos_with_tags:
                self.tags[i][0] += shift
                if self.tags[i][0] < 0:
                    self.tags[i][0] = 0
