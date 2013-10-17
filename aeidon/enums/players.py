# -*- coding: utf-8 -*-

# Copyright (C) 2005-2009,2013 Osmo Salomaa
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


def _get_ffplay_executable():
    if sys.platform == "win32":
        directory = os.environ.get("PROGRAMFILES", "C:\\Program Files")
        path = os.path.join(directory, "ffmpeg", "bin", "ffplay.exe")
        return aeidon.util.shell_quote(path)
    return "ffplay"

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



class FFplay(aeidon.EnumerationItem):

    command = " ".join((_get_ffplay_executable(),
                        "$VIDEOFILE",
                        "-ss $SECONDS",
                        "-fast",
                        "-scodec null",
                        "-vf subtitles=$SUBFILE"))

    # ffplay always assumes subtitles are UTF-8,
    # if not, the encoding would need to be specified.
    command_utf_8 = command
    label = "FFplay"


class MPlayer(aeidon.EnumerationItem):

    command = " ".join((_get_mplayer_executable(),
                        "-identify",
                        "-osdlevel 2",
                        "-ss $SECONDS",
                        "-slang",
                        "-noautosub",
                        "-sub $SUBFILE",
                        "$VIDEOFILE",))

    if sys.platform != "win32":
        # Required for mplayer to work if gaupol was started
        # as a background process (&) from a terminal window.
        # http://www.mplayerhq.hu/DOCS/HTML/en/faq.html#idp11051520
        command = "{} < /dev/null".format(command)
    command_utf_8 = " ".join((_get_mplayer_executable(),
                              "-identify",
                              "-osdlevel 2",
                              "-ss $SECONDS",
                              "-slang",
                              "-noautosub",
                              "-sub $SUBFILE",
                              "-utf8",
                              "$VIDEOFILE",))

    if sys.platform != "win32":
        # Required for mplayer to work if gaupol was started
        # as a background process (&) from a terminal window.
        # http://www.mplayerhq.hu/DOCS/HTML/en/faq.html#idp11051520
        command_utf_8 = "{} < /dev/null".format(command_utf_8)
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
players.FFPLAY = FFplay()
players.MPLAYER = MPlayer()
players.VLC = VLC()
