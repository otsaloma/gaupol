# -*- coding: utf-8-unix -*-

# Copyright (C) 2007-2009 Osmo Salomaa
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

"""Regular expression substitution for subtitle text."""

import aeidon
import re

__all__ = ("Pattern",)


class Pattern(aeidon.MetadataItem):

    """
    Regular expression substitution for subtitle text.

    :ivar enabled: ``True`` if pattern should be used, ``False`` if not
    :ivar fields: Dictionary of all data field names and values
    :ivar local: ``True`` if pattern is defined by user, ``False`` if system
    """

    def __init__(self, fields=None):
        """Initialize a :class:`Pattern` object."""
        aeidon.MetadataItem.__init__(self, fields)
        self.enabled = True
        self.local = False

    def get_flags(self):
        """Return the evaluated value of the ``Flags`` field."""
        flags = 0
        for name in self.get_field_list("Flags"):
            flags = flags | getattr(re, name)
        return flags
