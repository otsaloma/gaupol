# -*- coding: utf-8 -*-

# Copyright (C) 2005-2009,2011 Osmo Salomaa
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

"""
Lists of named constants with integer values.

:class:`EnumerationItem`s are subclassed from :class:`int`, so they are actual
integers. The string value of an item will be the name that it was defined with
in its set. New items can always be added to an enumeration.
"""

import aeidon

__all__ = ("EnumerationItem", "Enumeration",)


class EnumerationItem(int):

    """
    Named constant with an integer value.

    :class:`EnumerationItem` can be instantiated without any specified values
    and users need not bother with them. Instantiation with correct values
    harmonous with the rest of the items should be left up to the parent list.
    """

    def __bool__(self):
        """For consistency, always return ``True``."""
        return True

    def __eq__(self, other):
        """Compare enumeration item equality by value."""
        if isinstance(other, int):
            if isinstance(other, EnumerationItem):
                if self.parent is not other.parent:
                    raise NotImplementedError
            return int.__eq__(int(self), int(other))
        if other is None:
            return False
        raise NotImplementedError

    def __ge__(self, other):
        """Compare enumeration item equality by value."""
        if isinstance(other, int):
            if isinstance(other, EnumerationItem):
                if self.parent is not other.parent:
                    raise NotImplementedError
            return int.__ge__(int(self), int(other))
        raise NotImplementedError

    def __gt__(self, other):
        """Compare enumeration item equality by value."""
        if isinstance(other, int):
            if isinstance(other, EnumerationItem):
                if self.parent is not other.parent:
                    raise NotImplementedError
            return int.__gt__(int(self), int(other))
        raise NotImplementedError

    def __hash__(self):
        """Return a hashable value."""
        return int.__hash__(self)

    def __le__(self, other):
        """Compare enumeration item equality by value."""
        if isinstance(other, int):
            if isinstance(other, EnumerationItem):
                if self.parent is not other.parent:
                    raise NotImplementedError
            return int.__le__(int(self), int(other))
        raise NotImplementedError

    def __lt__(self, other):
        """Compare enumeration item equality by value."""
        if isinstance(other, int):
            if isinstance(other, EnumerationItem):
                if self.parent is not other.parent:
                    raise NotImplementedError
            return int.__lt__(int(self), int(other))
        raise NotImplementedError

    def __ne__(self, other):
        """Compare enumeration item equality by value."""
        if isinstance(other, int):
            if isinstance(other, EnumerationItem):
                if self.parent is not other.parent:
                    raise NotImplementedError
            return int.__ne__(int(self), int(other))
        if other is None:
            return True
        raise NotImplementedError

    def __new__(cls, value=0, name="", parent=None):
        """Return integer instance with additional attributes."""
        instance = int.__new__(cls, value)
        instance.name = name
        instance.parent = parent
        return instance

    def __str__(self):
        """Return name as the string representation."""
        return self.name

    if not aeidon.DEBUG:
        del __eq__
        del __ge__
        del __gt__
        del __le__
        del __lt__
        del __ne__


class Enumeration(list):

    """
    List of named constants with integer values.

    :class:`Enumeration` is an actual :class:`list` where enumeration items are
    stored as both list items and instance attributes. New items should be
    added by setting an instance attribute. Data-changing list methods raise
    :exc:`NotImplementedError`.

    Typical use to create a new enumeration would be something like::

        fruits = aeidon.Enumeration()
        fruits.APPLE = aeidon.EnumerationItem()
        fruits.MANGO = aeidon.EnumerationItem()
        fruits.APPLE.size = 10
        fruits.MANGO.size = 20

    Note that there is no finalization of an enumeration. New items can always
    be added just by assigning a new attribute to the enumeration. Likewise,
    existing items can always be removed using :func:`delattr`.
    """

    NONE = None

    def __contains__(self, item):
        if isinstance(item, EnumerationItem):
            if item.parent is not self:
                return False
        return list.__contains__(self, item)

    def __delattr__(self, name):
        """Delete enumeration item and attribute."""
        list.remove(self, getattr(self, name))
        return object.__delattr__(self, name)

    def __delitem__(self, *args, **kwargs):
        raise NotImplementedError

    def __iadd__(self, *args, **kwargs):
        raise NotImplementedError

    def __imul__(self, *args, **kwargs):
        raise NotImplementedError

    def __setattr__(self, name, value):
        """Set value of enumeration item with correct attributes."""
        if isinstance(value, EnumerationItem):
            value = value.__class__(len(self), name, self)
            list.append(self, value)
        return object.__setattr__(self, name, value)

    def __setitem__(self, *args, **kwargs):
        raise NotImplementedError

    def append(self, *args, **kwargs):
        raise NotImplementedError

    def extend(self, *args, **kwargs):
        raise NotImplementedError

    def find_item(self, name, value):
        """Return the first found item with the given attribute `value`."""
        for item in self:
            if getattr(item, name) == value:
                return item
        raise ValueError("Name {} not found"
                         .format(repr(name)))

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

    if not aeidon.DEBUG:
        del __contains__
