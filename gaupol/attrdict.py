# -*- coding: utf-8 -*-

# Copyright (C) 2006 Osmo Salomaa
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

"""Observable dictionary with attribute access to keys."""

import aeidon

__all__ = ("AttributeDictionary",)


class AttributeDictionary(aeidon.Observable):

    """
    Observable dictionary with attribute access to keys.

    :class:`AttributeDictionary` is initialized from a root dictionary,
    which is kept in sync with attribute values. This allows convenient
    attribute access to dictionary keys and notifications of changes
    via the :class:`aeidon.Observable` interface.
    """

    def __init__(self, root):
        """
        Initialize an :class:`AttributeDictionary` instance.

        All subdictionaries of `root` are initialized as instances of
        :class:`AttributeDictionary` as well.
        """
        aeidon.Observable.__init__(self)
        self._root = root
        self.update(root)

    def add_attribute(self, name, value):
        """Add instance attribute and corresponding root dictionary key."""
        self._root[name] = value
        # In the case of dictionaries, set the original dictionary
        # to the root dictionary, but instantiate an AttributeDictionary
        # for use as the corresponding attribute.
        if isinstance(value, dict):
            value = AttributeDictionary(value)
        setattr(self, name, value)
        self.connect("notify::{}".format(name), self._on_notify, name)

    def extend(self, root):
        """Add new values from another root dictionary."""
        for name, value in root.items():
            if hasattr(self, name):
                if isinstance(value, dict):
                    getattr(self, name).extend(value)
            else:
                self.add_attribute(name, value)


    def _on_notify(self, obj, value, name):
        """Synchronize changed attribute value with root dictionary."""
        self._root[name] = value

    def remove_attribute(self, name):
        """Remove instance attribute and corresponding root dictionary key."""
        self.disconnect("notify::{}".format(name), self._on_notify)
        delattr(self, name)
        if name in self._root:
            del self._root[name]

    def update(self, root):
        """Update values from another root dictionary."""
        for name, value in root.items():
            if hasattr(self, name):
                if isinstance(value, dict):
                    getattr(self, name).update(value)
                else:
                    setattr(self, name, value)
            else:
                self.add_attribute(name, value)
