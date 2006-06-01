# Copyright (C) 2005 Osmo Salomaa
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


try:
    from psyco.classes import *
except ImportError:
    pass

import os
import subprocess
import tempfile

from gaupol.base.colcons import *
from gaupol.base.delegates    import Delegate
from gaupol.base.error        import ExternalError
from gaupol.base.cons         import Document, Format


default_extensions = (
    '.asf',
    '.avi',
    '.dat',
    '.divx',
    '.mkv',
    '.mov',
    '.mpeg',
    '.mpg',
    '.mp4',
    '.m2v',
    '.ogg',
    '.ogm',
    '.qt',
    '.rm',
    '.rmvb',
    '.swf',
    '.vob',
    '.wmv',
    '.3ivx',
)


class PreviewDelegate(Delegate):

    """Previewing subtitles with video player."""

    def _get_subtitle_path(self, document):
        """
        Save subtitle data to a temporary file if needed.

        Raise IOError if writing to temporary file fails.
        Raise UnicodeError if encoding temporary file fails.
        Return subtitle file path, is temporary file.
        """
        if document == Document.MAIN:
            if not self.main_changed:
                return self.main_file.path, False
        elif document == Document.TRAN:
            if not self.tran_active and not self.tran_changed:
                return self.tran_file.path, False

        return self.get_temp_file_path(document), True

    def get_temp_file_path(self, document):
        """
        Save data to a temporary file and return path.

        Raise IOError if writing to temporary file fails.
        Raise UnicodeError if encoding temporary file fails.
        """
        sub_file  = (self.main_file, self.tran_file)[document]
        extension = Format.extensions[sub_file.format]
        sub_path  = tempfile.mkstemp(extension, 'gaupol.')[1]

        properties = (
            sub_path,
            sub_file.format,
            sub_file.encoding,
            sub_file.newlines
        )

        if document == Document.MAIN:
            self.save_main_file(False, properties)
        elif document == Document.TRAN:
            self.save_translation_file(False, properties)

        return sub_path

    def guess_video_file_path(self, extensions=default_extensions):
        """
        Guess video file path based on main file path.

        Video file is searched for in the same directory as the subtitle file.
        Subtitle file's filename without extension is assumed to start with or
        match video file's filename without extension.

        Return video file path or None.
        """
        assert self.main_file is not None

        subroot   = os.path.splitext(self.main_file.path)[0]
        dirname   = os.path.dirname(self.main_file.path)
        filenames = os.listdir(dirname)

        for filename in filenames:
            filepath = os.path.join(dirname, filename)
            fileroot, extension = os.path.splitext(filepath)
            if subroot.startswith(fileroot) and extension in extensions:
                self.video_path = filepath
                return filepath

        return None

    def preview_row(self, row, document, command, offset, temp_path=None):
        """Preview subtitles at row with video player."""

        time = self.times[row][SHOW]
        self.preview_time(time, document, command, offset, temp_path)

    def preview_time(self, time, document, command, offset, temp_path=None):
        """
        Preview subtitles at time with video player.

        command: string, where %s = subtitle filepath, %v = video filepath,
        %t = time, %c = seconds and %f = frame
        offset: float-convertable, seconds before row's show time to start
        temp_path: temporary subtitle file path if already written

        First dump the current subtitle data to a temporary file if the
        subtitle file is changed and then launch an external video player to
        view the video file with the subtitle file.

        Raise IOError if writing to temporary file fails.
        Raise UnicodeError if encoding temporary file fails.
        Raise ExternalError if command fails.
        """
        sub_file = (self.main_file, self.tran_file)[document]
        assert sub_file is not None
        assert self.video_path is not None

        seconds = self.calc.time_to_seconds(time)
        seconds = max(0.0, seconds - float(offset))

        time    = str(self.calc.seconds_to_time(seconds))
        frame   = str(self.calc.seconds_to_frame(seconds))
        seconds = str(seconds)

        if temp_path is not None:
            sub_path = temp_path
            is_temp  = True
        else:
            sub_path, is_temp = self._get_subtitle_path(document)
        output_fd, output_path = tempfile.mkstemp('.output', 'gaupol.')

        command = command.replace('%s', sub_path       )
        command = command.replace('%v', self.video_path)
        command = command.replace('%t', time           )
        command = command.replace('%c', seconds        )
        command = command.replace('%f', frame          )

        self.output = '$ %s\n' % command

        # Run video player and wait for exit.
        popen = subprocess.Popen(
            command,
            stdout=output_fd,
            stderr=subprocess.STDOUT,
            shell=True,
            universal_newlines=True,
        )
        return_value = popen.wait()

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


if __name__ == '__main__':

    from gaupol.test import Test

    class TestPreviewDelegate(Test):

        def __init__(self):

            Test.__init__(self)
            self.project = self.get_project()

        def test_get_subtitle_path(self):

            delegate = PreviewDelegate(self.project)
            data = delegate._get_subtitle_path(Document.MAIN)
            assert data == (self.project.main_file.path, False)

            self.project.clear_texts([0], Document.MAIN)
            data = delegate._get_subtitle_path(Document.MAIN)
            self.files.append(data[0])
            assert data[0] != self.project.main_file.path
            assert data[1] is True
            assert self.project.main_changed == 1

        def test_get_temp_file_path(self):

            path = self.project.get_temp_file_path(Document.MAIN)
            self.files.append(path)
            assert os.path.isfile(path)

            path = self.project.get_temp_file_path(Document.TRAN)
            self.files.append(path)
            assert os.path.isfile(path)

        def test_guess_video_file_path(self):

            self.project.guess_video_file_path()

    TestPreviewDelegate().run()
