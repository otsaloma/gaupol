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


"""Subtitle text tag converter."""


import re

from gaupol.tags import *


class TagConverter(object):

    """Subtitle text tag converter.

    Instance variables:

        _from_regexes: List of lists of regular expression, replacement, count
        _to_regexes:   List of lists of regular expression, replacement, count
        _pre_decode:   Tag conversion function
        _pre_encode:   Tag conversion function
        _post_decode:  Tag conversion function
        _post_encode:  Tag conversion function
    """

    def __init__(self, from_format, to_format):

        self._from_regexs = []
        for seq in eval(from_format.class_name).decode_tags:
            regex = re.compile(seq[0], seq[1])
            count = (seq[3] if len(seq) == 4 else 1)
            self._from_regexs.append([regex, seq[2], count])

        self._to_regexs = []
        for seq in eval(to_format.class_name).encode_tags:
            regex = re.compile(seq[0], seq[1])
            count = (seq[3] if len(seq) == 4 else 1)
            self._to_regexs.append([regex, seq[2], count])

        self._pre_decode  = eval(from_format.class_name).pre_decode
        self._post_decode = eval(from_format.class_name).post_decode
        self._pre_encode  = eval(to_format.class_name).pre_encode
        self._post_encode = eval(to_format.class_name).post_encode

    def convert(self, text):
        """Return text with tags converted."""

        if not text:
            return text

        # Convert to internal format ("decode").
        text = self._pre_decode(text)
        for regex, replacement, count in self._from_regexs:
            for i in range(count):
                text = regex.sub(replacement, text)
        text = self._post_decode(text)

        # Convert to desired format ("encode").
        text = self._pre_encode(text)
        for regex, replacement, count in self._to_regexs:
            for i in range(count):
                text = regex.sub(replacement, text)
        text = self._post_encode(text)

        return text
