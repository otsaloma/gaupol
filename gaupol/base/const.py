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

"""Constant members and sections.

Members are subclassed from 'int', so they are directly usable as integers.
The string value of a member will be the name that it was defined with in its
section.

Example usage:

    FRUIT = ConstantSection()
    FRUIT.APPLE = ConstantMember()
    FRUIT.APPLE.color = "green"
    FRUIT.ORANGE = ConstantMember()
    FRUIT.ORANGE.color = "orange"
    FRUIT.finalize()

Section's 'finalize' method will make all members' attributes available as
lists in the section. In the above example, the following lists will exist:

    FRUIT.colors
    FRUIT.members
    FRUIT.names

New members and attributes can always be added to a section, as long as at the
end of all new additions, the 'finalize' method will be called.
"""


class ConstantMember(int):

    """Constant member.

    This class can be instantiated without any specified values and users need
    not bother with them. Instantiation with correct values harmonous with the
    rest of the members should be left up to the parent section.
    """

    def __new__(cls, value=0, name=""):

        instance = int.__new__(cls, value)
        instance.name = name
        return instance

    def __str__(self):

        # pylint: disable-msg=E1101
        return self.name


class ConstantSection(object):

    """Constant section.

    Instance variables 'members' and 'names' exist by default. The rest are
    created automatically based on the defined attributes of the members when
    the 'finalize' method is run.
    """

    def __init__(self):

        self.members = []
        self.names = []

    def __setattr__(self, name, value):

        if isinstance(value, ConstantMember):
            value = ConstantMember(len(self.members), name)
            self.members.append(value)
        return object.__setattr__(self, name, value)

    def finalize(self):
        """Populate attribute lists."""

        names = dir(self.members[0])
        for name in (x for x in names if not x.startswith("_")):
            values = [getattr(x, name) for x in self.members]
            setattr(self, name + "s", values)
