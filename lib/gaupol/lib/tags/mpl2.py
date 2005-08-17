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


"""MPL2 tag library."""

# Documentation:
# http://napisy.ussbrowarek.org/mpl2-eng.html
# 
# Basically:
# / starts italics
# \ starts bold
# _ starts underline
# 
# All above tags affect only single line.
# In addition, MicroDVD tags can be used in MPL2.


import re

try:
    from psyco.classes import *
except ImportError:
    pass

from gaupol.lib.tags.microdvd import MicroDVD
from gaupol.lib.tags.taglib import TagLibrary


COMMON = re.MULTILINE|re.DOTALL


class MPL2(TagLibrary):

    """MPL2 tag library."""

    TAG    = r'(\{[a-z]:.*?\})|(\\|/|_)', re.IGNORECASE
    ITALIC = r'(\{y:i\})|(/)'           , re.IGNORECASE

    DECODE_TAGS = [
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
        )
    ] + MicroDVD.DECODE_TAGS

    ENCODE_TAGS = []
    
    # Ugly hack get style tags at the start of every line, assuming subtitle
    # has a maximum of ten lines.
    style_tags = [
        (r'<i>', r'</i>', r'/' ),
        (r'<b>', r'</b>', r'\\'),
        (r'<u>', r'</u>', r'_' ),
    ]

    for i in range(10):
        for entry in style_tags:

            pattern  = r'%s(.*?)' % entry[0]
            pattern += r'\n(.*?)' * i
            pattern += r'%s' % entry[1]

            replacement = r'%s\1' % entry[2]
            for k in range(1, i + 1):
                replacement += r'\n%s\%d' % (entry[2], k + 1)

            ENCODE_TAGS.append((pattern, re.MULTILINE, replacement))
    
    ENCODE_TAGS += MicroDVD.ENCODE_TAGS

    def italicize(text):
        """Italicize text."""
        
        return '/' + text.replace('\n', '\n/')

    italicize = staticmethod(italicize)
