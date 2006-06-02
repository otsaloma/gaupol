# Copyright (C) 2005-2006 Osmo Salomaa
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

from gaupol.base               import cons
from gaupol.base.file          import SubtitleFile
from gaupol.base.position.calc import Calculator


class MPL2(SubtitleFile):

    """MPL2 file."""

    format     = cons.Format.MPL2
    mode       = cons.Mode.TIME
    has_header = False
    identifier = r'^\[\d+\]\[\d+\].*?$', 0

    def read(self):
        """
        Read MPL2 file.

        Raise IOError if reading fails.
        Raise UnicodeError if decoding fails.
        Return show times, hide times, texts.
        """
        re_line = re.compile(r'^\[(\d+)\]\[(\d+)\](.*?)$')
        calc = Calculator()

        shows = []
        hides = []
        texts = []
        lines = self._read_lines()
        for line in lines:
            match = re_line.match(line)
            if match is not None:
                shows.append(match.group(1))
                hides.append(match.group(2))
                texts.append(match.group(3))

        for data in (shows, hides):
            for i, value in enumerate(data):
                seconds = float(value[:-1] + '.' + value[-1])
                data[i] = calc.seconds_to_time(seconds)
        texts = list(x.replace('|', '\n') for x in texts)

        return shows, hides, texts

    def write(self, shows, hides, texts):
        """
        Write MPL2 file.

        Raise IOError if writing fails.
        Raise UnicodeError if encoding fails.
        """
        shows = shows[:]
        hides = hides[:]
        texts = texts[:]
        newline_char = self._get_newline_character()
        calc = Calculator()

        for data in (shows, hides):
            for i in range(len(data)):
                decaseconds = calc.time_to_seconds(data[i]) * 10
                data[i] = '%.0f' % decaseconds
        texts = list(x.replace('\n', '|') for x in texts)

        fobj = codecs.open(self.path, 'w', self.encoding)
        try:
            for i in range(len(shows)):
                fobj.write('[%s][%s]%s%s' % (
                    shows[i], hides[i], texts[i], newline_char))
        finally:
            fobj.close()
