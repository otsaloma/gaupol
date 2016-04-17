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

"""Text parser for markup-tag-aware text editing."""

import aeidon

__all__ = ("Parser",)


class Parser(aeidon.Finder):

    """
    Text parser for markup-tag-aware text editing.

    :ivar clean_func: Function to clean tags or ``None``
    :ivar _margins: Start tag, end tag that every line is wrapped in
    :ivar re_tag: Regular expression object to match any tag
    :ivar _tags: List of lists of markup tag, position

    The purpose of :class:`Parser` is to split text to the actual text and its
    markup tags, allowing the text to be edited while keeping its tags separate
    and intact. An example would be replacing all "i"s with "j"s without
    changing italic markup::

        >>> import re
        >>> parser = aeidon.Parser(re.compile(r"<.+?>"))
        >>> parser.set_text("<i>iii</i>")
        >>> parser.pattern = "i"
        >>> parser.replacement = "j"
        >>> parser.replace_all()
        3
        >>> parser.get_text()
        '<i>jjj</i>'

    """

    def __init__(self, re_tag=None, clean_func=None):
        """Initialize a :class:`Parser` instance."""
        aeidon.Finder.__init__(self)
        self.clean_func = clean_func
        self._margins = None
        self.re_tag = re_tag
        self._tags = None

    def get_text(self):
        """Reassemble the full text and return it."""
        if not self.text:
            self._margins = []
            self._tags = []
        text = self.text[:]
        for pos, tag in self._tags:
            text = text[:pos] + tag + text[pos:]
        if self._margins:
            text = text.replace("\n", "{1}\n{0}".format(*self._margins))
            text = self._margins[0] + text + self._margins[1]
        if self.clean_func is not None:
            text = self.clean_func(text)
        return text

    def replace(self, next=True):
        """
        Replace the current match of pattern.

        `next` should be ``True`` to finish at end of match, ``False`` for
        beginning. Raise :exc:`re.error` if bad replacement.
        """
        a = self.match_span[0]
        orig_text = self.text[:]
        aeidon.Finder.replace(self, next)
        shift = len(self.text) - len(orig_text)
        self._shift_tags(a, shift, orig_text)

    def _set_margins(self, text):
        """Find the margin markup tags in `text` if such exist."""
        lines = text.split("\n")
        line = lines[0]
        start_tag = ""
        while True:
            match = self.re_tag.match(line)
            if match is None: break
            a, z = match.span()
            start_tag += line[a:z]
            line = line[z:]
        if not start_tag: return
        if not all(x.startswith(start_tag) for x in lines): return
        end_tag = ""
        while True:
            iterator = self.re_tag.finditer(line)
            match = aeidon.util.last(iterator)
            if match is None: break
            a, z = match.span()
            if z != len(line): return
            end_tag = line[a:z] + end_tag
            line = line[:a]
        if not all(x.endswith(end_tag) for x in lines): return
        for line in (x[len(start_tag):-len(end_tag)] for x in lines):
            # Ensure that no other tags exists on any of the lines.
            if self.re_tag.search(line) is not None: return
        self._margins = [start_tag, end_tag]

    def _set_tags(self, text):
        """Find markup tags in `text`."""
        for match in self.re_tag.finditer(text):
            a, z = match.span()
            self._tags.append([a, text[a:z]])

    def set_text(self, text):
        """Set the target text to search in and parse it."""
        aeidon.Finder.set_text(self, text)
        self._margins = []
        self._tags = []
        if self.re_tag is None: return
        if text.count("\n"):
            self._set_margins(text)
        if not self._margins:
            self._set_tags(text)
        self.text = self.re_tag.sub("", text)

    def _shift_tags(self, pos, shift, orig_text):
        """Shift all markup tags after `pos`."""
        if not shift: return
        if not self._tags: return
        # Try to determine whether a tag at position pos would be an opening
        # or a closing tag, i.e. attached to the next or the previous word.
        opening = True
        if pos < len(orig_text):
            if orig_text[pos].isspace():
                opening = False
        elif pos == len(orig_text):
            opening = False
        closing = not opening
        # Get length of tags *before* position. Try to add strings (positive
        # shift) inside tags and remove strings (negative shift) after tags.
        pos_with_tags = pos
        for tag_pos, tag in self._tags:
            if shift > 0 and closing:
                if tag_pos < pos_with_tags:
                    pos_with_tags += len(tag)
            elif tag_pos <= pos_with_tags:
                pos_with_tags += len(tag)
        between_length = 0
        for i, (tag_pos, tag) in enumerate(self._tags):
            orig_end = pos_with_tags - shift + between_length
            if (shift < 0) and (pos_with_tags < tag_pos < orig_end):
                # If tag is in the middle of what is being removed, it must be
                # shifted to the start of the removal block, but not so far
                # that it would overlap with preceding tags.
                self._tags[i][0] = pos_with_tags + between_length
                between_length += len(tag)
            elif tag_pos >= pos_with_tags:
                self._tags[i][0] += shift
