# Copyright (C) 2005-2007 Osmo Salomaa
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


"""Constants.

Module variables:

    DOCUMENT, FORMAT, FRAMERATE, MODE, NEWLINE, REGISTER, VIDEO_PLAYER
"""


import sys
from gettext import gettext as _

from gaupol.base import const


# All defined constants.
__all__ = set(locals())

DOCUMENT = const.Section()
DOCUMENT.MAIN = const.Member()
DOCUMENT.TRAN = const.Member()
DOCUMENT.finalize()

FORMAT = const.Section()
FORMAT.ASS = const.Member()
FORMAT.ASS.class_name = "AdvSubStationAlpha"
FORMAT.ASS.display_name = "Advanced Sub Station Alpha"
FORMAT.ASS.extension = ".ass"
FORMAT.MICRODVD = const.Member()
FORMAT.MICRODVD.class_name = "MicroDVD"
FORMAT.MICRODVD.display_name = "MicroDVD"
FORMAT.MICRODVD.extension = ".sub"
FORMAT.MPL2 = const.Member()
FORMAT.MPL2.class_name = "MPL2"
FORMAT.MPL2.display_name = "MPL2"
FORMAT.MPL2.extension = ".txt"
FORMAT.MPSUB = const.Member()
FORMAT.MPSUB.class_name = "MPsub"
FORMAT.MPSUB.display_name = "MPsub"
FORMAT.MPSUB.extension = ".sub"
FORMAT.SSA = const.Member()
FORMAT.SSA.class_name = "SubStationAlpha"
FORMAT.SSA.display_name = "Sub Station Alpha"
FORMAT.SSA.extension = ".ssa"
FORMAT.SUBRIP = const.Member()
FORMAT.SUBRIP.class_name = "SubRip"
FORMAT.SUBRIP.display_name = "SubRip"
FORMAT.SUBRIP.extension = ".srt"
FORMAT.SUBVIEWER2 = const.Member()
FORMAT.SUBVIEWER2.class_name = "SubViewer2"
FORMAT.SUBVIEWER2.display_name = "SubViewer 2.0"
FORMAT.SUBVIEWER2.extension = ".sub"
FORMAT.TMPLAYER = const.Member()
FORMAT.TMPLAYER.class_name = "TMPlayer"
FORMAT.TMPLAYER.display_name = "TMPlayer"
FORMAT.TMPLAYER.extension = ".txt"
FORMAT.finalize()

FRAMERATE = const.Section()
FRAMERATE.P24 = const.Member()
FRAMERATE.P24.display_name = _("23.976 fps")
FRAMERATE.P24.mpsub_name = "23.98"
FRAMERATE.P24.value = 23.976
FRAMERATE.P25 = const.Member()
FRAMERATE.P25.display_name = _("25 fps")
FRAMERATE.P25.mpsub_name = "25.00"
FRAMERATE.P25.value = 25.0
FRAMERATE.P30 = const.Member()
FRAMERATE.P30.display_name = _("29.97 fps")
FRAMERATE.P30.mpsub_name = "29.97"
FRAMERATE.P30.value = 29.97
FRAMERATE.finalize()

MODE = const.Section()
MODE.TIME = const.Member()
MODE.FRAME = const.Member()
MODE.finalize()

NEWLINE = const.Section()
NEWLINE.MAC = const.Member()
NEWLINE.MAC.display_name = "Mac (classic)"
NEWLINE.MAC.value = "\r"
NEWLINE.UNIX = const.Member()
NEWLINE.UNIX.display_name = "Unix"
NEWLINE.UNIX.value = "\n"
NEWLINE.WINDOWS = const.Member()
NEWLINE.WINDOWS.display_name = "Windows"
NEWLINE.WINDOWS.value = "\r\n"
NEWLINE.finalize()

REGISTER = const.Section()
REGISTER.DO = const.Member()
REGISTER.DO.shift = 1
REGISTER.DO.signal = "action-done"
REGISTER.UNDO = const.Member()
REGISTER.UNDO.shift = -1
REGISTER.UNDO.signal = "action-undone"
REGISTER.REDO = const.Member()
REGISTER.REDO.shift = 1
REGISTER.REDO.signal = "action-redone"
REGISTER.DO_MULTIPLE = const.Member()
REGISTER.DO_MULTIPLE.shift = 1
REGISTER.DO_MULTIPLE.signal = "action-done"
REGISTER.UNDO_MULTIPLE = const.Member()
REGISTER.UNDO_MULTIPLE.shift = -1
REGISTER.UNDO_MULTIPLE.signal = "action-undone"
REGISTER.REDO_MULTIPLE = const.Member()
REGISTER.REDO_MULTIPLE.shift = 1
REGISTER.REDO_MULTIPLE.signal = "action-redone"
REGISTER.finalize()

def get_mplayer_executable():
    if sys.platform == "win32":
        return r"%ProgramFiles%\mplayer\mplayer.exe"
    return "mplayer"

def get_vlc_executable():
    if sys.platform == "win32":
        return r"%ProgramFiles%\VideoLAN\vlc\vlc.exe"
    return "vlc"

VIDEO_PLAYER = const.Section()
VIDEO_PLAYER.MPLAYER = const.Member()
VIDEO_PLAYER.MPLAYER.command = " ".join((
    get_mplayer_executable(),
    "-identify",
    "-osdlevel 2",
    "-ss $SECONDS",
    "-sub $SUBFILE",
    "$VIDEOFILE",))
VIDEO_PLAYER.MPLAYER.display_name = "MPlayer"
VIDEO_PLAYER.VLC = const.Member()
VIDEO_PLAYER.VLC.command = " ".join((
    get_vlc_executable(),
    "--start-time=$SECONDS",
    "--sub-file=$SUBFILE",
    "$VIDEOFILE",))
VIDEO_PLAYER.VLC.display_name = "VLC"
VIDEO_PLAYER.finalize()

del get_mplayer_executable, get_vlc_executable
__all__ = sorted(list(set(locals()) - __all__))
