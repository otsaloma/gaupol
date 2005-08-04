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


"""Base class for subtitle tags."""


try:
    from psyco.classes import *
except ImportError:
    pass

    
class TagLibrary(object):

    """
    Base class for subtitle tags.
    
    This class cannot be instantiated. This is a grouping-class that holds
    constants and classmethods.

    DECODE_TAGS is a list of regular expressions that convert tags to the
    Gaupol internal format. ENCODE_TAGS convert from Gaupol internal format
    to the class's format.

    Internal tags:
    <b></b>
    <i></i>
    <u></u>
    <color="#rrggbb"></color>
    <font="name"></font>
    <size="int"></size>
    """

    TAG         = None
    ITALIC      = None
    DECODE_TAGS = None
    ENCODE_TAGS = None

    def italicize(cls, text):
        """Italicize text."""
        
        return text

    italicize = classmethod(italicize)
