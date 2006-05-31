# Copyright (C) 2005-2006 Osmo Salomaa
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


"""Constants."""


import sys

from gettext import gettext as _


SHOW = 0
HIDE = 1
DURN = 2


class Section(object):

    """Base class for constant classes."""

    @classmethod
    def get_names(cls):
        """Get names of attributes."""

        def sort(x, y):
            return cmp(getattr(cls, x), getattr(cls, y))

        names = []
        for name in dir(cls):
            if not name.startswith('_'):
                if name.isupper():
                    names.append(name)
        names.sort(sort)
        return names

    @classmethod
    def get_name(cls, value):
        """
        Get name of attribute with value.

        Raise ValueError if not found.
        """
        for name in cls.get_names():
            if getattr(cls, name) == value:
                return name
        raise ValueError


class Action(Section):

    """Revertable actions."""

    DO            = 0
    UNDO          = 1
    REDO          = 2
    DO_MULTIPLE   = 3
    UNDO_MULTIPLE = 4
    REDO_MULTIPLE = 5


class Column(Section):

    """Position data columns."""

    SHOW = 0
    HIDE = 1
    DURN = 2


class Document(Section):

    """Document types."""

    MAIN = 0
    TRAN = 1


class Format(Section):

    """Subtitle file formats."""

    ASS        = 0
    MICRODVD   = 1
    MPL2       = 2
    SSA        = 3
    SUBRIP     = 4
    SUBVIEWER2 = 5

    class_names = [
        'AdvancedSubStationAlpha',
        'MicroDVD',
        'MPL2',
        'SubStationAlpha',
        'SubRip',
        'SubViewer2',
    ]

    display_names = [
        _('Advanced Sub Station Alpha'),
        _('MicroDVD'),
        _('MPL2'),
        _('Sub Station Alpha'),
        _('SubRip'),
        _('SubViewer 2.0'),
    ]

    extensions = [
        '.ass',
        '.sub',
        '.txt',
        '.ssa',
        '.srt',
        '.sub',
    ]


class Framerate(Section):

    """Valid framerates."""

    FR_23_976 = 0
    FR_25     = 1
    FR_29_97  = 2

    display_names = [
        _('23.976 fps'),
        _('25 fps'),
        _('29.97 fps'),
    ]

    values = [
        23.976,
        25.0,
        29.97,
    ]


class Mode(Section):

    """Position modes."""

    TIME  = 0
    FRAME = 1


class Newlines(Section):

    """Newlines."""

    MAC     = 0
    UNIX    = 1
    WINDOWS = 2

    display_names = [
        _('Mac'),
        _('Unix'),
        _('Windows'),
    ]

    values = [
        '\r',
        '\n',
        '\r\n',
    ]


class VideoPlayer(Section):

    """Video players."""

    MPLAYER = 0
    VLC     = 1

    display_names = [
        _('MPlayer'),
        _('VLC'),
    ]

    _args = [
        '-identify -osdlevel 2 -ss %c -sub "%s" "%v"',
        '--start-time=%c --sub-file="%s" "%v"',
    ]

    commands = [
        'mplayer ' + _args[0],
        'vlc '     + _args[1],
    ]
    if sys.platform == 'win32':
        commands = [
            r'%ProgramFiles%\mplayer\mplayer.exe '  + _args[0],
            r'%ProgramFiles%\VideoLAN\vlc\vlc.exe ' + _args[1],
        ]
