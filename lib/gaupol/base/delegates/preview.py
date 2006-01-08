# Copyright (C) 2005 Osmo Salomaa
#
# This file is part of Gaupol.
#
# Gaupol is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Gaupol is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Gaupol; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA


"""Previewing subtitles with video player."""


try:
    from psyco.classes import *
except ImportError:
    pass

import os

from gaupol.base.colconstants import *
from gaupol.base.delegates    import Delegate
from gaupol.base.error        import ExternalError


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

    def preview(self, row, document, command, offset,
                extensions=default_extensions):
        """
        Preview subtitles with video player.

        command: string, where %t = time, %f = frame and %s = seconds
        offset: float-convertable, seconds before row's show time to start
        extensions: list of acceptable video file extensions

        Video file must exist in the same directory as the subtitle file.
        Subtitle file's filename without extension must start with or match
        video file's filename without extension. Full video filepath is
        appended to command inside double-quotes.

        Raise IOError if a video file is not found.
        Raise ExternalError with output as argument if command fails.
        """
        subfile = (self.main_file, self.tran_file)[document]
        assert subfile is not None

        # Get offsetted time.
        time    = self.times[row][SHOW]
        seconds = self.calc.time_to_seconds(time)
        seconds = max(0.0, seconds - float(offset))

        # Get time strings.
        time    = str(self.calc.seconds_to_time(seconds))
        frame   = str(self.calc.seconds_to_frame(seconds))
        seconds = str(seconds)

        # Replace times in command.
        command = command.replace('%t', time   )
        command = command.replace('%f', frame  )
        command = command.replace('%s', seconds)

        # Get paths.
        subroot   = os.path.splitext(subfile.path)[0]
        dirname   = os.path.dirname(subfile.path)
        filenames = os.listdir(dirname)

        # Find video.
        for filename in filenames:

            # Subtitle filename must start with video filename.
            filepath = os.path.join(dirname, filename)
            fileroot, extension = os.path.splitext(filepath)
            if not subroot.startswith(fileroot):
                continue

            # File must be a video file.
            if not extension in extensions:
                continue

            command += ' "%s"' % filepath

            # Get all output on UNIX.
            # TODO: How do we get the *error* output on non-unices?
            try:
                import commands
                return_value, output = commands.getstatusoutput(command)
            except ImportError:
                fobj = os.popen(command)
                output = fobj.read()
                return_value = fobj.close()

            if return_value in (0, None):
                return

            raise ExternalError(output)

        raise IOError
