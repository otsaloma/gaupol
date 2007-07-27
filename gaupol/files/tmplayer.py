# Copyright (C) 2006-2007 Osmo Salomaa
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

"""TMPlayer file."""

from __future__ import with_statement

import codecs
import contextlib
import gaupol
import re

from .subfile import SubtitleFile


class TMPlayer(SubtitleFile):

    """TMPlayer file."""

    __metaclass__ = gaupol.Contractual
    format = gaupol.FORMAT.TMPLAYER
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
        for line in self._read_lines():
            z = (10 if line.startswith("-") else 9)
            if len(line.strip()) >= z:
                starts.append(line[:z - 1] + ".000")
                texts.append(line[z:-1])

        calc = gaupol.Calculator()
        for i in range(1, len(starts)):
            ends.append(starts[i])
        ends.append(calc.add_seconds_to_time(starts[-1], 3.000))
        texts = [x.replace("|", "\n") for x in texts]
        return starts, ends, texts

    def write(self, starts, ends, texts):
        """Write file.

        Raise IOError if writing fails.
        Raise UnicodeError if encoding fails.
        """
        calc = gaupol.Calculator()
        starts = [calc.round_time(x, 0) for x in starts]
        re_milliseconds = re.compile("\.\d\d\d$")
        starts = [re_milliseconds.sub(r":", x) for x in starts]
        texts = [x.replace("\n", "|") for x in texts]

        args = (self.path, "w", self.encoding)
        with contextlib.closing(codecs.open(*args)) as fobj:
            for i in range(len(starts)):
                fobj.write(starts[i])
                fobj.write(texts[i])
                fobj.write(self.newline.value)
