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
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""Previewing subtitles with a video player."""

import aeidon
import os
import string


class PreviewAgent(aeidon.Delegate):

    """Previewing subtitles with a video player."""

    def __init__(self, master):
        """Initialize a :class:`aeidon.PreviewAgent` instance."""
        aeidon.Delegate.__init__(self, master)
        aeidon.util.connect(self, self, "notify::main_file")

    @aeidon.deco.export
    def find_video(self):
        """
        Find and return the video file path based on main file's path.

        The video file is searched for in the same directory as the subtitle
        file. The subtitle file's filename without extension is assumed to
        start with or match the video file's filename without extension,
        e.g. 'movie.avi' for 'movie.en.srt'.
        """
        if self.main_file is None: return None
        dirname = os.path.dirname(self.main_file.path)
        subname = os.path.basename(self.main_file.path)
        for name in os.listdir(dirname):
            path = os.path.join(dirname, name)
            root = os.path.splitext(name)[0]
            if not subname.startswith(root): continue
            if aeidon.util.is_video_file(path):
                self.video_path = path
                return self.video_path
        return None

    def _get_subtitle_path(self, doc, encoding=None, temp=False):
        """
        Return path to a file to preview, either real or temporary.

        Raise :exc:`IOError` if writing to temporary file fails.
        Raise :exc:`UnicodeError` if encoding temporary file fails.
        """
        file = self.get_file(doc)
        if file is None or encoding != file.encoding:
            return self.new_temp_file(doc)
        if doc == aeidon.documents.MAIN:
            if not self.main_changed and not temp:
                return self.main_file.path
        if doc == aeidon.documents.TRAN:
            if not self.tran_changed and not temp:
                return self.tran_file.path
        return self.new_temp_file(doc)

    def _on_notify_main_file(self, *args):
        """Try to find the video file path if unset."""
        if self.video_path is None:
            self.find_video()

    @aeidon.deco.export
    def preview(self, position, doc, command, offset, encoding=None, temp=False):
        """
        Start video player with `command` from `position`.

        `command` can have variables ``$MILLISECONDS``, ``$SECONDS``,
        ``$SUBFILE`` and ``$VIDEOFILE``. `offset` should be the amount
        of seconds before `position` to start. `encoding` can be specified
        if different from `doc` file encoding. Use ``True`` for `temp` to
        always use a temporary file for preview regardless of whether
        the file is changed or not.

        Return a three tuple of :class:`subprocess.POpen` instance, command
        with variables expanded and a file object to which process standard
        output and standard error are directed.

        Raise :exc:`IOError` if writing to temporary file fails.
        Raise :exc:`UnicodeError` if encoding temporary file fails.
        Raise :exc:`aeidon.ProcessError` if unable to start process.
        """
        sub_path = self._get_subtitle_path(doc, encoding, temp=temp)
        fout = open(aeidon.temp.create(".output"), "w")
        seconds = max(0, self.calc.to_seconds(position) - offset)
        command = string.Template(command).safe_substitute(
            MILLISECONDS=("{:.0f}".format(seconds * 1000)),
            SECONDS=("{:.3f}".format(seconds)),
            SUBFILE=aeidon.util.shell_quote(sub_path),
            VIDEOFILE=aeidon.util.shell_quote(self.video_path))

        process = aeidon.util.start_process(command, stderr=fout, stdout=fout)
        return process, command, fout
