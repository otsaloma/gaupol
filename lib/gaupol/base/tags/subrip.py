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


"""SubRip tag library."""


# No documentation found for SubRip format.
#
# Assumed tags:
# <b></b>
# <i></i>
# <u></u>


import re

from gaupol.base.tags import TagLibrary


class SubRip(TagLibrary):

    """SubRip tag library."""

    tag        = r'</?(b|i|u)>', re.IGNORECASE
    italic_tag = r'</?i>'      , re.IGNORECASE

    decode_tags = [
        (
            # Uppercase bold
            r'(</?)B>', None,
            r'\1b>'
        ), (
            # Uppercase italic
            r'(</?)I>', None,
            r'\1i>'
        ), (
            # Uppercase underline
            r'(</?)U>', None,
            r'\1u>'
        )
    ]

    encode_tags = [
        (
            # Color
            r'</?color.*?>', None,
            r''
        ), (
            # Font
            r'</?font.*?>', None,
            r''
        ), (
            # Size
            r'</?size.*?>', None,
            r''
        )
    ]

    @staticmethod
    def italicize(text):
        """Italicize text."""

        return u'<i>%s</i>' % text
