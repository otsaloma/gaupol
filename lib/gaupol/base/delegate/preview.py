# Copyright (C) 2005-2006 Osmo Salomaa
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


"""Previewing subtitles with video player."""


import os
import string
import subprocess
import tempfile

from gaupol.base          import cons
from gaupol.base.colcons  import *
from gaupol.base.delegate import Delegate
from gaupol.base.error    import ExternalError


EXTENSIONS = (
    '.3ivx',
    '.asf',
    '.avi',
    '.dat',
    '.divx',
    '.m2v',
    '.mkv',
    '.mov',
    '.mp4',
    '.mpeg',
    '.mpg',
    '.ogg',
    '.ogm',
    '.qt',
    '.rm',
    '.rmvb',
    '.swf',
    '.vob',
    '.wmv',
)


class PreviewDelegate(Delegate):

    """Previewing subtitles with video player."""

    def _get_subtitle_path(self, doc):
        """
        Save subtitle data to a temporary file if needed.

        Raise IOError if writing to temporary file fails.
        Raise UnicodeError if encoding temporary file fails.
        Return subtitle file path, is temporary file.
        """
        if doc == cons.Document.MAIN:
            if not self.main_changed:
                return self.main_file.path, False
        elif doc == cons.Document.TRAN:
            if not self.tran_active and not self.tran_changed:
                return self.tran_file.path, False

        return self.get_temp_file_path(doc), True

    def get_temp_file_path(self, doc):
        """
        Save data to a temporary file and return path.

        Raise IOError if writing to temporary file fails.
        Raise UnicodeError if encoding temporary file fails.
        """
        file_ = (self.main_file, self.tran_file)[doc]
        extension = cons.Format.extensions[file_.format]
        path = tempfile.mkstemp(extension, 'gaupol.')[1]

        props = (path, file_.format, file_.encoding, file_.newlines)
        if doc == cons.Document.MAIN:
            self.save_main_file(False, props)
        elif doc == cons.Document.TRAN:
            self.save_translation_file(False, props)

        return path

    def guess_video_path(self, extensions=EXTENSIONS):
        """
        Guess video file path based on main file path.

        Video file is searched for in the same directory as the subtitle file.
        Subtitle file's filename without extension is assumed to start with or
        match video file's filename without extension.

        Return video file path or None.
        """
        subroot = os.path.splitext(self.main_file.path)[0]
        dirname = os.path.dirname(self.main_file.path)
        for filename in os.listdir(dirname):
            filepath = os.path.join(dirname, filename)
            fileroot, extension = os.path.splitext(filepath)
            if subroot.startswith(fileroot):
                if extension in extensions:
                    self.video_path = filepath
                    return filepath
        return None

    def preview(self, time, doc, command, offset, temp_path=None):
        """
        Preview subtitles with video player.

        command: String, with following variables allowed

            ${seconds}
            ${subfile}
            ${videofile}

        offset: Float-convertible, seconds before row's show time to start
        temp_path: Temporary subtitle file path if already written

        First dump the current subtitle data to a temporary file if the
        subtitle file is changed and then launch an external video player to
        view the video file with the subtitle file.

        Raise IOError if writing to temporary file fails.
        Raise UnicodeError if encoding temporary file fails.
        Raise ExternalError if command fails.
        Raise ValueError if command is a blank string.
        """
        if command == '':
            raise ValueError
        sub_path = temp_path
        is_temp = True
        if temp_path is None:
            sub_path, is_temp = self._get_subtitle_path(doc)
        seconds = self.calc.time_to_seconds(time)
        seconds = max(0.0, seconds - float(offset))
        command = string.Template(command).safe_substitute(
            subfile=sub_path, videofile=self.video_path, seconds=str(seconds))
        output_fd, output_path = tempfile.mkstemp('.output', 'gaupol.')
        self.output = '$ ' + command + '\n\n'

        return_value = subprocess.Popen(
            command,
            stdout=output_fd,
            stderr=subprocess.STDOUT,
            shell=True,
            universal_newlines=True,
        ).wait()
        fobj = file(output_path, 'r')
        self.output += fobj.read()
        fobj.close()

        try:
            os.remove(output_path)
        except OSError:
            pass
        if is_temp:
            try:
                os.remove(sub_path)
            except OSError:
                pass
        if return_value != 0:
            raise ExternalError
