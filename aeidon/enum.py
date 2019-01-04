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

"""
Lists of named constants with integer values.

:class:`EnumerationItem`s are subclassed from :class:`int`, so they are actual
integers. The string value of an item will be the name that it was defined with
in its set. New items can always be added to an enumeration.
"""

__all__ = ("EnumerationItem", "Enumeration",)


class EnumerationItem(int):

    """
    Named constant with an integer value.

    :class:`EnumerationItem` can be instantiated without any specified values
    and users need not bother with them. Instantiation with correct values
    harmonous with the rest of the items should be left up to the parent list.
    """

    def __new__(cls, value=0, name="", parent=None):
        """Return integer instance with additional attributes."""
        instance = int.__new__(cls, value)
        instance.name = name
        instance.parent = parent
        return instance

    def __bool__(self):
        """For consistency, always return ``True``."""
        return True

    def __str__(self):
        """Return name as the string representation."""
        return self.name


class Enumeration(list):

    """
    List of named constants with integer values.

    :class:`Enumeration` is an actual :class:`list` where enumeration items are
    stored as both list items and instance attributes. New items should be
    added by setting an instance attribute.

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
        """Return ``True`` if enumeration contains `item`."""
        return list.__contains__(self, item)

    def __delattr__(self, name):
        """Delete enumeration item and attribute."""
        list.remove(self, getattr(self, name))
        return object.__delattr__(self, name)

    def find_item(self, name, value):
        """Return the first found item with the given attribute `value`."""
        for item in self:
            if getattr(item, name) == value:
                return item
        raise ValueError("Name {!r} not found".format(name))

    def __setattr__(self, name, value):
        """Set value of enumeration item with correct attributes."""
        if isinstance(value, EnumerationItem):
            value = value.__class__(len(self), name, self)
            list.append(self, value)
        return object.__setattr__(self, name, value)
