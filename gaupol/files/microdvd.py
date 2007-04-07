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

from gaupol import const, util
from ._subfile import SubtitleFile


class MicroDVD(SubtitleFile):

    """MicroDVD file."""

    format = const.FORMAT.MICRODVD
    has_header = True
    identifier = r"^\{\d+\}\{\d+\}.*?$", 0
    mode = const.MODE.FRAME

    def read(self):
        """Read file.

        Raise IOError if reading fails.
        Raise UnicodeError if decoding fails.
        Return show frames, hide frames, texts.
        """
        shows = []
        hides = []
        texts = []
        re_line = re.compile(r"^\{(\d+)\}\{(\d+)\}(.*?)$")
        for line in self._read_lines():
            match = re_line.match(line)
            if match is not None:
                shows.append(match.group(1))
                hides.append(match.group(2))
                texts.append(match.group(3))
            elif line.startswith("{DEFAULT}"):
                self.header = line[:-1]

        shows = [int(x) for x in shows]
        hides = [int(x) for x in hides]
        texts = [x.replace("|", "\n") for x in texts]
        return shows, hides, texts

    @util.contractual
    def write(self, shows, hides, texts):
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
            for i in range(len(shows)):
                fobj.write("{%d}" % shows[i])
                fobj.write("{%d}" % hides[i])
                fobj.write(texts[i])
                fobj.write(self.newline.value)
