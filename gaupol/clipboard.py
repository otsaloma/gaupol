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


"""Internal clipboard."""


class Clipboard(object):

    """Internal clipboard.

    Instance variables:

        data: List of strings or Nones

    Nones in data express that those items are to be skipped.
    """

    def __init__(self):

        self.data = []

    def get_data_as_string(self):
        """Get the data as a string."""

        return "\n\n".join([x or "" for x in self.data])
