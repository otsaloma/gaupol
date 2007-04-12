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


"""Sub Station Alpha tag library."""


import re

from gaupol import util
from ._taglib import TagLibrary


class SubStationAlpha(TagLibrary):

    """Sub Station Alpha tag library.

    Class variables:

        _re_int_opening:     Regular expression for an internal opening tag
        _re_int_closing:     Regular expression for an internal closing tag
        _re_int_closing_end: Regular expression ... at the end of a subtitle
    """

    _re_int_opening = re.compile(r"<[^/].*?>")
    _re_int_closing = re.compile(r"</.*?>")
    _re_int_closing_end = re.compile(r"</.*?>\Z")

    @property
    @util.once
    def italic_tag(self):
        """Regular expression for an italic tag."""

        return re.compile(r"\{\\i[01]\}", re.IGNORECASE)

    @property
    @util.once
    def tag(self):
        """Regular expression for any tag."""

        return re.compile(r"\{.*?\}", 0)

    @util.once
    def _get_decode_tags(self):
        """Get list of tuples of regular expression, replacement, count."""

        FLAGS = re.IGNORECASE

        # These leave </> for reset and a lot of tags unclosed.
        tags = [
            # Bold opening
            (r"\{\\b[1-9]\d*\}", FLAGS,
                r"<b>", 1),
            # Italic opening
            (r"\{\\i1\}", FLAGS,
                r"<i>", 1),
            # Bold, Italic closing
            (r"\{\\(b|i)0\}", FLAGS,
                r"</\1>", 1),
            # Color
            (r"\{\\c&H([a-zA-Z0-9]{6})&\}", FLAGS,
                r'<color="#\1">', 1),
            # Font
            (r"\{\\fn(.*?)\}", FLAGS,
                r'<font="\1">', 1),
            # Size
            (r"\{\\fs(.*?)\}", FLAGS,
                r'<size="\1">', 1),
            # Reset
            (r"\{\\r\}", FLAGS,
                r"</>", 1),
            # Remove all else.
            (r"\{.*?\}", FLAGS,
                r"", 1),]

        for i, (pattern, flags, replacement, count) in enumerate(tags):
            tags[i] = (re.compile(pattern, flags), replacement, count)
        return tags

    @util.once
    def _get_encode_tags(self):
        """Get list of tuples of regular expression, replacement, count."""

        FLAGS = re.MULTILINE | re.DOTALL

        tags = [
            # Remove redundant style tags (e.g. </b><b>).
            (r"</(b|i|u)>(\n?)<\1>", FLAGS,
                r"\2", 3),
            # Remove other redundant tags.
            (r"<(.*?)=(.*?)>(.*?)</\1>(\n?)<\1=\2>", FLAGS,
                r"<\1=\2>\3\4", 3),
            # Bold and italic, \061 = 1
            (r"<(b|i)>", 0,
                r"{\\\1\061}", 1),
            # Bold and italic, \060 = 0
            (r"</(b|i)>", 0,
                r"{\\\1\060}", 1),
            # Color opening
            (r'<color="#(.*?)">', 0,
                r"{\\c&H\1&}", 1),
            # Font opening
            (r'<font="(.*?)">', 0,
                r"{\\fn\1}", 1),
            # Size opening
            (r'<size="(.*?)">', 0,
                r"{\\fs\1}", 1),
            # Color, font or size closing
            (r"</[a-z]{3,}>", 0,
                r"{\\r}", 1),
            # Remove underline.
            (r"</?u>", 0,
                r"", 1),]

        for i, (pattern, flags, replacement, count) in enumerate(tags):
            tags[i] = (re.compile(pattern, flags), replacement, count)
        return tags

    def _post_decode(self, text):
        """Fix or add closing tags."""

        parts = text.split("</>")
        for i, part in enumerate(parts):

            suffix = ""
            opening_tags = self._re_int_opening.findall(part)
            closing_tags = self._re_int_closing.findall(part)

            # Find out which tags have already been closed.
            for j in reversed(range(len(closing_tags))):
                closing_core = closing_tags[j][2:-1]
                for k in range(len(opening_tags)):
                    opening_core = opening_tags[k][1:-1].split("=")[0]
                    if opening_core == closing_core:
                        opening_tags.pop(k)
                        break

            # Assemble suffix string to close remaining tags.
            for j in reversed(range(len(opening_tags))):
                tag = "</" + opening_tags[j][1:-1].split("=")[0] + ">"
                suffix += tag

            parts[i] = part + suffix

        return "".join(parts)

    def _pre_decode(self, text):
        """Break combined tags, e.g. {\\b1i1} to {\\b1}{\\i1}."""

        parts = text.split("\\")
        for i in range(1, len(parts)):
            text_so_far = "\\".join(parts[:i])
            if text_so_far.endswith("{"):
                continue
            opening_index = text_so_far.rfind("{")
            closing_index = text_so_far.rfind("}")
            if opening_index > closing_index:
                parts[i - 1] += "}{"
        return "\\".join(parts)

    def _pre_encode(self, text):
        """Remove pointless closing tags at the end of the text."""

        while self._re_int_closing_end.search(text) is not None:
            text = self._re_int_closing_end.sub("", text)
        return text

    def decode(self, text):
        """Return text with tags converted from this to internal format."""

        text = self._pre_decode(text)
        for regex, replacement, count in self._get_decode_tags():
            for i in range(count):
                # pylint: disable-msg=E1101
                text = regex.sub(replacement, text)
        text = self._post_decode(text)
        return text

    def encode(self, text):
        """Return text with tags converted from internal to this format."""

        text = self._pre_encode(text)
        for regex, replacement, count in self._get_encode_tags():
            for i in range(count):
                # pylint: disable-msg=E1101
                text = regex.sub(replacement, text)
        return text

    def italicize(self, text):
        """Return italicized text."""

        return u"{\\i1}%s" % text
