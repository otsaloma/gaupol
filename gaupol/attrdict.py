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

"""Observable dictionary with attribute access to keys."""

import gaupol

__all__ = ("AttrDict",)


class AttrDict(gaupol.Observable):

    """Observable dictionary with attribute access to keys."""

    def __init__(self, root):
        """Initialize an AttrDict object.

        All child dictionaries of root are initialized as AttrDicts as well.
        """
        gaupol.Observable.__init__(self)
        self.__root = root
        self._init_attributes()

    def _init_attributes(self):
        """Initialize attributes and signal handlers."""

        for name, value in self.__root.iteritems():
            if isinstance(value, dict):
                value = AttrDict(value)
            setattr(self, name, value)
            signal = "notify::%s" % name
            self.connect(signal, self._on_notify, name)

    def _on_notify(self, obj, value, name):
        """Synchronize attribute value with root dictionary."""

        if value != self.__root[name]:
            if isinstance(value, dict):
                value = AttrDict(value)
            self.__root[name] = value

    def update(self, root):
        """Update values from a new root dictionary."""

        self.__root = root
        for name, value in self.__root.iteritems():
            if isinstance(value, dict):
                value = AttrDict(value)
            setattr(self, name, value)
