# -*- coding: utf-8 -*-

# Copyright (C) 2011 Osmo Salomaa
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

"""Breaking lines to a specified width."""

import aeidon
import re
import sys

__all__ = ("Liner",)


class Liner(aeidon.Parser):

    """
    Breaking lines to a specified width.

    :ivar length_func: A function that returns the length of its argument
    :ivar max_length: Maximum length of a line in units of :attr:`length_func`
    :ivar max_lines: Maximum preferred amount of lines (may be exceeded)
    :ivar _penalties: List of penalty pattern dictionaries
    """

    # Reading Donald E. Knuth and Michael F. Plass's "Breaking Paragraphs into
    # Lines" from "Software--Practice and Experience" vol. 11 from 1981 is
    # recommended to understand the general problem of breaking a paragraph
    # of text into lines, the terminology used here as well of boxes, penalties
    # and demerits and the computational complexity of finding the optimal
    # solution in each case. Subtitling is in many ways a different
    # application, which is a lot simpler, but also more ambiguous and
    # subjective in terms of the minimized demerit measure.

    _re_multi_space = re.compile(r" {2,}")

    def __init__(self, re_tag=None, clean_func=None):
        """Initialize a :class:`Liner` instance."""
        aeidon.Parser.__init__(self, re_tag, clean_func)
        self._penalties = []
        self.length_func = len
        self.max_length = 40
        self.max_lines = 3

    def _boxes_to_lines(self, boxes, breaks):
        """Return `boxes` joined to form lines."""
        edges = [0] + [x + 1 for x in breaks] + [len(boxes)]
        return  [" ".join(boxes[edges[i]:edges[i+1]])
                 for i in range(len(edges) - 1)]

    def _break_lines(self, boxes, penalties, nlines):
        """
        Break `boxes` into lines and return break points and demerit.

        If keeping all boxes on a single line results in a valid and better
        result than splitting to `nlines` return an empty list. If no
        valid break points can be found, return ``None``.
        """
        breaks = self._list_possible_breaks(boxes, penalties, nlines)
        best_breaks = None
        best_demerit = sys.maxsize
        text = " ".join(boxes)
        if self.length_func(text) <= self.max_length:
            # Use a valid one-line solution as the benchmark,
            # that any more-line solution must beat.
            best_breaks = []
            best_demerit = self._calculate_demerit(boxes, penalties, [])
        if nlines == 1:
            return best_breaks, best_demerit
        if nlines == 2:
            for i in breaks:
                if penalties[i] > best_demerit: break
                demerit = self._calculate_demerit(boxes, penalties, [i])
                if demerit < best_demerit:
                    best_breaks = [i]
                    best_demerit = demerit
            return best_breaks, best_demerit
        # For more than two lines, loop over first break points and
        # recursively figure out rest of the breaks in each case.
        for i in breaks:
            # Use the maximum total negative penalty
            # that can accumulate from all later breaks.
            negpen = sorted(x for x in penalties[i+1:] if x < 0)
            negpen = sum(negpen[:min(len(negpen), nlines - 2)])
            if (penalties[i] + negpen) > best_demerit: break
            value = self._break_lines(boxes[i+1:], penalties[i+1:], nlines-1)
            if value[0] is None: continue
            later = [i + 1 + x for x in value[0]]
            demerit = self._calculate_demerit(boxes, penalties, [i] + later)
            if demerit < best_demerit:
                best_breaks = [i] + later
                best_demerit = demerit
        return best_breaks, best_demerit

    def break_lines(self):
        """Break lines and return text."""
        self.text = self.text.replace("\n", " ")
        self.pattern = self._re_multi_space
        self.replacement = " "
        self.replace_all()
        boxes = self.text.split(" ")
        if len(boxes) == 1:
            return self.get_text()
        penalties = self._detect_penalties(boxes)
        best_breaks = None
        best_demerit = sys.maxsize
        # We can probably handle up to ten lines of text
        # before finding break points gets intolerably slow.
        min_nlines = min(2, self.max_lines)
        max_nlines = min(10, len(boxes))
        for nlines in range(min_nlines, max_nlines + 1):
            breaks, demerit = self._break_lines(boxes, penalties, nlines)
            if breaks is None: continue
            if demerit < best_demerit:
                best_breaks = breaks
                best_demerit = demerit
            if nlines < self.max_lines:
                continue
            pos = -1
            for i in range(len(boxes)):
                pos = pos + 1 + len(boxes[i])
                text = self.text
                if i in best_breaks:
                    text = text[:pos] + "\n" + text[pos+1:]
                self.text = text
            return self.get_text()
        # If text cannot be broken, return original text.
        return self.get_text()

    def _calculate_demerit(self, boxes, penalties, breaks):
        """Return demerit measure for `boxes` broken by `breaks`."""
        nlines = len(breaks) + 1
        penalties = [penalties[i] for i in breaks]
        lines = self._boxes_to_lines(boxes, breaks)
        lengths = list(map(self.length_func, lines))
        mlength = sum(lengths) / len(lengths)
        xlength = self.max_length
        # Use two subjective measures of badness: (1) 'deviation',
        # which is the variance of line lengths relative to the
        # maximum line length and (2) upside-down 'pyramid', which
        # is the sum of how much longer each line is than the next.
        return (sum(penalties)
                + 50 * sum(((x - mlength) / xlength)**2 for x in lengths)
                + 50 * sum(((lengths[i] - lengths[i+1]) / xlength)**2
                           for i in range(len(lengths) - 1)
                           if lengths[i] > lengths[i+1])

                + 100 * (nlines-1)**3
                + 1000 * max(0, nlines - self.max_lines)**3)

    def _detect_penalties(self, boxes):
        """Detect penalties for break points following `boxes`."""
        text = " ".join(self._boxes_to_lines(boxes, breaks=[]))
        textpen = [0] * len(text)
        for penalty in self._penalties:
            self.pattern = penalty["regex"]
            self.pos = 0
            while True:
                try:
                    self.next()
                except StopIteration:
                    break
                start, end = self.match.span(penalty["group"])
                # Use sum, since in some rare cases multiple
                # patterns can match the same space.
                textpen[start] += penalty["value"]
        penalties = [0] * len(boxes)
        pos = -1
        for i in range(len(boxes) - 1):
            pos = pos + 1 + len(boxes[i])
            penalties[i] = textpen[pos]
        return penalties

    @aeidon.deco.memoize(100)
    def _list_possible_breaks(self, boxes, penalties, nlines):
        """
        Return a list of all possible break points for `boxes`.

        All break points that would necessarily cause `max_length` to be
        violated are discarded. Breaks are returned sorted in ascending order
        of associated `penalties`, so that all remaining breaks can be
        discarded once a demerit threshold is crossed.
        """
        breaks = list(range(len(boxes) - (nlines - 1)))
        breakpen = penalties[:len(breaks)]
        if nlines == 1:
            return []
        if nlines == 2:
            keep = [False] * len(breaks)
            for i in range(len(breaks)):
                lines = self._boxes_to_lines(boxes, breaks=[i])
                lengths = map(self.length_func, lines)
                keep[i] = max(lengths) <= self.max_length
            breaks = [breaks[i] for i in range(len(breaks)) if keep[i]]
            breakpen = [breakpen[i] for i in range(len(breakpen)) if keep[i]]
            # Sort breaks in ascending order by penalties,
            # so that all remaining breaks can be discarded once
            # a demerit threshold is crossed.
            if not breaks: return []
            points = sorted(zip(breakpen, breaks))
            breakpen, breaks = zip(*points)
            return(breaks)
        # For more than two lines, loop over first break points and
        # recursively figure out rest of the breaks in each case.
        keep = [False] * len(breaks)
        for i in range(len(breaks)):
            lines = self._boxes_to_lines(boxes, breaks=[i])
            alength = self.length_func(lines[0])
            if alength > self.max_length: break
            later = self._list_possible_breaks(boxes[i+1:],
                                               penalties[i+1:],
                                               nlines-1)

            keep[i] = bool(later)
        breaks = [breaks[i] for i in range(len(breaks)) if keep[i]]
        breakpen = [breakpen[i] for i in range(len(breakpen)) if keep[i]]
        # Sort breaks in ascending order by penalties,
        # so that all remaining breaks can be discarded once
        # a demerit threshold is crossed.
        if not breaks: return []
        points = sorted(zip(breakpen, breaks))
        breakpen, breaks = zip(*points)
        return(breaks)

    def set_penalties(self, penalties):
        """
        Set penalty patterns.

        `penalties` should be a list of dictionaries with items "pattern",
        "flags", "group" and "value", where pattern is a regular expression
        with group parentheses around a space, group is the number of the group
        in pattern to hold the penalty of value. A negative penalty encourages
        a break and a positive penalty discourages.
        """
        self._penalties = []
        for penalty in penalties:
            regex = re.compile(penalty["pattern"], penalty["flags"])
            self._penalties.append(dict(regex=regex,
                                        group=penalty["group"],
                                        value=penalty["value"]))

    def set_text(self, text):
        """Set the target text to search in and parse it."""
        aeidon.Parser.set_text(self, text.strip())
        self.text = self.text.strip()
