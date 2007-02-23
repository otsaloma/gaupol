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

    DOCUMENT.MAIN
    DOCUMENT.TRAN
    DOCUMENT.members
    DOCUMENT.names

    FORMAT.ASS
    FORMAT.MICRODVD
    FORMAT.MPL2
    FORMAT.MPSUB
    FORMAT.SSA
    FORMAT.SUBRIP
    FORMAT.SUBVIEWER2
    FORMAT.TMPLAYER
    FORMAT.class_names
    FORMAT.display_names
    FORMAT.extensions
    FORMAT.members
    FORMAT.names

    FRAMERATE.FR_23_976
    FRAMERATE.FR_25
    FRAMERATE.FR_29_97
    FRAMERATE.display_names
    FRAMERATE.members
    FRAMERATE.names
    FRAMERATE.mpsub_names
    FRAMERATE.values

    MODE.TIME
    MODE.FRAME
    MODE.members
    MODE.names

    NEWLINE.MAC
    NEWLINE.UNIX
    NEWLINE.WINDOWS
    NEWLINE.display_names
    NEWLINE.members
    NEWLINE.names
    NEWLINE.values

    REGISTER.DO
    REGISTER.UNDO
    REGISTER.REDO
    REGISTER.DO_MULTIPLE
    REGISTER.UNDO_MULTIPLE
    REGISTER.REDO_MULTIPLE
    REGISTER.members
    REGISTER.names
    REGISTER.shifts
    REGISTER.signals

    VIDEO_PLAYER.MPLAYER
    VIDEO_PLAYER.VLC
    VIDEO_PLAYER.commands
    VIDEO_PLAYER.display_names
    VIDEO_PLAYER.members
    VIDEO_PLAYER.names
