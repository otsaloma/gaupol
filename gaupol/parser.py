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


"""Text parser for tag-aware editing."""


from gaupol.finder import Finder


class Parser(Finder):

    """Text parser for tag-aware editing.

    Instance variables:

        re_tag:  Regular expression object to match any tag
        margins: Start tag, end tag that every line is wrapped in
        tags:    List of lists of tag, position

    The purpose of the Parser is to split text to the actual text and its tags,
    allowing the text to be edited while keeping the tags separate and intact.
    Parser can be used by first setting text to it, then performing operations
    via defined methods and finally getting the full text back.

    The margin system is only used if no other tags are found in the text and
    if the text has at least two lines. Either margins or tags will always be
    empty.
    """

    def __init__(self, re_tag=None):
        """Initialize Parser.

        re_tag should be a regular expression object.
        """
        Finder.__init__(self)

        self.re_tag  = re_tag
        self.margins = None
        self.tags    = None

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
        if not start_tag:
            return

        end_tag = ""
        while True:
            iterator = self.re_tag.finditer(line)
            match = None
            while True:
                try:
                    match = iterator.next()
                except StopIteration:
                    break
            if match is None:
                break
            a, z = match.span()
            if z != len(line):
                return
            end_tag = line[a:z] + end_tag
            line = line[:a]

        if all(list(x.startswith(start_tag) for x in lines)):
            if all(list(x.endswith(end_tag) for x in lines)):
                self.margins = [start_tag, end_tag]

    def _shift_tags(self, pos, shift, orig_text):
        """Shift all the tags after position."""

        if not shift or not self.tags:
            return

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
        for pos, tag in self.tags:
            if opening and pos <= pos_with_tags:
                pos_with_tags += len(tag)
            elif pos < pos_with_tags:
                pos_with_tags += len(tag)

        # Shift tags.
        for i in range(len(self.tags)):
            if opening and self.tags[i][0] > pos_with_tags:
                self.tags[i][0] += shift
            elif self.tags[i][0] >= pos_with_tags:
                self.tags[i][0] += shift
            if self.tags[i][0] < 0:
                self.tags[i][0] = 0

    def get_text(self):
        """Reassemble the text and return it."""

        text = self.text[:]
        for pos, tag in self.tags:
            text = text[:pos] + tag + text[pos:]
        if self.margins:
            text = text.replace("\n", "%s\n%s" % tuple(self.margins[::-1]))
            text = self.margins[0] + text + self.margins[1]
        return text

    def replace(self, next=True):
        """Replace the current match.

        next should be True to finish at end of match, False for beginning.
        """
        a = self.match_span[0]
        orig_text = self.text[:]
        Finder.replace(self, next)
        shift = len(self.text) - len(orig_text)
        self._shift_tags(a, shift, orig_text)

    def set_text(self, text, next=True):
        """Set the text and parse it.

        next should be True to start at beginning, False for end.
        """
        Finder.set_text(self, text, next)

        self.margins = []
        self.tags = []
        if self.re_tag is None:
            return
        if text.count("\n"):
            self._set_margins(text)
        if not self.margins:
            for match in self.re_tag.finditer(text):
                a, z = match.span()
                self.tags.append([a, text[a:z]])
        self.text = self.re_tag.sub("", text)
