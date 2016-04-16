# -*- coding: utf-8 -*-

# Copyright (C) 2005 Osmo Salomaa
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""Subtitle text markup converter."""

import aeidon

__all__ = ("MarkupConverter",)


class MarkupConverter:

    """Subtitle text markup converter."""

    def __init__(self, from_format, to_format):
        """
        Initialize a :class:`MarkupConverter` instance.

        `from_format` and `to_format` should be :attr:`aeidon.formats`
        enumeration items.
        """
        self._from = aeidon.markups.new(from_format)
        self._to = aeidon.markups.new(to_format)

    def convert(self, text):
        """Return `text` with markup converted."""
        return self._to.encode(self._from.decode(text))
