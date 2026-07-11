# -*- coding: utf-8 -*-

# Copyright (C) 2005 Osmo Salomaa
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

"""Text markup of all formats."""

import aeidon

from .ssa        import SubStationAlpha
from .ass        import AdvSubStationAlpha
from .lrc        import LRC
from .microdvd   import MicroDVD
from .mpl2       import MPL2
from .subrip     import SubRip
from .subviewer2 import SubViewer2
from .tmplayer   import TMPlayer
from .webvtt     import WebVTT

classes = [
    SubStationAlpha,
    AdvSubStationAlpha,
    LRC,
    MicroDVD,
    MPL2,
    SubRip,
    SubViewer2,
    TMPlayer,
    WebVTT,
]

def add(cls):
    """Add a new :class:`aeidon.Markup` class."""
    globals()[cls.__name__] = cls
    classes.append(cls)

def new(format):
    """Return a new :class:`aeidon.Markup` instance given `format`."""
    for cls in classes:
        if cls.format == format:
            return cls()
    raise ValueError("Format {!r} not found"
                     .format(format))
