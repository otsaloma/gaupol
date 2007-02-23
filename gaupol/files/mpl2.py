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


import codecs
import re

from gaupol import cons
from gaupol.calculator import Calculator
from ._subfile import SubtitleFile


class MPL2(SubtitleFile):

    """MPL2 file."""

    format = cons.FORMAT.MPL2
    has_header = False
    identifier = r"^\[\d+\]\[\d+\].*?$", 0
    mode = cons.MODE.TIME

    def read(self):
        """Read file.

        Raise IOError if reading fails.
        Raise UnicodeError if decoding fails.
        Return show times, hide times, texts.
        """
        re_line = re.compile(r"^\[(\d+)\]\[(\d+)\](.*?)$")
        calc = Calculator()

        shows = []
        hides = []
        texts = []
        for line in self._read_lines():
            match = re_line.match(line)
            if match is not None:
                shows.append(match.group(1))
                hides.append(match.group(2))
                texts.append(match.group(3))

        for seq in (shows, hides):
            for i, value in enumerate(seq):
                seconds = float(value[:-1] + "." + value[-1])
                seq[i] = calc.seconds_to_time(seconds)
        texts = list(x.replace("|", "\n") for x in texts)
        return shows, hides, texts

    def write(self, shows, hides, texts):
        """Write file.

        Raise IOError if writing fails.
        Raise UnicodeError if encoding fails.
        """
        calc = Calculator()
        def get_deca(time):
            return "%.0f" % (calc.time_to_seconds(time) * 10)
        shows = list(get_deca(x) for x in shows)
        hides = list(get_deca(x) for x in hides)
        texts = list(x.replace("\n", "|") for x in texts)

        fobj = codecs.open(self.path, "w", self.encoding)
        try:
            for i in range(len(shows)):
                fobj.write("[%s][%s]%s%s" % (
                    shows[i], hides[i], texts[i], self.newline.value))
        finally:
            fobj.close()
