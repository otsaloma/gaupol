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

"""Text markup for the SubRip format."""

import aeidon
import re

__all__ = ("SubRip",)


class SubRip(aeidon.Markup):

    """
    Text markup for the SubRip format.

    SubRip format is assumed (based on the SubRip application GUI) to contain
    the following HTML-style tags, in either lower- or upper case.

     * ``<b>.........................</b>``
     * ``<i>.........................</i>``
     * ``<u>.........................</u>``
     * ``<font color="#RRGGBB">...</font>``
    """

    _flags = re.DOTALL | re.MULTILINE | re.IGNORECASE
    format = aeidon.formats.SUBRIP

    def bolden(self, text, bounds=None):
        """Return bolded `text`."""
        a, z = bounds or (0, len(text))
        return "".join((text[:a], "<b>{}</b>".format(text[a:z]), text[z:]))

    def clean(self, text):
        """Return `text` with less ugly markup."""
        # Remove tags that are immediately closed after opening.
        text = self._substitute(text, r"<([a-z]+)[^<]*?>( *)</\1>", r"\2")
        # Remove tags that are immediately opened after closing.
        text = self._substitute(text, r"</([a-z]+)>( *)<\1[^<]*?>", r"\2")
        # Remove or relocate space right after an opening tag.
        text = self._substitute(text, r" ?(<(?!/)[^>]+?>) ", r" \1")
        # Remove or relocate space right before a closing tag.
        text = self._substitute(text, r" (</[^>]+?>) ?", r"\1 ")
        return text

    def colorize(self, text, color, bounds=None):
        """Return `text` colorized to hexadecimal value."""
        a, z = bounds or (0, len(text))
        target = '<font color="#{}">{}</font>'.format(color, text[a:z])
        return "".join((text[:a], target, text[z:]))

    def fontify(self, text, font, bounds=None):
        """Return `text` changed to `font`."""
        a, z = bounds or (0, len(text))
        target = '<font face="{}">{}</font>'.format(font, text[a:z])
        return "".join((text[:a], target, text[z:]))

    @property
    def italic_tag(self):
        """Regular expression for an italic markup tag."""
        return self._get_regex(r"</?i>")

    def italicize(self, text, bounds=None):
        """Return italicized `text`."""
        a, z = bounds or (0, len(text))
        return "".join((text[:a], "<i>{}</i>".format(text[a:z]), text[z:]))

    def _main_decode(self, text):
        """Return `text` with decodable markup decoded."""
        text = self._decode_b(text, r"<b>(.*?)</b>", 1)
        text = self._decode_i(text, r"<i>(.*?)</i>", 1)
        text = self._decode_u(text, r"<u>(.*?)</u>", 1)
        text = self._decode_c(text, r'<color="#([0-9a-fA-F]{6})">(.*?)</color>', 1, 2)
        text = self._decode_f(text, r'<face="(.*?)">(.*?)</face>', 1, 2)
        text = self._decode_s(text, r'<size="(.*?)">(.*?)</size>', 1, 2)
        return text

    def _pre_decode(self, text):
        """Return `text` with markup prepared for decoding."""
        text = self._pre_decode_font(text)
        return text

    def _pre_decode_font(self, text):
        """
        Return `text` with font style tags separated and closing tags renamed.

        For example:

        ``<font size="12">...</font>``
        is replaced with ``<size="12">...</size>``

        ``<font size="12" font="sans">...</font>``
        is replaced with ``<size="12"><face="sans">...</size></face>``
        """
        open_pattern = r'<font ((?:(?:face|size|color)="[^"]*" ?)+)>'
        close_pattern = r'</font>'
        style_pattern = r'(face|size|color)="([^"]*)"'
        open_match, close_match = self._find_match_pair(text, open_pattern, close_pattern)
        if not open_match or not close_match: return text
        styles = re.findall(style_pattern, open_match.group(1))
        open_replacement = "".join(['<{}="{}">'.format(t[0], t[1]) for t in styles])
        close_replacement = "".join(['</{}>'.format(t[0]) for t in reversed(styles)])
        inner_text = text[open_match.end(): close_match.start()]
        replacement = open_replacement + inner_text + close_replacement
        text = "".join((text[:open_match.start()], replacement, text[close_match.end():]))
        return self._pre_decode_font(text)

    def scale(self, text, size, bounds=None):
        """Return `text` scaled to `size`."""
        a, z = bounds or (0, len(text))
        target = '<font size="{}">{}</font>'.format(size, text[a:z])
        return "".join((text[:a], target, text[z:]))

    def _find_match_pair(self, text, open_pattern, close_pattern, bounds=None):
        """
        Return first balanced pair of :class:`re.MatchObject`
        that match provided patterns in `text`.

        Returns `(None, None)` if tags are unbalanced or if no matches are found.
        """
        depth = 0
        a, z = bounds or (0, len(text))
        open_regex = self._get_regex(open_pattern)
        close_regex = self._get_regex(close_pattern)
        open_matches = [m for m in open_regex.finditer(text, pos=a, endpos=z)]
        if not open_matches: return (None, None)
        close_matches = [m for m in close_regex.finditer(text, pos=open_matches[0].end(), endpos=z)]
        matches = sorted(open_matches + close_matches, key=lambda m: m.start())
        for m in matches:
            if m.re.pattern == open_pattern:
                depth += 1
            elif m.re.pattern == close_pattern:
                depth -= 1
                if depth == 0:
                    return (open_matches[0], m)
        return (None, None)

    @property
    def tag(self):
        """Regular expression for any markup tag."""
        return self._get_regex(r"<.*?>")

    def underline(self, text, bounds=None):
        """Return underlined `text`."""
        a, z = bounds or (0, len(text))
        return "".join((text[:a], "<u>{}</u>".format(text[a:z]), text[z:]))
