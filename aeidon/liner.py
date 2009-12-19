# Copyright (C) 2006-2007,2009 Osmo Salomaa
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
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# Gaupol. If not, see <http://www.gnu.org/licenses/>.

"""Breaker of text into lines according to preferred break points."""

from __future__ import division

import aeidon
import copy
import math
import re
import sys

__all__ = ("Liner",)


class Liner(aeidon.Parser):

    """Breaker of text into lines according to preferred break points.

    :class:`Liner` operates by first joining all lines by spaces and then
    trying different breaks. Breaks are tried first from :attr:`break_points`
    in the order they are defined and if that fails, lines are split at word
    boundaries. Lines are attempted to be broken so that the variance of line
    lengths is minimized, while satisfying legality constraints, of which
    :attr:`max_length` is never broken and :attr:`max_lines` is broken if
    absolutely necessary. Variance minimizing splits are sought using a brute
    force algorithm as long as the text is not abnormally long.
    :attr:`max_deviation` can be used to control the threshold for discarding
    legal solutions for subtitles with three or more lines and a variance too
    great for the subtitle to be typeset elegantly.

    :ivar _space_length: Length of a space according to :attr:`length_func`
    :ivar break_points: List of tuples of regex object, replacement
    :ivar length_func: A function that returns the length of its argument
    :ivar max_deviation: Maximum deviation for texts with three or more lines
    :ivar max_length: Maximum length of a line in units of :attr:`_length_func`
    :ivar max_lines: Maximum preferred amount of lines (may be exceeded)
    """

    __metaclass__ = aeidon.Contractual
    _re_multi_space = re.compile(r" {2,}")

    def __init__(self, re_tag=None, clean_func=None):
        """Initialize a :class:`Liner` object.

        `re_tag` should be a regular expression object.
        """
        aeidon.Parser.__init__(self, re_tag, clean_func)
        self._length_func = len
        self._space_length = 1
        self.break_points = []
        self.max_deviation = 0.16
        self.max_length = 44
        self.max_lines = 2

    def _break_on_pattern(self, max_lines, regex, replacement):
        """Break the text into lines based on `regex`.

        Return ``True`` if breaks made and result is elegant and legal.
        """
        # Prefer elegance over compactness by not using
        # a maximum line count less than the preferred maximum.
        max_lines = max(max_lines, self.max_lines)
        self.text = regex.sub(replacement, self.text).strip()
        if 0 < self.text.count("\n") < max_lines:
            if self.is_legal() and (not self._is_deviant()):
                # Success with one item per line.
                return True
        if self.text.count("\n") > 0:
            self._join_even(max_lines)
            if self.is_legal() and (not self._is_deviant()):
                # Success with multiple items spread evenly on lines.
                return True
        self.text = self.text.replace("\n", " ")
        return False

    def _break_on_words(self, max_lines):
        """Break the text into lines based on words."""
        self.text = self.text.replace(" ", "\n")
        self.text = self.text.replace("\n-\n", "\n- ")
        self._join_even(max_lines)
        if self.is_legal(): return True
        self.text = self.text.replace("\n", " ")
        return False

    def _get_length(self, lengths):
        """Return the length of items joined by spaces."""
        return (sum(lengths) + (len(lengths) - 1) * self._space_length)

    def _get_break_ensure(self, value, lengths):
        assert 0 <= value <= len(lengths)

    def _get_break(self, lengths):
        """Return index of break in two with minimum length difference.

        Index is brute forced within reason and the result is optimal.
        """
        min_index = 0
        min_diff = sys.maxint
        start = self._get_start_index(lengths, 2)
        for i in range(start, len(lengths)):
            a = self._get_length(lengths[:i])
            b = self._get_length(lengths[i:])
            diff = abs(a - b)
            if diff < min_diff:
                min_index = i
                min_diff = diff
            # End if already past halfway.
            if b < a: break
        return min_index

    def _get_breaks_ensure(self, value, lengths, max_lines):
        for index in value:
            assert 0 <= index <= len(lengths)

    def _get_breaks(self, lengths, max_lines):
        """Return indices of breaks with minimum length variance.

        Indexes are brute forced within reason and the result is optimal if
        ``max_lines`` is less than six, otherwise result is (potentially) ugly.
        """
        if max_lines == 1:
            return []
        if max_lines == 2:
            return [self._get_break(lengths)]
        if (max_lines > 5) or (sum(lengths) > (5 * self.max_length)):
            # Avoid slow brute forcing by combining items.
            return self._get_breaks_ugly(lengths, max_lines)
        return self._get_breaks_pretty(lengths, max_lines)

    def _get_breaks_pretty_ensure(self, value, lengths, max_lines):
        for index in value:
            assert 0 <= index <= len(lengths)

    def _get_breaks_pretty(self, lengths, max_lines):
        """Return indices of breaks with minimum length variance.

        Indexes are brute forced within reason and the result is optimal.
        """
        min_indices = []
        min_squares = sys.maxint
        start = self._get_start_index(lengths, max_lines)
        for i in range(start, len(lengths) - max_lines + 2):
            indices = self._get_breaks(lengths[i:], max_lines - 1)
            indices = [i] + [x + i for x in indices]
            borders = [0] + indices + [len(lengths)]
            line_lengths = []
            for j in range(1, len(borders)):
                a, z = borders[j - 1:j + 1]
                line_lengths.append(self._get_length(lengths[a:z]))
            mean = sum(line_lengths) / max_lines
            squares = sum([(x - mean)**2 for x in line_lengths])
            if round(min_squares - squares, 6) > 0:
                min_indices = indices
                min_squares = squares
            a = self._get_length(lengths[:i])
            b = self._get_length(lengths[i:])
            # End if remaining less than average line length.
            if a > (b / (max_lines - 1)): break
        return min_indices

    def _get_breaks_ugly_ensure(self, value, lengths, max_lines):
        for index in value:
            assert 0 <= index <= len(lengths)

    def _get_breaks_ugly(self, lengths, max_lines):
        """Return indices of breaks with minimum length variance.

        Items are first broken into half of ``max_lines`` and then each these
        lines is further broken internally into two. The result is not optimal,
        but is obtained fast.
        """
         # Splits can only be made to an even number of lines.
        if (max_lines % 2 != 0):
            max_lines = max_lines - 1
        indices = self._get_breaks(lengths, int(max_lines / 2))
        borders = [0] + indices + [len(lengths)]
        for i in range(1, len(borders)):
            a, z = borders[i - 1:i + 1]
            indices.append(self._get_break(lengths[a:z]) + a)
        return sorted(indices)

    def _get_length_func(self):
        """Return the length function used."""
        return self._length_func

    def _get_start_index_ensure(self, value, lengths, max_lines):
        assert 0 <= value <= len(lengths)

    def _get_start_index(self, lengths, max_lines):
        """Return the index for the first break candidate for items.

        The start index is determined based on the line length mean with the
        purpose to avoid brute forcing insanely small indices.
        """
        if len(lengths) < 3:
            return 1
        mean = sum(lengths) / max_lines
        for i in range(2, len(lengths)):
            a = self._get_length(lengths[:i])
            if a > mean:
                return i - 1
        return 1

    def _is_deviant(self):
        """Return ``True`` if line lengths deviate too much."""
        line_count = self.text.count("\n") + 1
        if line_count <= 2: return
        lengths = [self._length_func(x) for x in self.text.split("\n")]
        mean = sum(lengths) / line_count
        std = math.sqrt(sum([(x - mean)**2 for x in lengths]) / line_count)
        return ((std / self.max_length) > self.max_deviation)

    def _join_even_ensure(self, value, max_lines):
        assert self.text.count("\n") + 1 <= max_lines

    def _join_even(self, max_lines):
        """Join lines evenly so that ``max_lines`` is not violated."""
        text = ""
        items = self.text.split("\n")
        lengths = [self._length_func(x) for x in items]
        indices = self._get_breaks(lengths, max_lines)
        for i in range(len(items)):
            prefix = ("\n" if i in indices else " ")
            text = text + prefix + items[i]
        self.text = text.strip()

    def _set_length_func_require(self, func):
        assert isinstance(func(""), (int, float))

    def _set_length_func(self, func):
        """Set the length function to use."""
        self._length_func = func
        self._space_length = func(" ")

    def break_lines(self):
        """Break lines and return text."""
        self.text = self.text.replace("\n", " ")
        self.pattern = self._re_multi_space
        self.replacement = " "
        self.replace_all()
        text = self.text
        tags = copy.deepcopy(self._tags)
        for max_lines in range(1, 50):
            # Try preferred break points one by one.
            for regex, replacement in self.break_points:
                self.text = text
                self._tags = copy.deepcopy(tags)
                args = (max_lines, regex, replacement)
                if self._break_on_pattern(*args):
                    return self.get_text()
            # Fall back to breaking by words.
            self.text = text
            self._tags = copy.deepcopy(tags)
            if self._break_on_words(max_lines):
                return self.get_text()
        return self.get_text()

    def is_legal(self):
        """Return ``True`` if the text does not violate :attr:`max_length`."""
        for line in self.text.split("\n"):
            length = self._length_func(line)
            if (" " in line) and (length > self.max_length):
                return False
        return True

    def set_text(self, text, next=True):
        """Set the target text to search in and parse it.

        `next` should be ``True`` to start at beginning, ``False`` for end.
        """
        aeidon.Parser.set_text(self, text.strip(), next)
        self.text = self.text.strip()

    length_func = property(_get_length_func, _set_length_func)
