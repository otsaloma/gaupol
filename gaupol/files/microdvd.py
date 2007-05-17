# Copyright (C) 2005-2007 Osmo Salomaa
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


"""MicroDVD file."""


from __future__ import with_statement

import codecs
import contextlib
import re

from gaupol import const
from gaupol.base import Contractual
from .subfile import SubtitleFile


class MicroDVD(SubtitleFile):

    """MicroDVD file."""

    __metaclass__ = Contractual
    format = const.FORMAT.MICRODVD
    mode = const.MODE.FRAME

    def read(self):
        """Read file.

        Raise IOError if reading fails.
        Raise UnicodeError if decoding fails.
        Return start frames, end frames, texts.
        """
        starts = []
        ends = []
        texts = []
        re_line = re.compile(r"^\{(\d+)\}\{(\d+)\}(.*?)$")
        for line in self._read_lines():
            match = re_line.match(line)
            if match is not None:
                starts.append(match.group(1))
                ends.append(match.group(2))
                texts.append(match.group(3))
            elif line.startswith("{DEFAULT}"):
                self.header = line[:-1]

        starts = [int(x) for x in starts]
        ends = [int(x) for x in ends]
        texts = [x.replace("|", "\n") for x in texts]
        return starts, ends, texts

    def write(self, starts, ends, texts):
        """Write file.

        Raise IOError if writing fails.
        Raise UnicodeError if encoding fails.
        """
        texts = [x.replace("\n", "|") for x in texts]
        args = (self.path, "w", self.encoding)
        with contextlib.closing(codecs.open(*args)) as fobj:
            if self.header:
                fobj.write(self.header)
                fobj.write(self.newline.value)
            for i in range(len(starts)):
                fobj.write("{%d}" % starts[i])
                fobj.write("{%d}" % ends[i])
                fobj.write(texts[i])
                fobj.write(self.newline.value)
