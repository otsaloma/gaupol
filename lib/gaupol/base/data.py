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


"""Subtitle project data."""


import types

try:
    from psyco.classes import *
except ImportError:
    pass

from gaupol.base.delegates.classes import *
from gaupol.base.timing.calc import TimeFrameCalculator


class Data(object):
    
    """
    Subtitle project data.

    This is the main class for gaupol.base. This class holds the all the
    subtitle data of one project. All methods are outsourced to delegates.
    
    times    : list of lists of strings,  [[show, hide, duration], ...]
    frames   : list of lists of integers, [[show, hide, duration], ...]
    texts    : list of lists of strings,  [[text, translation], ...]
    """
    
    def __init__(self, framerate):

        self.times  = []
        self.frames = []
        self.texts  = []

        self.framerate = framerate
        self.main_file = None
        self.tran_file = None

        self.calc = TimeFrameCalculator(framerate)

        self._delegations = {}
        self._assign_delegations()

    def _assign_delegations(self):
        """Map method names to Delegate objects."""

        # Loop through all delegates creating an instance of the delegate and
        # mapping all its methods that don't start with an underscore to that
        # instance.
        for delegate in get_delegates():

            for attr_name in dir(delegate):
            
                if attr_name.startswith('_'):
                    continue
                
                attr = eval('delegate.%s' % attr_name)
                if not isinstance(attr, types.MethodType):
                    continue
                
                self._delegations[attr_name] = delegate
        
    def __getattr__(self, name):
        """Delegate method calls to Delegate objects."""
        
        return self._delegations[name].__getattribute__(name)
