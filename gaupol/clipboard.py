# Copyright (C) 2005-2007 Osmo Salomaa
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


"""Internal text clipboard."""


class Clipboard(object):

    """Internal text clipboard.

    Instance variables:
     * _texts: List of strings or Nones

    Nones in _texts express that those items are to be skipped.
    """

    def __init__(self):

        self._texts = []

    def append(self, item):
        """Append item to texts."""

        self._texts.append(item)

    def clear(self):
        """Clear the texts."""

        self._texts = []

    def get_string(self):
        """Get the texts as one string."""

        strings = [x or "" for x in self._texts]
        return "\n\n".join(strings)

    def get_texts(self):
        """Get the texts."""

        return self._texts[:]
