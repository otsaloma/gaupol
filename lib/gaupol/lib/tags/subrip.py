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


import re

try:
    from psyco.classes import *
except ImportError:
    pass

from gaupol.lib.tags.taglib import TagLibrary

    
class SubRip(TagLibrary):

    """SubRip tag library."""

    TAG = r'</?(b|i|u)>', re.IGNORECASE

    ITALIC = '</?i>', re.IGNORECASE
    
    DECODE_TAGS = (
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
    )

    ENCODE_TAGS = (
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
    )

    def italicize(text):
        """Italicize text."""
        
        return u'<i>%s</i>' % text

    italicize = staticmethod(italicize)
