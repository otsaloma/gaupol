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

"""SubRip tag library."""

import gaupol
import re

from .taglib import TagLibrary


class SubRip(TagLibrary):

    """SubRip tag library."""

    format = gaupol.FORMAT.SUBRIP

    @property
    @gaupol.util.once
    def italic_tag(self):
        """Regular expression for an italic tag."""

        return re.compile(r"</?i>", re.IGNORECASE)

    @property
    @gaupol.util.once
    def tag(self):
        """Regular expression for any tag."""

        return re.compile(r"</?(b|i|u)>", re.IGNORECASE)

    @gaupol.util.once
    def _get_decode_tags(self):
        """Get list of tuples of regular expression, replacement."""

        tags = [
            # Uppercase style tags
            (re.compile(r"(</?)B>"), r"\1b>"),
            (re.compile(r"(</?)I>"), r"\1i>"),
            (re.compile(r"(</?)U>"), r"\1u>"),]
        return tags

    @gaupol.util.once
    def _get_encode_tags(self):
        """Get list of tuples of regular expression, replacement."""

        # Remove all non-style tags.
        return [(re.compile(r"</?[^>]{3,}>"), "")]

    @gaupol.util.once
    def _get_redundant_tags(self):
        """Get list of tuples of regular expression, replacement."""

        tags = [
            (re.compile(r"<(.*?)(=.*?)?>( *)</\1>"), r"\3"),
            (re.compile(r"</(.*?)>( *)<\1(=.*?)?>"), r"\2"),]
        return tags

    def decode(self, text):
        """Return text with tags converted from this to internal format."""

        for regex, replacement in self._get_decode_tags():
            text = regex.sub(replacement, text)
        return text

    def encode(self, text):
        """Return text with tags converted from internal to this format."""

        for regex, replacement in self._get_encode_tags():
            text = regex.sub(replacement, text)
        return text

    def italicize(self, text):
        """Return italicized text."""

        return u"<i>%s</i>" % text

    def remove_redundant(self, text):
        """Return text with redundant tags removed."""

        for regex, replacement in self._get_redundant_tags():
            text = regex.sub(replacement, text)
        return text
