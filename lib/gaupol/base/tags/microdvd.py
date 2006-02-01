# Copyright (C) 2005 Osmo Salomaa
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


"""MicroDVD tag library."""


import re

from gaupol.base.tags import TagLibrary


COMMON = re.MULTILINE|re.DOTALL


class MicroDVD(TagLibrary):

    """MicroDVD tag library."""

    tag        = r'\{[a-z]:.*?\}', re.IGNORECASE
    italic_tag = r'\{y:i\}'      , re.IGNORECASE

    # decode_tags and encode_tags require multiple entries of the same tags to
    # cover overlapping matches. e.g. <b><i>test</i></b>, would require two
    # substitutions of pattern "<[bi]>.*?</[bi]>" to fully convert.

    decode_tags = [
        (
            # Style x3 (single line)
            r'\{y:(b|i|u).*?(b|i|u).*?(b|i|u)\}(.*?)$', COMMON,
            r'<\1><\2><\3>\4</\3></\2></\1>'
        ), (
            # Style x2 (single line)
            r'\{y:(b|i|u).*?(b|i|u)\}(.*?)$', COMMON,
            r'<\1><\2>\3</\2></\1>',
            2
        ), (
            # Style x1 (single line)
            r'\{y:(b|i|u)\}(.*?)$', COMMON,
            r'<\1>\2</\1>',
            3
        ), (
            # Style x3 (whole subtitle unit)
            r'\{Y:(b|i|u).*?(b|i|u).*?(b|i|u)\}(.*?)\Z', COMMON,
            r'<\1><\2><\3>\4</\3></\2></\1>'
        ), (
            # Style x2 (whole subtitle unit)
            r'\{Y:(b|i|u).*?(b|i|u)\}(.*?)\Z', COMMON,
            r'<\1><\2>\3</\2></\1>',
            2
        ), (
            # Style x1 (whole subtitle unit)
            r'\{Y:(b|i|u)\}(.*?)\Z', COMMON,
            r'<\1>\2</\1>',
            3
        ), (
            # Color (single line)
            r'\{c:\$([a-zA-Z0-9]{6})\}(.*?)$', COMMON,
            r'<color="#\1">\2</color>'
        ), (
            # Color (whole subtitle unit)
            r'\{C:\$([a-zA-Z0-9]{6})\}(.*?)\Z', COMMON,
            r'<color="#\1">\2</color>'
        ), (
            # Font (single line)
            r'\{f:(.*?)\}(.*?)$', COMMON,
            r'<font="\1">\2</font>'
        ), (
            # Font (whole subtitle unit)
            r'\{F:(.*?)\}(.*?)\Z', COMMON,
            r'<font="\1">\2</font>'
        ), (
            # Size (single line)
            r'\{s:(\d+)\}(.*?)$', COMMON,
            r'<size="\1">\2</size>'
        ), (
            # Size (whole subtitle unit)
            r'\{S:(\d+)\}(.*?)\Z', COMMON,
            r'<size="\1">\2</size>'
        ), (
            # Remove all other tags.
            r'\{.:.*?\}', re.IGNORECASE,
            r''
        )
    ]

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
            # Style (affecting a single line subtitle fully)
            r'\A<(b|i|u)>(.*?)</\1>\Z', re.MULTILINE,
            r'{Y:\1}\2',
            3
        ), (
            # Style (affecting only one line)
            r'<(b|i|u)>(.*?)</\1>', re.MULTILINE,
            r'{y:\1}\2',
            3
        ), (
            # Style (affecting whole subtitle unit)
            r'<(b|i|u)>(.*?)</\1>', COMMON,
            r'{Y:\1}\2',
            3
        ), (
            # Color (affecting a single line subtitle fully)
            r'\A<color="#(.{6})">(.*?)</color>\Z', re.MULTILINE,
            r'{C:$\1}\2'
        ), (
            # Color (affecting only one line)
            r'<color="#(.{6})">(.*?)</color>', re.MULTILINE,
            r'{c:$\1}\2'
        ), (
            # Color (affecting whole subtitle unit)
            r'<color="#(.{6})">(.*?)</color>', COMMON,
            r'{C:$\1}\2'
        ), (
            # Font (affecting a single line subtitle fully)
            r'\A<font="(.*?)">(.*?)</font>\Z', re.MULTILINE,
            r'{F:\1}\2'
        ), (
            # Font (affecting only one line)
            r'<font="(.*?)">(.*?)</font>', re.MULTILINE,
            r'{f:\1}\2'
        ), (
            # Font (affecting whole subtitle unit)
            r'<font="(.*?)">(.*?)</font>', COMMON,
            r'{F:\1}\2'
        ), (
            # Size (affecting a single line subtitle fully)
            r'\A<size="(.*?)">(.*?)</size>\Z', re.MULTILINE,
            r'{S:\1}\2'
        ), (
            # Size (affecting only one line)
            r'<size="(.*?)">(.*?)</size>', re.MULTILINE,
            r'{s:\1}\2'
        ), (
            # Size (affecting whole subtitle unit)
            r'<size="(.*?)">(.*?)</size>', COMMON,
            r'{S:\1}\2'
        )
    ]

    @staticmethod
    def italicize(text):
        """Italicize text."""

        return u'{Y:i}%s' % text
