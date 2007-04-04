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


"""Previewing subtitles with a video player.

Module variables:

    _EXTENSIONS: List of video file extensions used for guessing
"""


import os
import string
import subprocess
import tempfile

from gaupol import cons, util
from gaupol.base import Delegate


_EXTENSIONS = (
    ".3ivx", ".asf", ".avi", ".dat", ".divx", ".m2v", ".mkv", ".mov", ".mp4",
    ".mpeg", ".mpg", ".ogg", ".ogm", ".qt", ".rm", ".rmvb", ".swf", ".vob",
    ".wmv",)


class PreviewAgent(Delegate):

    """Previewing subtitles with a video player."""

    # pylint: disable-msg=E0203,W0201

    def __init__(self, master):

        Delegate.__init__(self, master)

        util.connect(self, self, "notify::main_file")

    def _get_subtitle_path(self, doc):
        """Save the subtitle data to a temporary file if needed.

        Raise IOError if writing to temporary file fails.
        Raise UnicodeError if encoding temporary file fails.
        Return subtitle file path, True if file is temporary.
        """
        if doc == cons.DOCUMENT.MAIN:
            if not self.main_changed:
                return self.main_file.path, False
        if doc == cons.DOCUMENT.TRAN:
            if not self.tran_active or not self.tran_changed:
                return self.tran_file.path, False
        return self.get_temp_file_path(doc), True

    def _on_notify_main_file(self, *args):
        """Guess the video file path if it is unset."""

        if not self.video_path:
            self.guess_video_path()

    def get_temp_file_path(self, doc):
        """Save the subtitle data to a temporary file and return path.

        Raise IOError if writing to temporary file fails.
        Raise UnicodeError if encoding temporary file fails.
        """
        file = self.get_file(doc)
        extension = file.format.extension
        path = tempfile.mkstemp(prefix="gaupol.", suffix=extension)[1]
        props = (path, file.format, file.encoding, file.newline)
        self.save(doc, props, False)
        return path

    def guess_video_path(self, extensions=_EXTENSIONS):
        """Guess the video file path based on main file's path.

        Video file is searched for in the same directory as the subtitle file.
        Subtitle file's filename without extension is assumed to start with or
        match video file's filename without extension.
        Return the video file path or None.
        """
        if self.main_file is None:
            return None
        subroot = os.path.splitext(self.main_file.path)[0]
        dirname = os.path.dirname(self.main_file.path)
        for filename in os.listdir(dirname):
            filepath = os.path.join(dirname, filename)
            fileroot, extension = os.path.splitext(filepath)
            if (extension in extensions) and subroot.startswith(fileroot):
                self.video_path = filepath
                return filepath
        return None

    def preview(self, time, doc, command, offset, temp_path=None):
        """Preview subtitles with a video player.

        command should have variables $SECONDS, $SUBFILE and $VIDEOFILE.
        offset is the amount of seconds before time to start.
        temp_path should be a temporary subtitle file path if already written.

        Raise IOError if writing to temporary file fails.
        Raise UnicodeError if encoding temporary file fails.
        Return subprocess.POpen instance, command,
        path to output file, path to temporary file.
        """
        sub_path = temp_path
        is_temp = temp_path is not None
        if temp_path is None:
            sub_path, is_temp = self._get_subtitle_path(doc)
        temp_path = (sub_path if is_temp else None)

        output_fd, output_path = tempfile.mkstemp(
            prefix="gaupol.", suffix=".output")
        seconds = self.calc.time_to_seconds(time)
        seconds = "%.3f" % max(0.0, seconds - float(offset))
        command = string.Template(command).safe_substitute(
            SECONDS=seconds,
            SUBFILE=util.shell_quote(sub_path),
            VIDEOFILE=util.shell_quote(self.video_path))

        process = util.start_process(
            command, stderr=subprocess.STDOUT, stdout=output_fd)
        return process, command, output_path, temp_path
