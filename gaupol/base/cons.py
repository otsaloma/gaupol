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


"""Constant members and sections."""


class Member(int):

    """Constant member."""

    def __new__(cls, value=0, name=""):

        obj = int.__new__(cls, value)
        obj.name = name
        return obj

    def __str__(self):

        return self.name


class Section(object):

    """Constant section.

    Instance variables:

        members: List of all constant members
        names:   List of the names of members
    """

    def __init__(self):

        self.members = []
        self.names   = []

    def __setattr__(self, name, value):

        if isinstance(value, Member):
            value = Member(len(self.members), name)
            self.members.append(value)
        return object.__setattr__(self, name, value)

    def finalize(self):
        """Populate attribute lists based on members."""

        names = dir(self.members[0])
        for name in (x for x in names if not x.startswith("_")):
            values = list(getattr(x, name) for x in self.members)
            setattr(self, name + "s", values)
