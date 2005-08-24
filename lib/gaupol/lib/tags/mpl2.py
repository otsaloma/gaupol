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

    ENCODE_TAGS = MicroDVD.ENCODE_TAGS
    
    def pre_encode(text):
        """Convert style tags to native MPL2 style tags."""
        
        style_tags = [
            ('<i>', '</i>', '/' ),
            ('<b>', '</b>', '\\'),
            ('<u>', '</u>', '_' ),
        ]
    
        for i in range(len(style_tags)):
    
            opening, closing, replacement = style_tags[i]
    
            while text.find(opening) != -1:
        
                # Get start and end positions of tag.
                start = text.find(opening)
                try:
                    end = text.index(closing)
                except ValueError:
                    end = len(text)
                
                # Divide text into parts.
                before = text[:start]
                middle = text[start + 3:end]
                after  = text[end   + 4:]
    
                # Add new style tags to beginning of each line.
                lines = middle.split('\n')
                for i in range(1, len(lines)):
                    if not lines[i].startswith(replacement):
                        lines[i] = replacement + lines[i]
                middle = '\n'.join(lines)
    
                # Reconstruct line.
                text = before + replacement + middle + after
        
        return text
        
    pre_encode  = staticmethod(pre_encode)

    def italicize(text):
        """Italicize text."""
        
        return '/' + text.replace('\n', '\n/')

    italicize = staticmethod(italicize)
