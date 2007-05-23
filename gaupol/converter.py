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


"""Subtitle text tag converter."""


from gaupol.tags import *


class TagConverter(object):

    """Subtitle text tag converter.

    Instance variables:
     * _from: TagLibrary instance for the 'from' format
     * _to: TagLibrary instance for the 'to' format
    """

    def __init__(self, from_format, to_format):
        """Initialize a TagConverter instance.

        from_format and to_format should be FORMAT constants.
        """
        self._from = eval(from_format.class_name)()
        self._to = eval(to_format.class_name)()

    def convert(self, text):
        """Return text with tags converted."""

        return self._to.encode(self._from.decode(text))
