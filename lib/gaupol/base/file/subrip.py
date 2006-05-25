# Copyright (C) 2005-2006 Osmo Salomaa
#
# This file is part of Gaupol.
#
# Gaupol is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Gaupol is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Gaupol; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA


"""SubRip file."""


import codecs
import re

from gaupol.base.cons import Format, Mode
from gaupol.base.file import SubtitleFile
from gaupol.base.util import listlib


class SubRip(SubtitleFile):

    """SubRip file."""

    format     = Format.SUBRIP
    mode       = Mode.TIME
    has_header = False
    identifier = r'^\d\d:\d\d:\d\d,\d\d\d --> \d\d:\d\d:\d\d,\d\d\d\s*$', 0

    def read(self):
        """
        Read Subrip file.

        Raise IOError if reading fails.
        Raise UnicodeError if decoding fails.
        Return show times, hide times, texts.
        """
        time = r'\d\d:\d\d:\d\d,\d\d\d'
        re_time_line = re.compile(r'^(%s) --> (%s)\s*$' % (time, time))

        # Remove blank lines and unit numbers.
        all_lines = self._read_lines()
        lines = []
        for line in all_lines:
            if not line.strip():
                continue
            elif re_time_line.match(line) is not None:
                lines[-1] = line
            else:
                lines.append(line)

        shows = []
        hides = []
        texts = []
        for line in lines:
            match = re_time_line.match(line)
            if match is not None:
                shows.append(match.group(1))
                hides.append(match.group(2))
                texts.append(u'')
            else:
                texts[-1] += line
        texts = listlib.strip(texts)

        return shows, hides, texts

    def write(self, shows, hides, texts):
        """
        Write SubRip file.

        Raise IOError if writing fails.
        Raise UnicodeError if encoding fails.
        """
        texts = texts[:]
        newline_char = self._get_newline_character()
        texts = list(text.replace('\n', newline_char) for text in texts)

        fobj = codecs.open(self.path, 'w', self.encoding)
        try:
            for i in range(len(shows)):
                fobj.write('%.0f%s%s --> %s%s%s%s%s' % (
                    i + 1, newline_char,
                    shows[i], hides[i], newline_char,
                    texts[i], newline_char, newline_char
                ))
        finally:
            fobj.close()
