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

class EXTENSION(object):

    VALUES   = ['.sub', '.txt', '.srt']
    MICRODVD = 0
    MPL2     = 1
    SUBRIP   = 2

class FORMAT(object):

    NAMES    = ['MicroDVD', 'MPL2', 'SubRip']
    MICRODVD = 0
    MPL2     = 1
    SUBRIP   = 2

class FRAMERATE(object):

    NAMES   = ['23.976', '25'  , '29.97']
    VALUES  = [ 23.976 ,  25.0 ,  29.97 ]
    _23_976 = 0
    _25     = 1
    _29_97  = 2

class MODE(object):

    NAMES = ['time', 'frame']
    TIME  = 0
    FRAME = 1

class NEWLINE(object):

    NAMES   = ['Mac', 'Unix', 'Windows']
    VALUES  = ['\r' , '\n'  , '\r\n'   ]
    UNIX    = 'Unix'
    MAC     = 'Mac'
    WINDOWS = 'Windows'

class POSITION(object):

    NAMES = ['above', 'below']
    ABOVE = 0
    BELOW = 1

class TYPE(object):

    NAMES = ['main', 'translation']
    MAIN  = 0
    TRAN  = 1
