# Copyright (C) 2005-2007 Osmo Salomaa
#
# This file is part of Gaupol.
#
# Gaupol is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# Gaupol is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# Gaupol.  If not, see <http://www.gnu.org/licenses/>.

"""Text parser for tag-aware editing."""

import gaupol

__all__ = ["Parser"]


class Parser(gaupol.Finder):

    """Text parser for tag-aware editing.

    Instance variables:
     * _margins: Start tag, end tag that every line is wrapped in
     * _tags: List of lists of tag, position
     * re_tag: Regular expression object to match any tag

    The purpose of the Parser is to split text to the actual text and its tags,
    allowing the text to be edited while keeping the tags separate and intact.
    Parser can be used by first setting text to it, then performing operations
    via the defined methods and finally getting the full text back.

    The margin system (wrapping each line in the same tags) is only used if no
    other tags are found in the text and if the text has at least two lines.
    Either margins or tags will always be empty.
    """

    __metaclass__ = gaupol.Contractual

    def __init__(self, re_tag=None):

        gaupol.Finder.__init__(self)
        self._margins = None
        self._tags = None
        self.re_tag = re_tag

    def _set_margins_require(self, text):
        assert self.re_tag is not None

    @gaupol.util.asserted_return
    def _set_margins(self, text):
        """Find the margin tags in text if such exist."""

        lines = text.split("\n")
        line = lines[0]
        start_tag = ""
        while True:
            match = self.re_tag.match(line)
            if match is None:
                break
            a, z = match.span()
            start_tag += line[a:z]
            line = line[z:]
        assert start_tag

        end_tag = ""
        while True:
            iterator = self.re_tag.finditer(line)
            match = gaupol.util.last(iterator)
            if match is None:
                break
            a, z = match.span()
            assert z == len(line)
            end_tag = line[a:z] + end_tag
            line = line[:a]

        if all([x.startswith(start_tag) for x in lines]):
            if all([x.endswith(end_tag) for x in lines]):
                self._margins = [start_tag, end_tag]

    def _set_tags_require(self, text):
        assert self.re_tag is not None

    def _set_tags(self, text):
        """Find tags in text."""

        for match in self.re_tag.finditer(text):
            a, z = match.span()
            self._tags.append([a, text[a:z]])

    @gaupol.util.asserted_return
    def _shift_tags(self, pos, shift, orig_text):
        """Shift all the tags after position."""

        assert shift
        assert self._tags

        # Shift tags at position if at a closing tag and shift is positive,
        # otherwise shift only tags after position. This should keep tags at
        # the very outer edges of words.
        opening = True
        if shift > 0:
            if pos < len(orig_text):
                if orig_text[pos].isspace():
                    opening = False
            elif pos == len(orig_text):
                opening = False

        # Get length of tags before position.
        pos_with_tags = pos
        for pos, tag in self._tags:
            if opening and pos <= pos_with_tags:
                pos_with_tags += len(tag)
            elif pos < pos_with_tags:
                pos_with_tags += len(tag)

        # Shift tags.
        for i in range(len(self._tags)):
            if opening and self._tags[i][0] > pos_with_tags:
                self._tags[i][0] += shift
            elif self._tags[i][0] >= pos_with_tags:
                self._tags[i][0] += shift
            if self._tags[i][0] < 0:
                self._tags[i][0] = 0

    def get_text(self):
        """Reassemble the text and return it."""

        text = self.text[:]
        for pos, tag in self._tags:
            text = text[:pos] + tag + text[pos:]
        if self._margins:
            text = text.replace("\n", "%s\n%s" % tuple(self._margins[::-1]))
            text = self._margins[0] + text + self._margins[1]
        return text

    def replace(self, next=True):
        """Replace the current match.

        next should be True to finish at end of match, False for beginning.
        Raise re.error if bad replacement.
        """
        a = self.match_span[0]
        orig_text = self.text[:]
        gaupol.Finder.replace(self, next)
        shift = len(self.text) - len(orig_text)
        self._shift_tags(a, shift, orig_text)

    @gaupol.util.asserted_return
    def set_text(self, text, next=True):
        """Set the text to search in and parse it.

        next should be True to start at beginning, False for end.
        """
        gaupol.Finder.set_text(self, text, next)
        self._margins = []
        self._tags = []
        assert self.re_tag is not None
        if text.count("\n"):
            self._set_margins(text)
        if not self._margins:
            self._set_tags(text)
        self.text = self.re_tag.sub("", text)
