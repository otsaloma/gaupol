# Copyright (C) 2006-2007 Osmo Salomaa
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


"""MPsub file."""


from __future__ import with_statement

import codecs
import contextlib
import gaupol
import re

from .subfile import SubtitleFile


class MPsub(SubtitleFile):

    """MPsub file.

    Instance variables framerate and mode depend on what is written on the
    first line of the file header. They will be determined when the file is
    read and can later be changed with the 'set_header' method.
    """

    __metaclass__ = gaupol.Contractual
    format = gaupol.FORMAT.MPSUB
    mode = gaupol.MODE.TIME

    def __init__(self, path, encoding, newline=None):

        SubtitleFile.__init__(self, path, encoding, newline)
        self.framerate = None
        self.mode = gaupol.MODE.TIME

    def _clean_lines(self, all_lines, re_time_line):
        """Return lines without blank lines preceding time lines."""

        lines = ["\n"]
        for line in all_lines:
            if re_time_line.match(line) is not None:
                if not lines[-1].strip():
                    lines[-1] = line
                    continue
            lines.append(line)
        while lines[0] == "\n":
            lines.pop(0)
        return lines

    def _get_mpsub_frames(self, starts, ends):
        """Get MPsub style starts and ends as frames."""

        starts = starts[:]
        ends = ends[:]
        for i in reversed(range(1, len(starts))):
            ends[i] = str(ends[i] - starts[i])
            starts[i] = str(starts[i] - ends[i - 1])
        ends[0] = str(ends[0] - starts[0])
        return starts, ends

    def _get_mpsub_times(self, starts, ends):
        """Get MPsub style starts and ends as times."""

        calc = gaupol.Calculator()
        starts = [calc.time_to_seconds(x) for x in starts]
        ends = [calc.time_to_seconds(x) for x in ends]
        for i in reversed(range(1, len(starts))):
            ends[i] -= starts[i]
            starts[i] -= ends[i - 1]
        ends[0] -= starts[0]

        deviation = 0
        # Round times and avoid cumulation of rounding errors.
        for i in range(len(starts)):
            orig_show = starts[i]
            starts[i] = round(starts[i] - deviation, 2)
            deviation = deviation + starts[i] - orig_show
            orig_hide = ends[i]
            ends[i] = round(ends[i] - deviation, 2)
            deviation = deviation + ends[i] - orig_hide

        starts = ["%.2f" % x for x in starts]
        ends = ["%.2f" % x for x in ends]
        return starts, ends

    def _read_components(self, lines, re_time_line):
        """Read and return starts, ends and texts."""

        starts = []
        ends = []
        texts = []
        for line in lines:
            match = re_time_line.match(line)
            if match is not None:
                start = float(match.group(1))
                start = (start + ends[-1] if ends else start)
                starts.append(start)
                ends.append(starts[-1] + float(match.group(2)))
                texts.append(u"")
            elif texts:
                texts[-1] += line

        calc = gaupol.Calculator()
        if self.mode == gaupol.MODE.TIME:
            starts = [calc.seconds_to_time(x) for x in starts]
            ends = [calc.seconds_to_time(x) for x in ends]
        elif self.mode == gaupol.MODE.FRAME:
            starts = [int(round(x, 0)) for x in starts]
            ends = [int(round(x, 0)) for x in ends]
        re_trailer = re.compile(r"\n\Z", re.MULTILINE)
        texts = [re_trailer.sub("", x) for x in texts]
        return starts, ends, texts

    def _read_header(self, lines, re_time_line):
        """Read header and return leftover lines."""

        header = ""
        lines = lines[:]
        while re_time_line.match(lines[0]) is None:
            header += lines.pop(0)
        if header.endswith("\n"):
            header = header[:-1]
        self.header = header
        return lines

    def copy_from(self, file):
        """Copy generic properties from file of same format."""

        SubtitleFile.copy_from(self, file)
        self.mode = file.mode
        self.framerate = file.framerate

    def read(self):
        """Read file.

        Raise IOError if reading fails.
        Raise UnicodeError if decoding fails.
        Raise ValueError if bad FORMAT line.
        Return starts, ends, texts.
        """
        lines = self._read_lines()
        re_time_line = re.compile(r"^([\d\.]+) ([\d\.]+)\s*$")
        lines = self._clean_lines(lines, re_time_line)
        lines = self._read_header(lines, re_time_line)
        return self._read_components(lines, re_time_line)

    def set_header(self, header):
        """Parse and set header, mode and framerate.

        Raise ValueError if bad FORMAT line.
        """
        mode = None
        for line in header.split("\n"):
            if line.startswith("FORMAT="):
                mode = line[7:].strip()
        if not mode in (gaupol.FRAMERATE.mpsubs + ["TIME"]):
            raise ValueError

        self.header = header
        self.mode = gaupol.MODE.TIME
        self.framerate = None
        if mode in gaupol.FRAMERATE.mpsubs:
            self.mode = gaupol.MODE.FRAME
            index = gaupol.FRAMERATE.mpsubs.index(mode)
            self.framerate = gaupol.FRAMERATE.members[index]

    def write(self, starts, ends, texts):
        """Write file.

        Raise IOError if writing fails.
        Raise UnicodeError if encoding fails.
        """
        method = (self._get_mpsub_times, self._get_mpsub_frames)[self.mode]
        starts, ends = method(starts, ends)
        texts = [x.replace("\n", self.newline.value) for x in texts]

        args = (self.path, "w", self.encoding)
        with contextlib.closing(codecs.open(*args)) as fobj:
            fobj.write(self.header)
            fobj.write(self.newline.value)
            fobj.write(self.newline.value)
            for i in range(len(starts)):
                fobj.write(starts[i])
                fobj.write(" ")
                fobj.write(ends[i])
                fobj.write(self.newline.value)
                fobj.write(texts[i])
                fobj.write(self.newline.value)
                fobj.write(self.newline.value)
