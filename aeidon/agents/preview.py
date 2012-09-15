# -*- coding: utf-8 -*-

# Copyright (C) 2005-2010 Osmo Salomaa
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

"""Previewing subtitles with a video player."""

import aeidon
import os
import string
import subprocess


class PreviewAgent(aeidon.Delegate, metaclass=aeidon.Contractual):

    """Previewing subtitles with a video player."""

    def __init__(self, master):
        """Initialize a :class:`aeidon.PreviewAgent` object."""
        aeidon.Delegate.__init__(self, master)
        aeidon.util.connect(self, self, "notify::main_file")

    def _get_subtitle_path_require(self, doc, encoding=None, temp=False):
        if encoding is not None:
            assert aeidon.encodings.is_valid_code(encoding)

    def _get_subtitle_path(self, doc, encoding=None, temp=False):
        """
        Return path to a file to preview, either real or temporary.

        Raise :exc:`IOError` if writing to temporary file fails.
        Raise :exc:`UnicodeError` if encoding temporary file fails.
        """
        sfile = self.get_file(doc)
        if sfile is None or encoding != sfile.encoding:
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
        if not self.video_path:
            self.find_video()

    @aeidon.deco.export
    def find_video(self, extensions=None):
        """
        Find and return the video file path based on main file's path.

        `extensions` should be a sequence of video filename extensions or
        ``None`` for defaults. The video file is searched for in the same
        directory as the subtitle file. The subtitle file's filename without
        extension is assumed to start with or match the video file's filename
        without extension.
        """
        if self.main_file is None: return None
        extensions = list(extensions or (
                ".3ivx", ".asf", ".avi", ".divx", ".flv", ".m2v", ".mkv",
                ".mov", ".mp4", ".mpeg", ".mpg", ".ogm", ".ogv", ".qt", ".rm",
                ".rmvb", ".swf", ".vob", ".wmv",
                # Keep extensions used by other file types than video at the
                # end of the list, so that if there are multiple matches,
                # ambiguous extensions would not be the ones chosen.
                ".ogg", ".dat"))

        # Add upper-case versions of all extensions.
        extensions = aeidon.util.flatten([[x, x.upper()] for x in extensions])
        dirname = os.path.dirname(self.main_file.path)
        basename_sub = os.path.basename(self.main_file.path)
        rootname_sub = os.path.splitext(basename_sub)[0]
        for extension in extensions:
            for video_path in os.listdir(dirname):
                if not video_path.endswith(extension): continue
                basename_video = os.path.basename(video_path)
                rootname_video = os.path.splitext(basename_video)[0]
                if not rootname_sub.startswith(rootname_video): continue
                self.video_path = os.path.join(dirname, basename_video)
                return self.video_path
        return None

    def preview_require(self, *args, **kwargs):
        assert self.video_path is not None

    def preview_ensure(self, value, *args, **kwargs):
        assert os.path.isfile(value[2])

    @aeidon.deco.export
    def preview(self,
                position,
                doc,
                command,
                offset,
                encoding=None,
                temp=False):

        """
        Start video player with `command` from `position`.

        `command` can have variables ``$MILLISECONDS``, ``$SECONDS``,
        ``$SUBFILE`` and ``$VIDEOFILE``. `offset` should be the amount of
        seconds before `position` to start, which can be used to take into
        account that video players can usually seek only to keyframes, which
        exist maybe ten seconds or so apart. `encoding` can be specified if
        different from `doc` file encoding. Use ``True`` for `temp` to always
        use a temporary file for preview regardless of whether the file is
        changed or not.

        Return a three tuple of :class:`subprocess.POpen` instance, command
        with variables expanded and process standard output and error path.

        Raise :exc:`IOError` if writing to temporary file fails.
        Raise :exc:`UnicodeError` if encoding temporary file fails.
        Raise :exc:`aeidon.ProcessError` if unable to start process.
        """
        sub_path = self._get_subtitle_path(doc, encoding, temp=temp)
        output_path = aeidon.temp.create(".output")
        output_fd = aeidon.temp.get_handle(output_path)
        seconds = max(0, self.calc.to_seconds(position) - offset)
        command = string.Template(command).safe_substitute(
            MILLISECONDS=("{:.0f}".format(seconds * 1000)),
            SECONDS=("{:.3f}".format(seconds)),
            SUBFILE=aeidon.util.shell_quote(sub_path),
            VIDEOFILE=aeidon.util.shell_quote(self.video_path))

        process = aeidon.util.start_process(command,
                                            stderr=subprocess.STDOUT,
                                            stdout=output_fd)

        return process, command, output_path
