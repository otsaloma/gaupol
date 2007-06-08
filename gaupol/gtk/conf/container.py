# Copyright (C) 2006-2007 Osmo Salomaa
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


"""Configuration data container."""


import gaupol


class Container(gaupol.Observable):

    """Configuration data container.

    This class can be a configuration section or a container for the entire
    configuration data if there are no sections. This class is instantiated
    with a 'root', which is a lowest (sub)dictionary of a ConfigObj instance.
    This class provides convenient attribute access and notifications for
    configuration variables as per the Observable API.
    """

    def __init__(self, root):

        gaupol.Observable.__init__(self)
        self.__root = root
        self._init_signal_handlers()

    def _init_signal_handlers(self):
        """Initialize signal handlers."""

        for name, value in self.__root.items():
            setattr(self, name, value)
            signal = "notify::%s" % name
            self.connect(signal, self._on_notify, name)

    def _on_notify(self, obj, value, name):
        """Synchronize attribute value with root dictionary."""

        if value != self.__root[name]:
            self.__root[name] = value
