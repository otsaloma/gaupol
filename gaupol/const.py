# Copyright (C) 2005-2007 Osmo Salomaa
#
# This file is part of Gaupol.
#
# Gaupol is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# Gaupol is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# Gaupol.  If not, see <http://www.gnu.org/licenses/>.

"""Constants."""

# pylint: disable-msg=E1101,W0201

import gaupol
import os
import sys
_ = gaupol.i18n._

DOCUMENT = gaupol.ConstantSection()
DOCUMENT.MAIN = gaupol.ConstantMember()
DOCUMENT.TRAN = gaupol.ConstantMember()
DOCUMENT.finalize()

FORMAT = gaupol.ConstantSection()
FORMAT.ASS = gaupol.ConstantMember()
FORMAT.ASS.label = "Advanced Sub Station Alpha"
FORMAT.ASS.extension = ".ass"
FORMAT.ASS.has_header = True
FORMAT.ASS.identifier = r"^ScriptType:\s*[vV]4.00\+\s*$"
FORMAT.MICRODVD = gaupol.ConstantMember()
FORMAT.MICRODVD.label = "MicroDVD"
FORMAT.MICRODVD.extension = ".sub"
FORMAT.MICRODVD.has_header = True
FORMAT.MICRODVD.identifier = r"^\{-?\d+\}\{-?\d+\}"
FORMAT.MPL2 = gaupol.ConstantMember()
FORMAT.MPL2.label = "MPL2"
FORMAT.MPL2.extension = ".txt"
FORMAT.MPL2.has_header = False
FORMAT.MPL2.identifier = r"^\[-?\d+\]\[-?\d+\]"
FORMAT.MPSUB = gaupol.ConstantMember()
FORMAT.MPSUB.label = "MPsub"
FORMAT.MPSUB.extension = ".sub"
FORMAT.MPSUB.has_header = True
FORMAT.MPSUB.identifier = r"^FORMAT=(TIME|[\d\.]+)\s*$"
FORMAT.SSA = gaupol.ConstantMember()
FORMAT.SSA.label = "Sub Station Alpha"
FORMAT.SSA.extension = ".ssa"
FORMAT.SSA.has_header = True
FORMAT.SSA.identifier = r"^ScriptType:\s*[vV]4.00\s*$"
FORMAT.SUBRIP = gaupol.ConstantMember()
FORMAT.SUBRIP.label = "SubRip"
FORMAT.SUBRIP.extension = ".srt"
FORMAT.SUBRIP.has_header = False
FORMAT.SUBRIP.identifier = r"^-?\d\d:\d\d:\d\d,\d\d\d --> -?\d\d:\d\d:\d\d,\d\d\d\s*$"
FORMAT.SUBVIEWER2 = gaupol.ConstantMember()
FORMAT.SUBVIEWER2.label = "SubViewer 2.0"
FORMAT.SUBVIEWER2.extension = ".sub"
FORMAT.SUBVIEWER2.has_header = True
FORMAT.SUBVIEWER2.identifier = r"^-?\d\d:\d\d:\d\d\.\d\d,-?\d\d:\d\d:\d\d\.\d\d\s*$"
FORMAT.TMPLAYER = gaupol.ConstantMember()
FORMAT.TMPLAYER.label = "TMPlayer"
FORMAT.TMPLAYER.extension = ".txt"
FORMAT.TMPLAYER.has_header = False
FORMAT.TMPLAYER.identifier = r"^-?\d\d:\d\d:\d\d:"
FORMAT.finalize()

FRAMERATE = gaupol.ConstantSection()
FRAMERATE.P24 = gaupol.ConstantMember()
FRAMERATE.P24.label = _("24 fps")
FRAMERATE.P24.mpsub = "23.98"
FRAMERATE.P24.value = 24 / 1.001
FRAMERATE.P25 = gaupol.ConstantMember()
FRAMERATE.P25.label = _("25 fps")
FRAMERATE.P25.mpsub = "25.00"
FRAMERATE.P25.value = 25.0
FRAMERATE.P30 = gaupol.ConstantMember()
FRAMERATE.P30.label = _("30 fps")
FRAMERATE.P30.mpsub = "29.97"
FRAMERATE.P30.value = 30 / 1.001
FRAMERATE.finalize()

MODE = gaupol.ConstantSection()
MODE.TIME = gaupol.ConstantMember()
MODE.FRAME = gaupol.ConstantMember()
MODE.finalize()

NEWLINE = gaupol.ConstantSection()
NEWLINE.MAC = gaupol.ConstantMember()
NEWLINE.MAC.label = "Mac (classic)"
NEWLINE.MAC.value = "\r"
NEWLINE.UNIX = gaupol.ConstantMember()
NEWLINE.UNIX.label = "Unix"
NEWLINE.UNIX.value = "\n"
NEWLINE.WINDOWS = gaupol.ConstantMember()
NEWLINE.WINDOWS.label = "Windows"
NEWLINE.WINDOWS.value = "\r\n"
NEWLINE.finalize()

REGISTER = gaupol.ConstantSection()
REGISTER.DO = gaupol.ConstantMember()
REGISTER.DO.shift = 1
REGISTER.DO.signal = "action-done"
REGISTER.UNDO = gaupol.ConstantMember()
REGISTER.UNDO.shift = -1
REGISTER.UNDO.signal = "action-undone"
REGISTER.REDO = gaupol.ConstantMember()
REGISTER.REDO.shift = 1
REGISTER.REDO.signal = "action-redone"
REGISTER.finalize()

def get_mplayer_executable():
    if sys.platform == "win32":
        directory = os.environ.get("PROGRAMFILES", r"C:\Program Files")
        return os.path.join(directory, "mplayer", "mplayer.exe")
    return "mplayer"

def get_vlc_executable():
    if sys.platform == "win32":
        directory = os.environ.get("PROGRAMFILES", r"C:\Program Files")
        return os.path.join(directory, "VideoLAN", "VLC", "vlc.exe")
    return "vlc"

VIDEO_PLAYER = gaupol.ConstantSection()
VIDEO_PLAYER.MPLAYER = gaupol.ConstantMember()
VIDEO_PLAYER.MPLAYER.command = " ".join((
    get_mplayer_executable(),
    "-identify",
    "-osdlevel 2",
    "-ss $SECONDS",
    "-slang",
    "-noautosub",
    "-sub $SUBFILE",
    "$VIDEOFILE",))
VIDEO_PLAYER.MPLAYER.label = "MPlayer"
VIDEO_PLAYER.VLC = gaupol.ConstantMember()
VIDEO_PLAYER.VLC.command = " ".join((
    get_vlc_executable(),
    "$VIDEOFILE",
    ":start-time=$SECONDS",
    ":sub-file=$SUBFILE",))
VIDEO_PLAYER.VLC.label = "VLC"
VIDEO_PLAYER.finalize()

del get_mplayer_executable, get_vlc_executable
__all__ = [x for x in dir() if x.isupper()]
