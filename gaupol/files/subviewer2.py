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

"""SubViewer 2.0 file."""

from __future__ import with_statement

import codecs
import contextlib
import gaupol
import re

from .subfile import SubtitleFile


class SubViewer2(SubtitleFile):

    """SubViewer 2.0 file."""

    __metaclass__ = gaupol.Contractual
    format = gaupol.FORMAT.SUBVIEWER2
    mode = gaupol.MODE.TIME

    def _read_components(self, lines):
        """Read and return starts, ends and texts."""

        starts = []
        ends = []
        texts = []
        time = r"-?\d\d:\d\d:\d\d.\d\d"
        re_time_line = re.compile(r"^(%s),(%s)\s*$" % (time, time))
        re_trailer = re.compile(r"\n\Z", re.MULTILINE)
        for i, line in enumerate(lines + [""]):
            match = re_time_line.match(line)
            if match is not None:
                starts.append(match.group(1))
                ends.append(match.group(2))
                texts.append(re_trailer.sub("", lines[i + 1]))

        starts = [x + "0" for x in starts]
        ends = [x + "0" for x in ends]
        texts = [x.replace("[br]", "\n") for x in texts]
        return starts, ends, texts

    def _read_header(self, lines):
        """Read header and return leftover lines."""

        header = ""
        lines = lines[:]
        while lines[0].startswith("["):
            header += lines.pop(0)
        if header.endswith("\n"):
            header = header[:-1]
        self.header = header
        return lines

    def read(self):
        """Read file.

        Raise IOError if reading fails.
        Raise UnicodeError if decoding fails.
        Return start times, end times, texts.
        """
        lines = self._read_lines()
        lines = self._read_header(lines)
        return self._read_components(lines)

    def write(self, starts, ends, texts):
        """Write file.

        Raise IOError if writing fails.
        Raise UnicodeError if encoding fails.
        """
        calc = gaupol.Calculator()
        starts = [calc.round_time(x, 2) for x in starts]
        ends = [calc.round_time(x, 2) for x in ends]
        re_last_digit = re.compile(r"\d$")
        starts = [re_last_digit.sub("", x) for x in starts]
        ends = [re_last_digit.sub("", x) for x in ends]
        texts = [x.replace("\n", "[br]") for x in texts]

        args = (self.path, "w", self.encoding)
        with contextlib.closing(codecs.open(*args)) as fobj:
            fobj.write(self.header)
            fobj.write(self.newline.value)
            fobj.write(self.newline.value)
            for i in range(len(starts)):
                fobj.write(starts[i])
                fobj.write(",")
                fobj.write(ends[i])
                fobj.write(self.newline.value)
                fobj.write(texts[i])
                fobj.write(self.newline.value)
                fobj.write(self.newline.value)
