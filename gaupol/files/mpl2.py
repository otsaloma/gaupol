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


"""MPL2 file."""


from __future__ import with_statement

import codecs
import contextlib
import re

from gaupol import const, util
from gaupol.calculator import Calculator
from ._subfile import SubtitleFile


class MPL2(SubtitleFile):

    """MPL2 file."""

    format = const.FORMAT.MPL2
    has_header = False
    identifier = re.compile(r"^\[\d+\]\[\d+\].*?$")
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
        calc = Calculator()
        re_line = re.compile(r"^\[(\d+)\]\[(\d+)\](.*?)$")
        for line in self._read_lines():
            match = re_line.match(line)
            if match is not None:
                shows.append(match.group(1))
                hides.append(match.group(2))
                texts.append(match.group(3))

        for times in (shows, hides):
            for i, time in enumerate(times):
                seconds = float("%s.%s" % (time[:-1], time[-1]))
                times[i] = calc.seconds_to_time(seconds)
        texts = [x.replace("|", "\n") for x in texts]
        return shows, hides, texts

    @util.contractual
    def write(self, shows, hides, texts):
        """Write file.

        Raise IOError if writing fails.
        Raise UnicodeError if encoding fails.
        """
        calc = Calculator()
        def get_deca(time):
            return "%.0f" % (calc.time_to_seconds(time) * 10)
        shows = [get_deca(x) for x in shows]
        hides = [get_deca(x) for x in hides]
        texts = [x.replace("\n", "|") for x in texts]

        args = (self.path, "w", self.encoding)
        with contextlib.closing(codecs.open(*args)) as fobj:
            for i in range(len(shows)):
                fobj.write("[%s]" % shows[i])
                fobj.write("[%s]" % hides[i])
                fobj.write(texts[i])
                fobj.write(self.newline.value)
