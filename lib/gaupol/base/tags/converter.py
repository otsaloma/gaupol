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


"""Conversions between tags of different formats."""


import re

from gaupol.base              import cons
from gaupol.base.tags.classes import *


class TagConverter(object):

    """
    Conversions between tags of different formats.

    Instance variables:

        _from_regexs: List of regex, replacement, count
        _to_regexs:   List of regex, replacement, count

    Tag conversions are done via an internal format, which has a HTML style
    syntax. All essential tags are converted and rest removed.
    """

    def __init__(self, from_format, to_format):

        self._from_regexs = []
        self._to_regexs   = []

        from_name = cons.Format.class_names[from_format]
        to_name   = cons.Format.class_names[to_format]
        from_tags = eval(from_name).decode_tags
        to_tags   = eval(to_name).encode_tags

        for entry in from_tags:
            regex = re.compile(entry[0], entry[1])
            try:
                count = entry[3]
            except IndexError:
                count = 1
            self._from_regexs.append([regex, entry[2], count])
        for entry in to_tags:
            regex = re.compile(entry[0], entry[1])
            try:
                count = entry[3]
            except IndexError:
                count = 1
            self._to_regexs.append([regex, entry[2], count])

        self._pre_decode  = eval(from_name).pre_decode
        self._post_decode = eval(from_name).post_decode
        self._pre_encode  = eval(to_name).pre_encode
        self._post_encode = eval(to_name).post_encode

    def convert(self, text):
        """Convert tags in text."""

        if not text:
            return text
        text = text[:]

        # Convert to internal format ('decode').
        text = self._pre_decode(text)
        for entry in self._from_regexs:
            for i in range(entry[2]):
                text = entry[0].sub(entry[1], text)
        text = self._post_decode(text)

        # Convert to desired format ('encode').
        text = self._pre_encode(text)
        for entry in self._to_regexs:
            for i in range(entry[2]):
                text = entry[0].sub(entry[1], text)
        text = self._post_encode(text)

        return text
