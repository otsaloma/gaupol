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

"""Base class for objects that dispatch ``self``-lookups."""

__all__ = ("Delegate",)


class Delegate:

    """
    Base class for objects that dispatch ``self``-lookups.

    :ivar master: Object to where attribute calls are dispatched
    """

    def __init__(self, master):
        """Initialize a :class:`Delegate` instance."""
        object.__setattr__(self, "master", master)

    def __getattr__(self, name):
        """Return value of master attribute."""
        return getattr(self.master, name)

    def __setattr__(self, name, value):
        """Set value of master attribute."""
        # Do not create new attributes for master.
        if hasattr(self.master, name):
            return setattr(self.master, name, value)
        return object.__setattr__(self, name, value)
