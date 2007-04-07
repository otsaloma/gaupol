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


"""SubRip file."""


from __future__ import with_statement

import codecs
import contextlib
import re

from gaupol import const, util
from ._subfile import SubtitleFile


class SubRip(SubtitleFile):

    """SubRip file."""

    format = const.FORMAT.SUBRIP
    has_header = False
    identifier = r"^\d\d:\d\d:\d\d,\d\d\d --> \d\d:\d\d:\d\d,\d\d\d\s*$", 0
    mode = const.MODE.TIME

    def _clean_lines(self, all_lines, re_time_line):
        """Return lines without unit numbers and preceding blank lines."""

        lines = ["\n"]
        for line in all_lines:
            if re_time_line.match(line) is not None:
                lines[-1] = line
                if not lines[-2].strip():
                    lines.pop(-2)
                continue
            lines.append(line)
        return lines

    def _read_components(self, lines, re_time_line):
        """Read and return shows, hides and texts."""

        shows = []
        hides = []
        texts = []
        for line in lines:
            match = re_time_line.match(line)
            if match is not None:
                shows.append(match.group(1).replace(",", "."))
                hides.append(match.group(2).replace(",", "."))
                texts.append("")
                continue
            texts[-1] += line
        re_trailer = re.compile(r"\n\Z", re.MULTILINE)
        texts = [re_trailer.sub("", x) for x in texts]
        return shows, hides, texts

    def read(self):
        """Read file.

        Raise IOError if reading fails.
        Raise UnicodeError if decoding fails.
        Return show times, hide times, texts.
        """
        time = r"\d\d:\d\d:\d\d,\d\d\d"
        re_time_line = re.compile(r"^(%s) --> (%s)\s*$" % (time, time))
        lines = self._read_lines()
        lines = self._clean_lines(lines, re_time_line)
        return self._read_components(lines, re_time_line)

    @util.contractual
    def write(self, shows, hides, texts):
        """Write file.

        Raise IOError if writing fails.
        Raise UnicodeError if encoding fails.
        """
        shows = [x.replace(".", ",") for x in shows]
        hides = [x.replace(".", ",") for x in hides]
        texts = [x.replace("\n", self.newline.value) for x in texts]

        args = (self.path, "w", self.encoding)
        with contextlib.closing(codecs.open(*args)) as fobj:
            for i in range(len(shows)):
                fobj.write(str(i + 1))
                fobj.write(self.newline.value)
                fobj.write(shows[i])
                fobj.write(" --> ")
                fobj.write(hides[i])
                fobj.write(self.newline.value)
                fobj.write(texts[i])
                fobj.write(self.newline.value)
                fobj.write(self.newline.value)
