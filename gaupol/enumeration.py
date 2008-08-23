# Copyright (C) 2005-2008 Osmo Salomaa
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

"""Lists of named constants with integer values.

EnumerationItems are subclassed from 'int', so they are actual integers. The
string value of an item will be the name that it was defined with in its set.
New items can always be added to a list.
"""

import gaupol

__all__ = ("EnumerationItem", "Enumeration",)


class EnumerationItem(int):

    """Named constant with an integer value.

    This class can be instantiated without any specified values and users need
    not bother with them. Instantiation with correct values harmonous with the
    rest of the items should be left up to the parent list.
    """

    # pylint: disable-msg=E1101

    def __cmp__(self, other):

        if isinstance(other, int):
            if isinstance(other, EnumerationItem):
                if self.parent is not other.parent:
                    raise ValueError
            return int.__cmp__(int(self), int(other))
        return 1

    if not gaupol.debug: del __cmp__

    def __new__(cls, value=0, name="", parent=None):

        instance = int.__new__(cls, value)
        instance.name = name
        instance.parent = parent
        return instance

    def __str__(self):

        return self.name


class Enumeration(list):

    """List of named constants with integer values.

    This class is an actual list where enumeration items are stored as both
    list items and instance attributes. New items should be added by setting an
    instance attribute. Data-changing list methods raise NotImplementedError.
    """

    NONE = None

    def __contains__(self, item):

        if isinstance(item, EnumerationItem):
            if item.parent is not self:
                return False
        return list.__contains__(self, item)

    if not gaupol.debug: del __contains__

    def __delitem__(self, *args, **kwargs):
        raise NotImplementedError

    def __delslice__(self, *args, **kwargs):
        raise NotImplementedError

    def __iadd__(self, *args, **kwargs):
        raise NotImplementedError

    def __imul__(self, *args, **kwargs):
        raise NotImplementedError

    def __setattr__(self, name, value):

        if isinstance(value, EnumerationItem):
            value = value.__class__(len(self), name, self)
            list.append(self, value)
        return object.__setattr__(self, name, value)

    def __setitem__(self, *args, **kwargs):
        raise NotImplementedError

    def __setslice__(self, *args, **kwargs):
        raise NotImplementedError

    def append(self, *args, **kwargs):
        raise NotImplementedError

    def extend(self, *args, **kwargs):
        raise NotImplementedError

    def find_item(self, name, value):
        """Return the first found item with the given attribute value."""

        for item in self:
            if getattr(item, name) == value:
                return item
        raise ValueError

    def insert(self, *args, **kwargs):
        raise NotImplementedError

    def pop(self, *args, **kwargs):
        raise NotImplementedError

    def remove(self, *args, **kwargs):
        raise NotImplementedError

    def reverse(self, *args, **kwargs):
        raise NotImplementedError

    def sort(self, *args, **kwargs):
        raise NotImplementedError
