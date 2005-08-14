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
# along with Gaupol; if falset, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA


"""gaupol-wide constants."""


VERSION = '0.0+svn'


# Extension and Format class constants must have the same order.

class Extension(object):

    EXTENSION_VALUES   = ['.sub', '.srt']
    EXTENSION_MICRODVD = 0
    EXTENSION_SUBRIP   = 1

class Format(object):

    FORMAT_NAMES    = ['MicroDVD', 'SubRip']
    FORMAT_MICRODVD = 0
    FORMAT_SUBRIP   = 1

class Framerate(object):

    FRAMERATE_NAMES  = ['23.976', '25'  , '29.97']
    FRAMERATE_VALUES = [ 23.976 ,  25.0 ,  29.97 ]
    FRAMERATE_23_976 = 0
    FRAMERATE_25     = 1
    FRAMERATE_29_97  = 2

class Mode(object):

    MODE_NAMES = ['frame', 'time']
    MODE_FRAME = 0
    MODE_TIME  = 1

class Newline(object):

    NEWLINE_NAMES   = ['Mac', 'Unix', 'Windows']
    NEWLINE_VALUES  = ['\r' , '\n'  , '\r\n'   ]
    NEWLINE_UNIX    = 'Unix'
    NEWLINE_MAC     = 'Mac'
    NEWLINE_WINDOWS = 'Windows'

class Position(object):

    POSITION_NAMES = ['above', 'below']
    POSITION_ABOVE = 0
    POSITION_BELOW = 1

class Type(object):

    TYPE_NAMES       = ['main', 'translation']
    TYPE_MAIN        = 0
    TYPE_TRANSLATION = 1
