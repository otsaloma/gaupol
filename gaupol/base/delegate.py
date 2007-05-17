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


"""Base class for delegates."""


class Delegate(object):

    """Base class for delegates.

    Instance variables:

        master: The master instance to where attribute calls are redirected
    """

    def __getattr__(self, name):

        return getattr(self.master, name)

    def __init__(self, master):

        object.__setattr__(self, "master", master)

    def __setattr__(self, name, value):

        if hasattr(self.master, name):
            return setattr(self.master, name, value)
        return object.__setattr__(self, name, value)

    def _invariant(self):
        if hasattr(self.master, "_invariant"):
            return self.master._invariant()
