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
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# Gaupol. If not, see <http://www.gnu.org/licenses/>.

"""Base class for objects that dispatch self-lookups."""

__all__ = ("Delegate",)


class Delegate(object):

    """Base class for objects that dispatch self-lookups.

    Calls for all attributes not found in self are dispatched to the object
    defined as instance variable 'master'.
    """

    def __getattr__(self, name):

        return getattr(self.master, name)

    def __init__(self, master):

        object.__setattr__(self, "master", master)

    def __setattr__(self, name, value):

        # Do not create new attributes for master.
        if hasattr(self.master, name):
            return setattr(self.master, name, value)
        return object.__setattr__(self, name, value)

    def _invariant(self):

        # Default to checking master's class invariant.
        if hasattr(self.master, "_invariant"):
            return self.master._invariant()
