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

"""Text markup for the Sub Station Alpha format."""

import aeidon
import re

__all__ = ("SubStationAlpha",)


class SubStationAlpha(aeidon.Markup):

    """
    Text markup for the Sub Station Alpha format.

    Sub Station Alpha format contains a lot of markup tags of which the
    following are of interest to us. The generic reset ``{\\r}`` is used to
    revert to regular text, i.e. to close all open tags. Most of the tagging
    methods, e.g. :meth:`colorize`, leave tags unclosed, instead of explicitly
    closing them and possibly other tags with ``{\\r}``. Usually this is not a
    problem as such tags tend to be applied to the whole subtitle.

     * ``{\\b1}...........{\\b0}``
     * ``{\\i1}...........{\\i0}``
     * ``{\\fnNAME}............``
     * ``{\\fsPOINTS}..........``
     * ``{\\c&HBBGGRR&}........``
     * ``.................{\\r}``

     The hexadecimal color value is in reverse order, ``BBGGRR`` instead of the
     normal ``RRGGBB``. Furthermore, leading zeros can be omitted,
     e.g. ``ff00`` can be used instead of ``00ff00``.
    """

    _flags = re.DOTALL | re.MULTILINE | re.IGNORECASE
    format = aeidon.formats.SSA

    # Defined here so that AdvSubStationAlpha can override them.
    _closing_pattern = r"\{\\([bi])0\}"
    _opening_pattern = r"\{\\(?![bi]0)(b|i|c|fn|fs).*?\}"
    _reset_pattern   = r"\{\\r\}"

    def bolden(self, text, bounds=None):
        """Return bolded `text`."""
        a, z = bounds or (0, len(text))
        target = "{{\\b1}}{}{{\\b0}}".format(text[a:z])
        return "".join((text[:a], target, text[z:]))

    def colorize(self, text, color, bounds=None):
        """Return `text` colorized to hexadecimal value."""
        a, z = bounds or (0, len(text))
        # Reverse the color value from RRGGBB to BBGGRR.
        color = "{}{}{}".format(color[4:], color[2:4], color[:2])
        target = "{{\\c&H{}&}}{}".format(color, text[a:z])
        return "".join((text[:a], target, text[z:]))

    def fontify(self, text, font, bounds=None):
        """Return `text` changed to `font`."""
        a, z = bounds or (0, len(text))
        target = "{{\\fn{}}}{}".format(font, text[a:z])
        return "".join((text[:a], target, text[z:]))

    @property
    def italic_tag(self):
        """Regular expression for an italic markup tag."""
        return self._get_regex(r"\{\\i[01]\}")

    def italicize(self, text, bounds=None):
        """Return italicized `text`."""
        a, z = bounds or (0, len(text))
        target = "{{\\i1}}{}{{\\i0}}".format(text[a:z])
        return "".join((text[:a], target, text[z:]))

    def _main_decode(self, text):
        """Return `text` with decodable markup decoded."""
        text = self._decode_b(text, r"\{\\b1\}(.*?)\{\\b[0\\]\}", 1)
        text = self._decode_c(text, r"\{\\c#(.+?)\}(.*?)\{\\c\\\}", 1, 2)
        text = self._decode_f(text, r"\{\\fn(.+?)\}(.*?)\{\\fn\\\}", 1, 2)
        text = self._decode_i(text, r"\{\\i1\}(.*?)\{\\i[0\\]\}", 1)
        text = self._decode_s(text, r"\{\\fs(\d+)\}(.*?)\{\\fs\\\}", 1, 2)
        return text

    def _post_decode(self, text):
        """Return `text` with markup finalized after decoding."""
        # Remove all unsupported markup tags.
        return self._substitute(text, r"\{\\.*?\}", "")

    def _pre_decode(self, text):
        """Return `text` with markup prepared for decoding."""
        text = self._pre_decode_break(text)
        text = self._pre_decode_reset(text)
        text = self._pre_decode_color(text)
        return text

    def _pre_decode_break(self, text):
        """
        Return `text` with combined markup tags separated.

        For example, ``{\\b1\\i1}`` is replaced with ``{\\b1}{\\i1}``.
        """
        parts = text.split("\\")
        for i in range(1, len(parts)):
            text_so_far = "\\".join(parts[:i])
            if text_so_far.endswith("{"): continue
            opening_index = text_so_far.rfind("{")
            closing_index = text_so_far.rfind("}")
            if opening_index > closing_index:
                parts[i - 1] += "}{"
        return "\\".join(parts)

    def _pre_decode_color(self, text):
        """
        Return `text` with colors converted to standard hexadecimal form.

        Color tags are converted from ``{\\c&HBBGGRR&}`` to ``{\\c#RRGGBB}``.
        """
        pattern = r"\{\\c&H([0-9a-fA-F]*)&\}"
        regex = self._get_regex(pattern)
        match = regex.search(text)
        if match is None: return text
        color = ("{:0>6s}".format(match.group(1))).replace(" ", "0")
        color = "{}{}{}".format(color[4:], color[2:4], color[:2])
        text = regex.sub(r"{{\\c#{}}}".format(color), text, 1)
        return self._pre_decode_color(text)

    def _pre_decode_reset(self, text):
        """
        Return `text` with all markup tags closed explicitly.

        Tags of form ``{\\nameVALUE}`` are closed with ``{\\name\\}``.
        The returned text will not contain reset ``{\\r}`` tags.
        """
        re_opening = self._get_regex(self._opening_pattern)
        re_closing = self._get_regex(self._closing_pattern)
        re_reset = self._get_regex(self._reset_pattern)
        parts = re_reset.split(text + "{\\r}")
        for i, part in enumerate(parts):
            opening_matches = [x for x in re_opening.finditer(part)]
            closing_matches = [x for x in re_closing.finditer(part)]
            # Find out which tags have already been closed.
            for j in reversed(range(len(closing_matches))):
                closing_core = closing_matches[j].group(1)
                for k in range(len(opening_matches)):
                    opening_core = opening_matches[k].group(1)
                    if opening_core == closing_core:
                        opening_matches.pop(k)
                        break
            # Add artificial closing tags to close remaining tags.
            for j in reversed(range(len(opening_matches))):
                parts[i] += "{{\\{}\\}}".format(opening_matches[j].group(1))
        return "".join(parts)

    def scale(self, text, size, bounds=None):
        """Return `text` scaled to `size`."""
        a, z = bounds or (0, len(text))
        target = "{{\\fs{}}}{}".format(str(size), text[a:z])
        return "".join((text[:a], target, text[z:]))

    @property
    def tag(self):
        """Regular expression for any markup tag."""
        return self._get_regex(r"\{\\.*?\}")
