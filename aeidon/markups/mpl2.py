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

"""Text markup for the MPL2 format."""

import aeidon

from collections import OrderedDict

__all__ = ("MPL2",)


class MPL2(aeidon.markups.MicroDVD):

    """
    Text markup for the MPL2 format.

    MPL2 contains the following markup tags, all of which appear at the
    beginning of the line and affect up to the end of the line. In addition,
    any MicroDVD markup can be used.

     * ``\\...`` (bold)
     * ``/....`` (italic)
     * ``_....`` (underline)
    """

    format = aeidon.formats.MPL2

    def bolden(self, text, bounds=None):
        """Return bolded `text`."""
        return self._style_mpl2(text, "\\", bounds)

    @property
    def italic_tag(self):
        """Regular expression for an italic markup tag."""
        return self._get_regex(r"(^/)|(\{[Yy]:i\})")

    def italicize(self, text, bounds=None):
        """Return italicized `text`."""
        return self._style_mpl2(text, "/", bounds)

    def _main_decode(self, text):
        """Return `text` with decodable markup decoded."""
        text = self._decode_b(text, r"<\\>(.*?)</\\>", 1)
        text = self._decode_i(text, r"</>(.*?)<//>", 1)
        text = self._decode_u(text, r"<_>(.*?)</_>", 1)
        return aeidon.markups.MicroDVD._main_decode(self, text)

    def _pre_decode(self, text):
        """Return `text` with markup prepared for decoding."""
        text = self._pre_decode_identify(text)
        return aeidon.markups.MicroDVD._pre_decode(self, text)

    def _pre_decode_identify(self, text):
        """
        Return `text` with all tags identified and closed.

        ``\\``, ``/`` and ``_`` characters at the beginnings of lines are
        identified as tags and replaced with artificial tags ``<\\>``, ``</>``
        and ``<_>``. Closing tags are added to the ends of lines as artificial
        tags ``</\\>``, ``<//>`` and ``</_>``.
        """
        lines = text.split("\n")
        re_tag = self._get_regex(r"^([\\/_]+)(.*)$")
        for i, line in enumerate(lines):
            match = re_tag.search(line)
            if match is None: continue
            lines[i] = match.group(2)
            for tag in reversed(OrderedDict.fromkeys(match.group(1))):
                lines[i] = "<{}>{}</{}>".format(tag, lines[i], tag)
        return "\n".join(lines)

    def _style_mpl2(self, text, tag, bounds=None):
        """Return `text` wrapped in markup `tag`."""
        a, z = bounds or (0, len(text))
        prefix = text[:a].split("\n")[-1]
        suffix = text[z:].split("\n")[0]
        re_alpha = self._get_regex(r"\w")
        # Return plain text if bounds does not define an entire line or
        # subtitle and thus cannot be marked without side-effects.
        if re_alpha.search(prefix): return text
        if re_alpha.search(suffix): return text
        styled_text = text[a:z].replace("\n", "\n{}".format(tag))
        return "".join((text[:a], tag, styled_text, text[z:]))

    @property
    def tag(self):
        """Regular expression for any markup tag."""
        return self._get_regex(r"(^[\\/_]+)|(\{[CFSYcfsy]:.*?\})")

    def underline(self, text, bounds=None):
        """Return underlined `text`."""
        return self._style_mpl2(text, "_", bounds)
