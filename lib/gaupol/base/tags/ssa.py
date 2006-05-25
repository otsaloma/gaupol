# Copyright (C) 2005-2006 Osmo Salomaa
#
# This file is part of Gaupol.
#
# Gaupol is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Gaupol is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Gaupol; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA


"""Sub Station Alpha tag library."""


import re

from gaupol.base.tags import Internal, TagLibrary


COMMON = re.MULTILINE|re.DOTALL


class SubStationAlpha(TagLibrary):

    """Sub Station Alpha tag library."""

    tag        = r'\{.*?\}'    , 0
    italic_tag = r'\{\\i[01]\}', re.IGNORECASE

    @staticmethod
    def pre_decode(text):
        """Break combined tags, e.g. {\\b1i1} to {\\b1}{\\i1}."""

        parts = text.split('\\')
        for i in range(1, len(parts)):
            text_so_far = '\\'.join(parts[:i])
            if text_so_far.endswith('{'):
                continue
            opening_index = text_so_far.rfind('{')
            closing_index = text_so_far.rfind('}')
            if opening_index > closing_index:
                parts[i - 1] += '}{'

        return '\\'.join(parts)

    # Decode tags leave </> for reset and a lot of tags unclosed.
    decode_tags = [
        (
            # Bold opening
            r'\{\\b[1-9]\d*\}', re.IGNORECASE,
            r'<b>'
        ), (
            # Italic opening
            r'\{\\i1\}', re.IGNORECASE,
            r'<i>'
        ), (
            # Bold, Italic closing
            r'\{\\(b|i)0\}', re.IGNORECASE,
            r'</\1>'
        ), (
            # Color
            r'\{\\c&H([a-zA-Z0-9]{6})&\}', re.IGNORECASE,
            r'<color="#\1">'
        ), (
            # Font
            r'\{\\fn(.*?)\}', re.IGNORECASE,
            r'<font="\1">'
        ), (
            # Size
            r'\{\\fs(.*?)\}', re.IGNORECASE,
            r'<size="\1">'
        ), (
            # Reset
            r'\{\\r\}', re.IGNORECASE,
            r'</>'
        ), (
            # Remove all else
            r'\{.*?\}', re.IGNORECASE,
            r''
        )
    ]

    @staticmethod
    def post_decode(text):
        """Fix/add closing tags."""

        re_opening_tag = re.compile(*Internal.opening_tag)
        re_closing_tag = re.compile(*Internal.closing_tag)

        parts = text.split('</>')
        for i, part in enumerate(parts):

            suffix       = ''
            opening_tags = re_opening_tag.findall(part)
            closing_tags = re_closing_tag.findall(part)

            # Find out which tags have already been closed.
            for j in reversed(range(len(closing_tags))):
                closing_core = closing_tags[j][2:-1]
                for k in range(len(opening_tags)):
                    opening_core = opening_tags[k][1:-1].split('=')[0]
                    if opening_core == closing_core:
                        opening_tags.pop(k)
                        break

            # Assemble suffix string to close remaining tags.
            for j in reversed(range(len(opening_tags))):
                tag = '</' + opening_tags[j][1:-1].split('=')[0] + '>'
                suffix += tag

            parts[i] = part + suffix

        return ''.join(parts)

    @staticmethod
    def pre_encode(text):
        """Remove pointless closing tags at the end of the text."""

        re_closing_tag_end = re.compile(*Internal.closing_tag_end)
        while re_closing_tag_end.search(text):
            text = re_closing_tag_end.sub('', text)

        return text

    encode_tags = [
        (
            # Remove duplicate style tags (e.g. <b>foo</b><b>bar</b>).
            r'</(b|i|u)>(\n?)<\1>', COMMON,
            r'\2',
            3
        ), (
            # Remove other duplicate tags.
            r'<(.*?)=(.*?)>(.*?)</\1>(\n?)<\1=\2>', COMMON,
            r'<\1=\2>\3\4',
            3
        ), (
            # Bold and italic
            # \061 = 1
            r'<(b|i)>', 0,
            r'{\\\1\061}'
        ), (
            # Bold and italic
            # \060 = 0
            r'</(b|i)>', 0,
            r'{\\\1\060}'
        ), (
            # Color opening
            r'<color="#(.*?)">', 0,
            r'{\\c&H\1&}'
        ), (
            # Font opening
            r'<font="(.*?)">', 0,
            r'{\\fn\1}'
        ), (
            # Size opening
            r'<size="(.*?)">', 0,
            r'{\\fs\1}'
        ), (
            # Color, font or size closing
            r'</[a-z]{3,}>', 0,
            r'{\\r}'
        ), (
            # Remove underline
            r'</?u>', 0,
            r''
        )
    ]

    @staticmethod
    def italicize(text):
        """Italicize text."""

        return u'{\\i1}%s' % text
