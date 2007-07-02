# Copyright (C) 2007 Osmo Salomaa
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


"""Base class for single-instance classes."""


class Singleton(object):

    """Base class for single-instance classes.

    Class variables:
     * _instance: The single instance returned by __new__
    """

    def __new__(cls, *args, **kwargs):

        if not '_instance' in cls.__dict__:
            cls._instance = object.__new__(cls, *args, **kwargs)
        return cls._instance
