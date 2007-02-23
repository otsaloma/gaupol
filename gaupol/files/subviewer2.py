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


"""SubViewer 2.0 file."""


import codecs
import re

from gaupol import cons
from gaupol.calculator import Calculator
from ._subfile import SubtitleFile


class SubViewer2(SubtitleFile):

    """SubViewer 2.0 file."""

    format = cons.FORMAT.SUBVIEWER2
    has_header = True
    identifier = r"^\d\d:\d\d:\d\d.\d\d,\d\d:\d\d:\d\d.\d\d\s*$", 0
    mode = cons.MODE.TIME

    def _read_components(self, lines):
        """Read and return shows, hides and texts."""

        time = r"\d\d:\d\d:\d\d.\d\d"
        re_time_line = re.compile(r"^(%s),(%s)\s*$" % (time, time))

        shows = []
        hides = []
        texts = []
        lines.append(u"")
        for i, line in enumerate(lines):
            match = re_time_line.match(line)
            if match is not None:
                shows.append(match.group(1))
                hides.append(match.group(2))
                texts.append(lines[i + 1][:-1])

        shows = list(x + "0" for x in shows)
        hides = list(x + "0" for x in hides)
        texts = list(x.replace("[br]", "\n") for x in texts)
        return shows, hides, texts

    def _read_header(self, lines):
        """Read header and return leftover lines."""

        header = ""
        while lines[0].startswith("["):
            header += lines.pop(0)
        self.header = header[:-1]
        return lines

    def read(self):
        """Read file.

        Raise IOError if reading fails.
        Raise UnicodeError if decoding fails.
        Return show times, hide times, texts.
        """
        lines = self._read_lines()
        lines = self._read_header(lines)
        return self._read_components(lines)

    def write(self, shows, hides, texts):
        """Write file.

        Raise IOError if writing fails.
        Raise UnicodeError if encoding fails.
        """
        calc = Calculator()
        shows = list(calc.round_time(x, 2)[:11] for x in shows)
        hides = list(calc.round_time(x, 2)[:11] for x in hides)
        texts = list(x.replace("\n", "[br]") for x in texts)

        fobj = codecs.open(self.path, "w", self.encoding)
        try:
            fobj.write(self.header + self.newline.value * 2)
            for i in range(len(shows)):
                fobj.write("%s,%s%s%s%s%s" % (
                    shows[i], hides[i], self.newline.value,
                    texts[i], self.newline.value, self.newline.value))
        finally:
            fobj.close()
