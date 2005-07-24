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


"""Base class for delegate classes."""


# Code borrowed from:
# "Automatic delegation as an alternative to inheritance" by Alex Martelli
# http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/52295


try:
    from psyco.classes import *
except ImportError:
    pass


class Delegate(object):

    """
    Base class for delegate classes.
    
    This class is meant to be subclassed and extended by actual delegate
    classes.
    
    The purpose of the methods in this class is to provide direct access to the
    master class's attributes by redirecting all self.attribute calls not found
    in the delegate class.
    """

    def __init__(self, master):

        self.__dict__['master'] = master

    def __getattr__(self, name):
        """Get value of master object's attribute."""
        
        return getattr(self.master, name)
        
    def __setattr__(self, name, value):
        """Set value of master object's attribute."""
        
        return setattr(self.master, name, value)
