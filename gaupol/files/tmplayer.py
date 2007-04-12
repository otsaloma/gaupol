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


"""TMPlayer file."""


from __future__ import with_statement

import codecs
import contextlib
import re

from gaupol import const, util
from gaupol.calculator import Calculator
from ._subfile import SubtitleFile


class TMPlayer(SubtitleFile):

    """TMPlayer file."""

    format = const.FORMAT.TMPLAYER
    has_header = False
    identifier = re.compile(r"^\d\d:\d\d:\d\d:.*$")
    mode = const.MODE.TIME

    def read(self):
        """Read file.

        Raise IOError if reading fails.
        Raise UnicodeError if decoding fails.
        Return show times, hide times, texts.
        """
        shows = []
        hides = []
        texts = []
        for line in self._read_lines():
            if len(line.strip()) >= 9:
                shows.append(line[:8] + ".000")
                texts.append(line[9:-1])

        calc = Calculator()
        for i in range(1, len(shows)):
            hides.append(shows[i])
        hides.append(calc.add_seconds_to_time(shows[-1], 3.000))
        texts = [x.replace("|", "\n") for x in texts]
        return shows, hides, texts

    @util.contractual
    def write(self, shows, hides, texts):
        """Write file.

        Raise IOError if writing fails.
        Raise UnicodeError if encoding fails.
        """
        calc = Calculator()
        shows = [calc.round_time(x, 0)[:8] + ":" for x in shows]
        texts = [x.replace("\n", "|") for x in texts]

        args = (self.path, "w", self.encoding)
        with contextlib.closing(codecs.open(*args)) as fobj:
            for i in range(len(shows)):
                fobj.write(shows[i])
                fobj.write(texts[i])
                fobj.write(self.newline.value)