"""

# pylint: disable-msg=E1101


import sys
from gettext import gettext as _

from gaupol.base import cons


__all__ = [
    "DOCUMENT",
    "FORMAT",
    "FRAMERATE",
    "MODE",
    "NEWLINE",
    "REGISTER",
    "VIDEO_PLAYER",]

DOCUMENT = cons.Section()
DOCUMENT.MAIN = cons.Member()
DOCUMENT.TRAN = cons.Member()
DOCUMENT.finalize()

FORMAT = cons.Section()
FORMAT.ASS = cons.Member()
FORMAT.ASS.class_name = "AdvSubStationAlpha"
FORMAT.ASS.display_name = "Advanced Sub Station Alpha"
FORMAT.ASS.extension = ".ass"
FORMAT.MICRODVD = cons.Member()
FORMAT.MICRODVD.class_name = "MicroDVD"
FORMAT.MICRODVD.display_name = "MicroDVD"
FORMAT.MICRODVD.extension = ".sub"
FORMAT.MPL2 = cons.Member()
FORMAT.MPL2.class_name = "MPL2"
FORMAT.MPL2.display_name = "MPL2"
FORMAT.MPL2.extension = ".txt"
FORMAT.MPSUB = cons.Member()
FORMAT.MPSUB.class_name = "MPsub"
FORMAT.MPSUB.display_name = "MPsub"
FORMAT.MPSUB.extension = ".sub"
FORMAT.SSA = cons.Member()
FORMAT.SSA.class_name = "SubStationAlpha"
FORMAT.SSA.display_name = "Sub Station Alpha"
FORMAT.SSA.extension = ".ssa"
FORMAT.SUBRIP = cons.Member()
FORMAT.SUBRIP.class_name = "SubRip"
FORMAT.SUBRIP.display_name = "SubRip"
FORMAT.SUBRIP.extension = ".srt"
FORMAT.SUBVIEWER2 = cons.Member()
FORMAT.SUBVIEWER2.class_name = "SubViewer2"
FORMAT.SUBVIEWER2.display_name = "SubViewer 2.0"
FORMAT.SUBVIEWER2.extension = ".sub"
FORMAT.TMPLAYER = cons.Member()
FORMAT.TMPLAYER.class_name = "TMPlayer"
FORMAT.TMPLAYER.display_name = "TMPlayer"
FORMAT.TMPLAYER.extension = ".txt"
FORMAT.finalize()

FRAMERATE = cons.Section()
FRAMERATE.FR_23_976 = cons.Member()
FRAMERATE.FR_23_976.display_name = _("23.976 fps")
FRAMERATE.FR_23_976.mpsub_name = "23.98"
FRAMERATE.FR_23_976.value = 23.976
FRAMERATE.FR_25 = cons.Member()
FRAMERATE.FR_25.display_name = _("25 fps")
FRAMERATE.FR_25.mpsub_name = "25.00"
FRAMERATE.FR_25.value = 25.0
FRAMERATE.FR_29_97 = cons.Member()
FRAMERATE.FR_29_97.display_name = _("29.97 fps")
FRAMERATE.FR_29_97.mpsub_name = "29.97"
FRAMERATE.FR_29_97.value = 29.97
FRAMERATE.finalize()

MODE = cons.Section()
MODE.TIME = cons.Member()
MODE.FRAME = cons.Member()
MODE.finalize()

NEWLINE = cons.Section()
NEWLINE.MAC = cons.Member()
NEWLINE.MAC.display_name = "Mac"
NEWLINE.MAC.value = "\r"
NEWLINE.UNIX = cons.Member()
NEWLINE.UNIX.display_name = "Unix"
NEWLINE.UNIX.value = "\n"
NEWLINE.WINDOWS = cons.Member()
NEWLINE.WINDOWS.display_name = "Windows"
NEWLINE.WINDOWS.value = "\r\n"
NEWLINE.finalize()

REGISTER = cons.Section()
REGISTER.DO = cons.Member()
REGISTER.DO.shift = 1
REGISTER.DO.signal = "action-done"
REGISTER.UNDO = cons.Member()
REGISTER.UNDO.shift = -1
REGISTER.UNDO.signal = "action-undone"
REGISTER.REDO = cons.Member()
REGISTER.REDO.shift = 1
REGISTER.REDO.signal = "action-redone"
REGISTER.DO_MULTIPLE = cons.Member()
REGISTER.DO_MULTIPLE.shift = 1
REGISTER.DO_MULTIPLE.signal = "action-done"
REGISTER.UNDO_MULTIPLE = cons.Member()
REGISTER.UNDO_MULTIPLE.shift = -1
REGISTER.UNDO_MULTIPLE.signal = "action-undone"
REGISTER.REDO_MULTIPLE = cons.Member()
REGISTER.REDO_MULTIPLE.shift = 1
REGISTER.REDO_MULTIPLE.signal = "action-redone"
REGISTER.finalize()

VIDEO_PLAYER = cons.Section()
VIDEO_PLAYER.MPLAYER = cons.Member()
VIDEO_PLAYER.MPLAYER.command = " ".join((
    "mplayer",
    "-identify",
    "-osdlevel 2",
    "-ss $SECONDS",
    "-sub $SUBFILE",
    "$VIDEOFILE",))
VIDEO_PLAYER.MPLAYER.display_name = "MPlayer"
VIDEO_PLAYER.VLC = cons.Member()
VIDEO_PLAYER.VLC.command = " ".join((
    "vlc",
    "--start-time=$SECONDS",
    "--sub-file=$SUBFILE",
    "$VIDEOFILE",))
VIDEO_PLAYER.VLC.display_name = "VLC"
if sys.platform == "win32":
    VIDEO_PLAYER.MPLAYER.command[0:7] = r"%ProgramFiles%\mplayer\mplayer.exe"
    VIDEO_PLAYER.VLC.command[0:3] = r"%ProgramFiles%\VideoLAN\vlc\vlc.exe"
VIDEO_PLAYER.finalize()
