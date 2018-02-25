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

"""Internal text clipboard."""

__all__ = ("Clipboard",)


class Clipboard:

    """Internal text clipboard."""

    def __init__(self):
        """Initialize a :class:`Clipboard` instance."""
        # List of strings, each being the text of one subtitle. Nones in the
        # list express that those subtitles are skipped, i.e. the range of
        # subtitles is not unified, but contains gaps.
        self._texts = []

    def append(self, item):
        """Append `item` to texts."""
        self._texts.append(item)

    def clear(self):
        """Clear texts."""
        self._texts = []

    def get_string(self):
        """Return texts as one string."""
        strings = [x or "" for x in self._texts]
        return "\n\n".join(strings)

    def get_texts(self):
        """Return texts as a list of strings."""
        return self._texts[:]

    def is_empty(self):
        """Return ``True`` if empty."""
        return not bool(self._texts)

    def set_string(self, string):
        """Set the list of texts from a single string."""
        strings = [x or None for x in string.split("\n\n")]
        self.set_texts(strings)

    def set_texts(self, texts):
        """Set the list of texts."""
        self._texts = list(texts)
