# Copyright (C) 2005-2009 Osmo Salomaa
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
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# Gaupol. If not, see <http://www.gnu.org/licenses/>.

"""Subtitle text markup converter."""

import aeidon

__all__ = ("MarkupConverter",)


class MarkupConverter(object):

    """Subtitle text markup converter."""

    def __init__(self, from_format, to_format):
        """
        Initialize a :class:`MarkupConverter` instance.

        `from_format` and `to_format` should be :attr:`aeidon.formats`
        enumeration items.
        """
        self._from = aeidon.tags.new(from_format)
        self._to = aeidon.tags.new(to_format)

    def convert(self, text):
        """Return `text` with markup converted."""
        return self._to.encode(self._from.decode(text))
