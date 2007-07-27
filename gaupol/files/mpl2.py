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

"""MPL2 file."""

from __future__ import with_statement

import codecs
import contextlib
import gaupol
import re

from .subfile import SubtitleFile


class MPL2(SubtitleFile):

    """MPL2 file."""

    __metaclass__ = gaupol.Contractual
    format = gaupol.FORMAT.MPL2
    mode = gaupol.MODE.TIME

    def read(self):
        """Read file.

        Raise IOError if reading fails.
        Raise UnicodeError if decoding fails.
        Return start times, end times, texts.
        """
        starts = []
        ends = []
        texts = []
        calc = gaupol.Calculator()
        re_line = re.compile(r"^\[(-?\d+)\]\[(-?\d+)\](.*?)$")
        for line in self._read_lines():
            match = re_line.match(line)
            if match is not None:
                starts.append(match.group(1))
                ends.append(match.group(2))
                texts.append(match.group(3))

        for times in (starts, ends):
            for i, time in enumerate(times):
                seconds = float("%s.%s" % (time[:-1], time[-1]))
                times[i] = calc.seconds_to_time(seconds)
        texts = [x.replace("|", "\n") for x in texts]
        return starts, ends, texts

    def write(self, starts, ends, texts):
        """Write file.

        Raise IOError if writing fails.
        Raise UnicodeError if encoding fails.
        """
        calc = gaupol.Calculator()
        get_deca = lambda x: "%.0f" % (calc.time_to_seconds(x) * 10)
        starts = [get_deca(x) for x in starts]
        ends = [get_deca(x) for x in ends]
        texts = [x.replace("\n", "|") for x in texts]

        args = (self.path, "w", self.encoding)
        with contextlib.closing(codecs.open(*args)) as fobj:
            for i in range(len(starts)):
                fobj.write("[%s]" % starts[i])
                fobj.write("[%s]" % ends[i])
                fobj.write(texts[i])
                fobj.write(self.newline.value)
