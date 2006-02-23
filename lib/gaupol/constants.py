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


from gettext import gettext as _


class Action(object):

    DO            = 0
    UNDO          = 1
    REDO          = 2
    UNDO_MULTIPLE = 3
    REDO_MULTIPLE = 4


class Document(object):

    MAIN = 0
    TRAN = 1


class Format(object):

    ASS        = 0
    MICRODVD   = 1
    MPL2       = 2
    SUBRIP     = 3
    SSA        = 4
    SUBVIEWER2 = 5

    class_names = [
        'AdvancedSubStationAlpha',
        'MicroDVD',
        'MPL2',
        'SubRip',
        'SubStationAlpha',
        'SubViewer2',
    ]

    display_names = [
        _('Advanced Sub Station Alpha'),
        _('MicroDVD'),
        _('MPL2'),
        _('SubRip'),
        _('Sub Station Alpha'),
        _('SubViewer 2.0'),
    ]

    extensions = [
        '.ass',
        '.sub',
        '.txt',
        '.srt',
        '.ssa',
        '.sub',
    ]

    id_names = [
        'ass',
        'microdvd',
        'mpl2',
        'subrip',
        'ssa',
        'subviewer2',
    ]


class Framerate(object):

    FR_23_976 = 0
    FR_25     = 1
    FR_29_97  = 2

    display_names = [
        _('23.976 fps'),
        _('25 fps'),
        _('29.97 fps'),
    ]

    id_names = [
        '23_976',
        '25',
        '29_97',
    ]

    values = [
        23.976,
        25.0,
        29.97,
    ]


class Mode(object):

    TIME  = 0
    FRAME = 1

    id_names = [
        'time',
        'frame',
    ]


class Newlines(object):

    MAC     = 0
    UNIX    = 1
    WINDOWS = 2

    display_names = [
        _('Mac'),
        _('Unix'),
        _('Windows'),
    ]

    id_names = [
        'mac',
        'unix',
        'windows',
    ]

    values = [
        '\r',
        '\n',
        '\r\n',
    ]


class Position(object):

    ABOVE = 0
    BELOW = 1

    id_names = [
        'above',
        'below',
    ]


class VideoPlayer(object):

    MPLAYER = 0
    VLC     = 1

    display_names = [
        _('MPlayer'),
        _('VLC'),
    ]

    id_names = [
        'mplayer',
        'vlc',
    ]

    # %v = video filename
    # %s = subtitle filename
    # %t = time
    # %c = seconds
    # %f = frame

    commands    = [
        'mplayer -identify -osdlevel 2 -ss %c -sub "%s" "%v"',
        'vlc --start-time=%c --sub-file="%s" "%v"',
    ]
