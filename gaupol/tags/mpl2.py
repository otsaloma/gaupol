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


"""MPL2 tag library."""


import gaupol
import re

from .microdvd import MicroDVD


class MPL2(MicroDVD):

    """MPL2 tag library."""

    format = gaupol.FORMAT.MPL2

    @property
    @gaupol.util.once
    def italic_tag(self):
        """Regular expression for an italic tag."""

        return re.compile(r"(\{y:i\})|(/)", re.IGNORECASE)

    @property
    @gaupol.util.once
    def tag(self):
        """Regular expression for any tag."""

        return re.compile(r"(\{[a-z]:.*?\})|(\\|/|_)", re.IGNORECASE)

    @gaupol.util.once
    def _get_decode_tags(self):
        """Get list of tuples of regular expression, replacement, count."""

        FLAGS = re.MULTILINE | re.DOTALL

        tags = [
            # Italic (single line)
            (r"/(.*?)$", FLAGS,
                r"<i>\1</i>", 1),
            # Bold (single line)
            (r"\\(.*?)$", FLAGS,
                r"<b>\1</b>", 1),
            # Underline (single line)
            (r"_(.*?)$", FLAGS,
                r"<u>\1</u>", 1),
            # Remove redundant style tags (e.g. </b><b>).
            (r"</(b|i|u)>(\n?)<\1>", FLAGS,
                r"\2", 3),]

        for i, (pattern, flags, replacement, count) in enumerate(tags):
            tags[i] = (re.compile(pattern, flags), replacement, count)
        return tags + MicroDVD._get_decode_tags(self)

    def _encode_style(self, text):
        """Convert style tags to MPL2 style."""

        style_tags = [
            ("<i>", "</i>", "/" ),
            ("<b>", "</b>", "\\"),
            ("<u>", "</u>", "_" ),]

        for opening, closing, replacement in style_tags:
            opening_lenght = len(opening)
            closing_length = len(closing)
            while True:
                if not opening in text:
                    break
                a = text.index(opening)
                z = (text.index(closing) if closing in text else len(text))
                before = text[:a]
                middle = text[a + opening_lenght:z]
                after = text[z + closing_length:]
                lines = middle.split("\n")
                for i in range(1, len(lines)):
                    if not lines[i].startswith(replacement):
                        lines[i] = replacement + lines[i]
                middle = "\n".join(lines)
                text = before + replacement + middle + after
        return text

    def encode(self, text):
        """Return text with tags converted from internal to this format."""

        text = self._encode_style(text)
        return MicroDVD.encode(self, text)

    def italicize(self, text):
        """Return italicized text."""

        return "/" + text.replace("\n", "\n/")
