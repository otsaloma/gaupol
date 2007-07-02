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


"""Previewing subtitles with a video player."""


import atexit
import gaupol
import os
import string
import subprocess
import tempfile


class PreviewAgent(gaupol.Delegate):

    """Previewing subtitles with a video player."""

    # pylint: disable-msg=E0203,W0201

    __metaclass__ = gaupol.Contractual

    def __init__(self, master):

        gaupol.Delegate.__init__(self, master)
        gaupol.util.connect(self, self, "notify::main_file")

    def _get_subtitle_path_require(self, doc):
        assert self.get_file(doc) is not None

    def _get_subtitle_path(self, doc):
        """Save the subtitle data to a temporary file if needed.

        Raise IOError if writing to temporary file fails.
        Raise UnicodeError if encoding temporary file fails.
        Return subtitle file path, True if file is temporary.
        """
        if doc == gaupol.DOCUMENT.MAIN:
            if not self.main_changed:
                return self.main_file.path
        if doc == gaupol.DOCUMENT.TRAN:
            if not self.tran_changed:
                return self.tran_file.path
        return self.get_temp_file_path(doc)

    def _on_notify_main_file(self, *args):
        """Guess the video file path if unset."""

        if not self.video_path:
            self.guess_video_path()

    def _get_temp_file_path_require(self, doc):
        assert self.get_file(doc) is not None

    def _get_temp_file_path_ensure(self, value, doc):
        assert os.path.isfile(value)

    def get_temp_file_path(self, doc):
        """Save the subtitle data to a temporary file and return path.

        Raise IOError if writing to temporary file fails.
        Raise UnicodeError if encoding temporary file fails.
        """
        file = self.get_file(doc)
        path = tempfile.mkstemp(file.format.extension, "gaupol.")[1]
        props = (path, file.format, file.encoding, file.newline)
        self.save(doc, props, False)
        return path

    @gaupol.util.asserted_return
    def guess_video_path(self, extensions=None):
        """Guess and return the video file path based on main file's path.

        extensions should be a list of video file extensions or None for
        defaults. The video file is searched for in the same directory as the
        subtitle file. The subtitle file's filename without extension is
        assumed to start with or match the video file's filename without
        extension.
        """
        assert self.main_file is not None
        extensions = extensions or (
            ".3ivx", ".asf", ".avi", ".dat", ".divx", ".m2v", ".mkv", ".mov",
            ".mp4", ".mpeg", ".mpg", ".ogg", ".ogm", ".qt", ".rm", ".rmvb",
            ".swf", ".vob", ".wmv",)
        subroot = os.path.splitext(self.main_file.path)[0]
        dirname = os.path.dirname(self.main_file.path)
        for filename in os.listdir(dirname):
            filepath = os.path.join(dirname, filename)
            fileroot, extension = os.path.splitext(filepath)
            if (extension in extensions) and subroot.startswith(fileroot):
                self.video_path = filepath
                return self.video_path
        return None

    def preview_require(self, time, doc, command, offset, sub_path=None):
        assert self.get_file(doc) is not None
        assert self.video_path is not None

    def preview_ensure(self, value, *args, **kwargs):
        assert os.path.isfile(value[2])

    def preview(self, time, doc, command, offset, sub_path=None):
        """Preview subtitles with a video player.

        command should have variables $SECONDS, $SUBFILE and $VIDEOFILE.
        offset is the amount of seconds before time to start.
        sub_path can be a temporary subtitle file path.
        Raise IOError if writing to temporary file fails.
        Raise UnicodeError if encoding temporary file fails.
        Return subprocess.POpen instance, command, output path.
        """
        sub_path = sub_path or self._get_subtitle_path(doc)
        remove = gaupol.util.silent(OSError)(os.remove)
        if sub_path != self.get_file(doc).path:
            atexit.register(remove, sub_path)
        output_fd, output_path = tempfile.mkstemp(".output", "gaupol.")
        atexit.register(remove, output_path)
        seconds = self.calc.time_to_seconds(time)
        seconds = "%.3f" % max(0.0, seconds - float(offset))
        command = string.Template(command).safe_substitute(
            SECONDS=seconds, SUBFILE=gaupol.util.shell_quote(sub_path),
            VIDEOFILE=gaupol.util.shell_quote(self.video_path))
        process = gaupol.util.start_process(
            command, stderr=subprocess.STDOUT, stdout=output_fd)
        return process, command, output_path
