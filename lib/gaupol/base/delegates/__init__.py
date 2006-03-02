# Copyright (C) 2005 Osmo Salomaa
#
# This file is part of Gaupol.
#
# Gaupol is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Gaupol is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Gaupol; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA


"""Common delegate affairs."""


try:
    from psyco.classes import *
except ImportError:
    pass

import inspect


# List of all delegate module names. Methods of listed modules will be imported
# into the delegation system.
module_names = (
    'action',
    'edit',
    'fileopen',
    'filesave',
    'format',
    'preview',
    'stat',
    'timing',
)


class Delegate(object):

    """
    Base class for delegates.

    The purpose of the methods in this class is to provide direct access to
    the master class's attributes by redirecting all self.attribute calls not
    found in the delegate class.
    """

    # Code borrowed from
    # "Automatic delegation as an alternative to inheritance" by Alex Martelli
    # http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/52295

    def __init__(self, master):

        self.__dict__['master'] = master

    def __getattr__(self, name):
        """Get value of master object's attribute."""

        return getattr(self.master, name)

    def __setattr__(self, name, value):
        """Set value of master object's attribute."""

        return setattr(self.master, name, value)


class Delegates(object):

    """All delegates."""

    module_names = module_names
    classes = []


def list_delegate_classes():
    """List all delegate classes."""

    for module_name in Delegates.module_names:
        path = 'gaupol.base.delegates.' + module_name
        module = __import__(path, None, None, [''])
        for name in dir(module):
            if name.startswith('_'):
                continue
            value = getattr(module, name)
            if inspect.getmodule(value) != module:
                continue
            try:
                if issubclass(value, Delegate):
                    Delegates.classes.append(value)
            except TypeError:
                continue


# List delegates if they have not yet been listed.
if not Delegates.classes:
    list_delegate_classes()
