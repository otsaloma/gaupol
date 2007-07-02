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


"""Internal text clipboard."""


__all__ = ["Clipboard"]


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
        """Get the texts as a list."""

        return self._texts[:]

    def set_texts(self, texts):
        """Set the list of texts."""

        self._texts = list(texts)

    def is_empty(self):
        """Return True is the clipboard is empty."""

        return not bool(self._texts)
