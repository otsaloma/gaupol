# -*- coding: utf-8 -*-

# Copyright (C) 2006-2010 Osmo Salomaa
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

"""Observable dictionary with attribute access to keys."""

import aeidon

__all__ = ("AttributeDictionary",)


class AttributeDictionary(aeidon.Observable):

    """
    Observable dictionary with attribute access to keys.

    :class:`AttributeDictionary` is initialized from a root dictionary, which
    is kept in sync with attribute values. This allows convenient attribute
    access to dictionary keys and notifications of changes via the
    :class:`aeidon.Observable` interface.
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

    def _on_notify(self, obj, value, name):
        """Synchronize changed attribute value with root dictionary."""
        self._root[name] = value

    def add_attribute(self, name, value):
        """Add instance attribute and corresponding root dictionary key."""
        self._root[name] = value
        # In the case of dictionaries, set the original dictionary to the root
        # dictionary, but instantiate an AttributeDictionary for use as the
        # corresponding attribute.
        if isinstance(value, dict):
            value = AttributeDictionary(value)
        setattr(self, name, value)
        self.connect("notify::{}".format(name), self._on_notify, name)

    def extend(self, root):
        """Add new values from another root dictionary."""
        for name, value in root.items():
            if not hasattr(self, name):
                self.add_attribute(name, value)
            else: # Extend current value.
                if isinstance(value, dict):
                    getattr(self, name).extend(value)

    def remove_attribute(self, name):
        """Remove instance attribute and corresponding root dictionary key."""
        self.disconnect("notify::{}".format(name), self._on_notify)
        delattr(self, name)
        if name in self._root:
            del self._root[name]

    def update(self, root):
        """Update values from another root dictionary."""
        for name, value in root.items():
            if not hasattr(self, name):
                self.add_attribute(name, value)
            else: # Update current value.
                if isinstance(value, dict):
                    getattr(self, name).update(value)
                else: # Set non-dictionary value.
                    setattr(self, name, value)
