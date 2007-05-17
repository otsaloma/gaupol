# Copyright (C) 2006-2007 Osmo Salomaa
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


"""Splitter and merger of lines."""


from __future__ import division

import copy
import re

from gaupol import scriptlib
from gaupol.base import Contractual
from gaupol.parser import Parser


class Liner(Parser):

    """Splitter and merger of lines.

    Class variables:

        _re_multi_space: Regular expression for two or more spaces

    Instance variables:

        _length_func:  A function that returns the length of its argument
        _space_length: Length of a space according to length_func
        max_length:    Maximum length of a line in units of _length_func
        ok_clauses:    Amount of clause lines that need not be joined
        ok_dialogue:   Amount of dialogue lines that need not be joined
        re_clause:     Regular expression for a clause separator
        re_dialogue:   Regular expression for a dialogue separator

    re_clause and re_dialogue are required to have groups 'before' and 'after'
    surrounding a single space that acts as the separator.
    """

    __metaclass__ = Contractual
    _re_multi_space = re.compile(r" {2,}")

    def __init__(self, re_tag=None):
        """Initialize Liner.

        re_tag should be a regular expression object.
        """
        Parser.__init__(self, re_tag)

        self._length_func  = len
        self._space_length = 1
        self.max_length    = 44
        self.ok_clauses    = 2
        self.ok_dialogue   = 3
        self.re_clause     = None
        self.re_dialogue   = None

        pattern = scriptlib.get_clause_separator("latin-english")
        self.re_clause = re.compile(pattern, re.UNICODE)
        pattern = scriptlib.get_dialogue_separator("latin")
        self.re_dialogue = re.compile(pattern, re.UNICODE)

    def _get_length(self, lengths):
        """Get the length of units joined by spaces."""

        return (sum(lengths) + (len(lengths) - 1) * self._space_length)

    def _get_split_ensure(self, value, lengths):
        assert 0 <= value <= len(lengths)

    def _get_split(self, lengths):
        """Get index of split in two for units.

        Indexes are brute forced within reason and the result is optimal.
        """
        min_index = None
        min_diff = None
        unit_count = len(lengths)
        start = self._get_start_index(lengths, 2)
        for i in range(start, unit_count):
            a = self._get_length(lengths[:i])
            b = self._get_length(lengths[i:])
            diff = abs(a - b)
            if min_diff is None or diff < min_diff:
                min_index = i
                min_diff = diff
            if b < a:
                break
        return min_index

    def _get_splits_ensure(self, value, lengths, max_lines):
        for index in value:
            assert 0 <= index <= len(lengths)

    def _get_splits(self, lengths, max_lines):
        """Get indexes of splits for units."""

        if max_lines == 2:
            return [self._get_split(lengths)]
        if max_lines > 5 and max_lines % 2 == 0:
            return self._get_splits_ugly(lengths, max_lines)
        min_indexes = None
        min_squares = None
        unit_count = len(lengths)
        start = self._get_start_index(lengths, max_lines)
        for i in range(start, unit_count - max_lines + 2):
            indexes = self._get_splits(lengths[i:], max_lines - 1)
            indexes = [x + i for x in indexes]
            indexes.insert(0, i)
            borders = [0] + indexes + [unit_count]
            line_lengths = []
            for j in range(1, len(borders)):
                a, z = borders[j - 1:j + 1]
                line_lengths.append(self._get_length(lengths[a:z]))
            mean = sum(line_lengths) / max_lines
            squares = sum([(x - mean)**2 for x in line_lengths])
            if min_squares is None or round(min_squares - squares, 6) > 0:
                min_indexes = indexes
                min_squares = squares
            mean = self._get_length(lengths[i:]) / (max_lines - 1)
            if self._get_length(lengths[:i]) > mean:
                break
        return min_indexes

    def _get_splits_ugly_ensure(self, value, lengths, max_lines):
        for index in value:
            assert 0 <= index <= len(lengths)

    def _get_splits_ugly(self, lengths, max_lines):
        """Get unoptimal indexes of splits for units.

        Units are first split to groups of two, which are then split
        internally. The result is not optimal, but is obtained fast.
        """
        double_lengths = []
        unit_count = len(lengths)
        for i in range(1, unit_count):
            double_lengths.append(sum(lengths[i - 1:i + 1]))
        double_indexes = self._get_splits(double_lengths, int(max_lines / 2))
        borders = [0] + double_indexes + [unit_count]
        sub_indexes = []
        for i in range(1, len(borders)):
            a, z = borders[i - 1:i + 1]
            sub_indexes.append(self._get_split(lengths[a:z]) + a)
        return sorted(double_indexes + sub_indexes)

    def _get_start_index_ensure(self, value, lengths, max_lines):
        assert 0 <= value <= len(lengths)

    def _get_start_index(self, lengths, max_lines):
        """Get the index for the first split candidate for units.

        The start index is determined based on the line length mean with the
        purpose to avoid brute forcing insane indexes.
        """
        unit_count = len(lengths)
        if unit_count < 3:
            return 1
        mean = sum(lengths) / max_lines
        for i in range(2, unit_count):
            if self._get_length(lengths[:i]) > mean:
                return i - 1
        return 1

    def _join_even_ensure(self, value, max_lines):
        assert self.text.count("\n") == max_lines - 1

    def _join_even(self, max_lines):
        """Join the lines, each containing a logical unit, evenly."""

        if max_lines == 1:
            self.text = self.text.replace("\n", " ")
            return
        text = ""
        units = self.text.split("\n")
        lengths = [self._length_func(x) for x in units]
        indexes = self._get_splits(lengths, max_lines)
        for i in range(len(lengths)):
            prefix = ("\n" if i in indexes else " ")
            text = text + prefix + units[i]
        self.text = text.strip()

    def _split_on_clauses(self, max_lines):
        """Split the text to lines based on clauses.

        Return True if one or more splits made.
        """
        replacement = r"\g<before>\n\g<after>"
        self.text = self.re_clause.sub(replacement, self.text).strip()
        if not self.text.count("\n"):
            return False
        line_count = max(self.ok_clauses, max_lines)
        if self.text.count("\n") < line_count:
            return True
        self._join_even(line_count)
        return True

    def _split_on_dialogue(self, max_lines):
        """Split the text to lines based on dialogue.

        Return True if one or more splits made.
        """
        replacement = r"\g<before>\n\g<after>"
        self.text = self.re_dialogue.sub(replacement, self.text).strip()
        if not self.text.count("\n"):
            return False
        line_count = max(self.ok_dialogue, max_lines)
        if self.text.count("\n") < line_count:
            return True
        self._join_even(line_count)
        return True

    def _split_on_words(self, max_lines):
        """Split the text to lines based on words."""

        self.text = self.text.replace(" ", "\n")
        self.text = self.text.replace("\n-\n", "\n- ")
        if self.text.count("\n") < max_lines:
            return True
        self._join_even(max_lines)
        return True

    def format(self):
        """Format lines and return text."""

        self.text = self.text.replace("\n", " ")
        self.pattern = self._re_multi_space
        self.replacement = r" "
        self.replace_all()

        text = self.text
        tags = copy.deepcopy(self._tags)
        for max_lines in range(1, 100):
            for method in ("dialogue", "clauses", "words"):
                self.text = text
                self._tags = copy.deepcopy(tags)
                method = getattr(self, "_split_on_%s" % method)
                if method(max_lines) and self.is_legal():
                    return self.get_text()
        return self.get_text()

    def is_legal(self):
        """Return True if the text does not break self.max_length."""

        for line in self.text.split("\n"):
            if (" " in line) and (self._length_func(line) > self.max_length):
                return False
        return True

    def set_length_func_require(self, func):
        assert isinstance(func(""), int) or isinstance(func(""), float)

    def set_length_func(self, func):
        """Set the length function to use."""

        self._length_func = func
        self._space_length = func(" ")

    def set_text(self, text, next=True):
        """Set the text and parse it.

        next should be True to start at beginning, False for end.
        """
        Parser.set_text(self, text.strip(), next)
