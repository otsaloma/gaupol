# Copyright (C) 2005-2006 Osmo Salomaa
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


import re

from gaupol.base.tags          import TagLibrary
from gaupol.base.tags.microdvd import MicroDVD


COMMON = re.MULTILINE|re.DOTALL


class MPL2(TagLibrary):

    """MPL2 tag library."""

    tag        = r'(\{[a-z]:.*?\})|(\\|/|_)', re.IGNORECASE
    italic_tag = r'(\{y:i\})|(/)'           , re.IGNORECASE

    decode_tags = [
        (
            # Italic (single line)
            r'/(.*?)$', COMMON,
            r'<i>\1</i>'
        ), (
            # Bold (single line)
            r'\\(.*?)$', COMMON,
            r'<b>\1</b>'
        ), (
            # Underline (single line)
            r'_(.*?)$', COMMON,
            r'<u>\1</u>'
        ), (
            # Remove duplicate style tags (e.g. <b>test</b><b>test</b>).
            r'</(b|i|u)>(\n?)<\1>', COMMON,
            r'\2',
            3
        )
    ] + MicroDVD.decode_tags

    _style_tags = [
        ('<i>', '</i>', '/' ),
        ('<b>', '</b>', '\\'),
        ('<u>', '</u>', '_' ),
    ]

    @classmethod
    def pre_encode(cls, text):
        """Convert style tags to native MPL2 style tags."""

        for (opening, closing, replacement) in cls._style_tags:
            opening_lenght = len(opening)
            closing_length = len(closing)
            while True:
                try:
                    start = text.index(opening)
                except ValueError:
                    break
                try:
                    end = text.index(closing)
                except ValueError:
                    end = len(text)
                before = text[:start]
                middle = text[start + opening_lenght:end]
                after  = text[end + closing_length:]
                lines = middle.split('\n')
                for i in range(1, len(lines)):
                    if not lines[i].startswith(replacement):
                        lines[i] = replacement + lines[i]
                middle = '\n'.join(lines)
                text = before + replacement + middle + after

        return text

    encode_tags = MicroDVD.encode_tags

    @staticmethod
    def italicize(text):
        """Italicize text."""

        return '/' + text.replace('\n', '\n/')
