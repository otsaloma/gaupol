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


"""Sub Station Alpha tag library."""


import re

from gaupol.base.tags import internal, TagLibrary


COMMON = re.MULTILINE|re.DOTALL


class SubStationAlpha(TagLibrary):

    """Sub Station Alpha tag library."""

    tag        = r'\{.*?\}'    , None
    italic_tag = r'\{\\i[01]\}', re.IGNORECASE

    encode_tags = [
        (
            # Remove duplicate style tags (e.g. <b>foo</b><b>bar</b>).
            r'</(b|i|u)>(\n?)<\1>', COMMON,
            r'\2'
        ), (
            # Remove other duplicate tags.
            r'<(.*?)=(.*?)>(.*?)</\1>(\n?)<\1=\2>', COMMON,
            r'<\1=\2>\3\4'
        ), (
            # Bold and italics
            # \061 = 1
            r'<(b|i)>', None,
            r'{\\\1\061}'
        ), (
            # Bold and italics
            # \060 = 0
            r'</(b|i)>', None,
            r'{\\\1\060}'
        ), (
            # Color
            r'<color="(.*?)">', None,
            r'{\\c&H\1}'
        ), (
            # Color
            r'</color.*?>', None,
            r'{\\r}'
        ), (
            # Font
            r'<font="(.*?)">', None,
            r'{\\fn\1}'
        ), (
            # Font
            r'</font.*?>', None,
            r'{\\r}'
        ), (
            # Size
            r'<size="(.*?)">', None,
            r'{\\fs\1}'
        ), (
            # Size
            r'</size.*?>', None,
            r'{\\r}'
        ), (
            # Remove underline
            r'</?u>', None,
            r''
        )
    ]

    @staticmethod
    def pre_encode(text):
        """Remove pointless closing tags at the end of the text."""

        while internal.re_closing_end.search(text):
            text = internal.re_closing_end.sub('', text)

        return text

    @staticmethod
    def italicize(text):
        """Italicize text."""

        return u'{\\i1}%s' % text

