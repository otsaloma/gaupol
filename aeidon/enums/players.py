# Copyright (C) 2005-2009 Osmo Salomaa
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
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# Gaupol. If not, see <http://www.gnu.org/licenses/>.

"""Enumerations for video player application types."""

import aeidon
import os
import sys

__all__ = ("players",)


def _get_mplayer_executable():
    if sys.platform == "win32":
        directory = os.environ.get("PROGRAMFILES", "C:\\Program Files")
        path = os.path.join(directory, "MPlayer", "mplayer.exe")
        return aeidon.util.shell_quote(path)
    return "mplayer"

def _get_vlc_executable():
    if sys.platform == "win32":
        directory = os.environ.get("PROGRAMFILES", "C:\\Program Files")
        path = os.path.join(directory, "VideoLAN", "VLC", "vlc.exe")
        return aeidon.util.shell_quote(path)
    return "vlc"


class MPlayer(aeidon.EnumerationItem):

    command = " ".join((_get_mplayer_executable(),
                        "-identify",
                        "-osdlevel 2",
                        "-ss $SECONDS",
                        "-slang",
                        "-noautosub",
                        "-sub $SUBFILE",
                        "$VIDEOFILE",))

    command_utf_8 = " ".join((_get_mplayer_executable(),
                              "-identify",
                              "-osdlevel 2",
                              "-ss $SECONDS",
                              "-slang",
                              "-noautosub",
                              "-sub $SUBFILE",
                              "-utf8",
                              "$VIDEOFILE",))

    label = "MPlayer"


class VLC(aeidon.EnumerationItem):

    command = " ".join((_get_vlc_executable(),
                        "$VIDEOFILE",
                        ":start-time=$SECONDS",
                        ":sub-file=$SUBFILE",))

    command_utf_8 = " ".join((_get_vlc_executable(),
                              "$VIDEOFILE",
                              ":start-time=$SECONDS",
                              ":sub-file=$SUBFILE",
                              ":subsdec-encoding=UTF-8",))

    label = "VLC"


players = aeidon.Enumeration()
players.MPLAYER = MPlayer()
players.VLC = VLC()
