# Copyright (C) 2007-2008 Osmo Salomaa
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

"""Regular expression substitutions for subtitle text."""

import gaupol
import re

__all__ = ("Pattern",)


class Pattern(gaupol.MetadataItem):

    """Regular expression substitutions for subtitle text.

    Instance variables:
     * enabled: True if pattern should be used, False if not
     * fields: Dictionary of all data field names and values
     * local: True if pattern is defined by user, False if system
    """

    def __init__(self, fields=None):
        """Initialize a Pattern object."""

        gaupol.MetadataItem.__init__(self, fields)
        self.enabled = True
        self.local = False

    def get_flags(self):
        """Return the evaluated value of the 'Flags' field."""

        flags = 0
        for name in self.get_field_list("Flags"):
            flags = flags | getattr(re, name)
        return flags
