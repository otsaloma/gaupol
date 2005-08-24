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


"""Conversions between tags of different subtitle formats."""


import re

try:
    from psyco.classes import *
except ImportError:
    pass

from gaupol.constants import FORMAT
from gaupol.lib.tags.all import *


class TagConverter(object):
    
    """
    Conversions between tags of different subtitle formats.
    
    Tag conversions are done via an internal format, which has a HTML style
    syntax. All essential tags are converted and troublesome tags, such as
    position, and rare tags are removed.
    """
    
    def __init__(self, from_format, to_format):

        from_format_name = FORMAT.NAMES[from_format]
        to_format_name   = FORMAT.NAMES[  to_format]
        
        # Regular expressions
        from_tags = eval(from_format_name).DECODE_TAGS
        to_tags   = eval(  to_format_name).ENCODE_TAGS

        self._from_regexs = []
        self._to_regexs   = []

        PATTERN, FLAGS, REPL = 0, 1, 2

        for entry in from_tags:
            try:
                regex = re.compile(entry[PATTERN], entry[FLAGS])
            except TypeError:
                regex = re.compile(entry[PATTERN])
            self._from_regexs.append([regex, entry[REPL]])

        for entry in to_tags:
            try:
                regex = re.compile(entry[PATTERN], entry[FLAGS])
            except TypeError:
                regex = re.compile(entry[PATTERN])
            self._to_regexs.append([regex, entry[REPL]])
            
        # Arbitrary functions
        self._pre_decode  = eval(from_format_name).pre_decode
        self._post_decode = eval(from_format_name).post_decode
        self._pre_encode  = eval(to_format_name).pre_encode
        self._post_encode = eval(to_format_name).post_encode

    def convert_tags(self, text):
        """Convert subtitle tags in text."""

        if not text:
            return text

        REGEX, REPL = 0, 1

        # Convert to internal format ("decode").
        text = self._pre_decode(text)
        
        for entry in self._from_regexs:
            text = entry[REGEX].sub(entry[REPL], text)
            
        text = self._post_decode(text)
        
        # Convert to desired format ("encode").
        text = self._pre_encode(text)
        
        for entry in self._to_regexs:
            text = entry[REGEX].sub(entry[REPL], text)
            
        text = self._post_encode(text)

        return text
