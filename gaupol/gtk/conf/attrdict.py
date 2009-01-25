# Copyright (C) 2006-2008 Osmo Salomaa
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

"""Observable configuration dictionary with attribute access to keys."""

import gaupol


class ConfigAttrDict(gaupol.Observable):

    """Observable configuration dictionary with attribute access to keys.

    Attribute dictionary is initialized from a root dictionary, which is kept
    in sync with attribute values. This allows convenient attribute access to
    dictionary keys and notifications via the Observable interface, The root
    dictionary is expected to be a ConfigObj dictionary, i.e. a ConfigObj
    instance or any child dictionary of that instance.
    """

    def __init__(self, root):
        """Initialize a ConfigAttrDict object.

        All attributes of corresponding child dictionaries of root are
        initialized as ConfigAttrDicts as well.
        """
        gaupol.Observable.__init__(self)
        self.__keys = set(())
        self.__root = root
        self.update(root)

    def _on_notify(self, obj, value, name):
        """Synchronize changed attribute value with root dictionary."""

        if value != self.__root[name]:
            # Only set root dictionary key value if diffent than currently to
            # avoid ConfigObj registering it as set, i.e. non-default.
            self.__root[name] = value

    def add_attribute(self, name, value):
        """Add instance attribute and corresponding root dictionary key."""

        self.__root[name] = value
        # In the case of dictionaries, i.e. subsections of the current section,
        # set the original dictionary to the root dictionary, but instanctiate
        # an ConfigAttrDict instance for use as the corresponding attribute.
        if isinstance(value, dict):
            value = ConfigAttrDict(value)
        setattr(self, name, value)
        signal = "notify::%s" % name
        self.connect(signal, self._on_notify, name)
        self.__keys.add(name)

    def remove_attribute(self, name):
        """Remove instance attribute and corresponding root dictionary key."""

        self.__keys.remove(name)
        signal = "notify::%s" % name
        self.disconnect(signal, self._on_notify)
        delattr(self, name)
        if name in self.__root:
            del self.__root[name]

    def replace(self, root):
        """Replace root dictionary and update attribute values.

        Attribute values are updated to match values of corresponding keys in
        the new root dictionary and attributes that do not exist in the new
        root dictionary are removed (Use with care!). Using this method is
        usually a better idea than instantiating a new ConfigAttrDict, because
        there may already be attribute notification signal connections with the
        existing instance of ConfigAttrDict, which may not want to be lost.
        """
        self.__root = root
        self.update(root)
        for name in (self.__keys - set(root.keys())):
            self.remove_attribute(name)

    def update(self, root):
        """Update values from another root dictionary.

        The root dictionary given as argument is not deep-copied. If it
        contains any subdictionaries, those will be used as is.
        """
        new_defaults = set(root.defaults)
        for name, value in root.iteritems():
            if not hasattr(self, name):
                self.add_attribute(name, value)
            else: # Update current value.
                if isinstance(value, dict):
                    getattr(self, name).update(value)
                else: setattr(self, name, value)
        # Update ConfigObj default value tracking list.
        old_defaults = set(self.__root.defaults)
        for name in (new_defaults - old_defaults):
            self.__root.defaults.append(name)
