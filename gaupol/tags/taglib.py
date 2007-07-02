# Copyright (C) 2005-2007 Osmo Salomaa
#
# This file is part of Gaupol.
#
# Gaupol is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# Gaupol is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# Gaupol.  If not, see <http://www.gnu.org/licenses/>.


"""Base class for subtitle tag libraries.

Tag conversions are done via an internal format, which has the following tags:
 * <b>BOLD</b>
 * <i>ITALIC</i>
 * <u>UNDERLINE</u>
 * <color="#RRGGBB">COLOR</color>
 * <font="NAME">FONT FAMILY</font>
 * <size="INTEGER">FONT SIZE</size>
"""


import gaupol
import re


class TagLibrary(gaupol.Singleton):

    """Base class for subtitle tag libraries."""

    format = None

    @property
    @gaupol.util.once
    def italic_tag(self):
        """Regular expression for an italic tag or None."""

        return None

    @property
    @gaupol.util.once
    def tag(self):
        """Regular expression for any tag or None."""

        return None

    @gaupol.util.once
    def __get_encode_tags(self):
        """Get list of tuples of regular expression, replacement."""

        # Remove all tags.
        return [(re.compile(r"<.*?>"), "")]

    def decode(self, text):
        """Return text with tags converted from this to internal format."""

        return text

    def encode(self, text):
        """Return text with tags converted from internal to this format."""

        for regex, replacement in self.__get_encode_tags():
            text = regex.sub(replacement, text)
        return text

    def italicize(self, text):
        """Return italicized text."""

        raise NotImplementedError
