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


"""Style tags for different subtitle file formats."""


class TagLibrary(object):

    """
    Base class for subtitle tag libraries.

    Class variables:

        tag:         Regular expression pattern, flags
        italic_tag:  Regular expression pattern, flags
        decode_tags: List of tuples: pattern, flags, replacement[, count]
        encode_tags: List of tuples: pattern, flags, replacement[, count]

    decode_tags is a list of regular expressions that convert tags to the
    internal format. encode_tags convert from the internal format to the
    class's format. The fourth item in the decode_tags and encode_tags tuple is
    an optional integer that tells how many times the substitution should be
    performed (default is one).

    pre- and post, -decode and -encode functions can be used to perform
    arbitrary tasks in tag conversion. pre-methods are run before regular
    exressions and post-methods after.
    """

    tag        = '', 0
    italic_tag = '', 0

    @classmethod
    def pre_decode(cls, text):
        """Convert tags."""

        return text

    decode_tags = []

    @classmethod
    def post_decode(cls, text):
        """Convert tags."""

        return text

    @classmethod
    def pre_encode(cls, text):
        """Convert tags."""

        return text

    encode_tags = [
        (
            # Remove all tags.
            r'<.*?>', 0,
            r'',
        )
    ]

    @classmethod
    def post_encode(cls, text):
        """Convert tags."""

        return text

    @classmethod
    def italicize(cls, text):
        """Italicize text."""

        return text
