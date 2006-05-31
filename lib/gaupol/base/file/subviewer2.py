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


"""SubViewer 2.0 file."""


import codecs
import re

from gaupol.base.cons          import Format, Mode
from gaupol.base.file          import SubtitleFile
from gaupol.base.position.calc import TimeFrameCalculator


class SubViewer2(SubtitleFile):

    """SubViewer 2.0 file."""

    format     = Format.SUBVIEWER2
    mode       = Mode.TIME
    has_header = True
    identifier = r'^\d\d:\d\d:\d\d.\d\d,\d\d:\d\d:\d\d.\d\d\s*$', 0

    header_template = \
'''[INFORMATION]
[TITLE]
[AUTHOR]
[SOURCE]
[PRG]
[FILEPATH]
[DELAY]0
[CD TRACK]0
[COMMENT]
[END INFORMATION]
[SUBTITLE]
[COLF]&HFFFFFF,[STYLE]bd,[SIZE]18,[FONT]Arial'''

    def read(self):
        """
        Read SubViewer 2.0 file.

        Raise IOError if reading fails.
        Raise UnicodeError if decoding fails.
        Return show times, hide times, texts.
        """
        time = r'\d\d:\d\d:\d\d.\d\d'
        re_time_line = re.compile(r'^(%s),(%s)\s*$' % (time, time))

        shows  = []
        hides  = []
        texts  = []
        header = ''
        header_read = False
        lines = self._read_lines()
        for line in lines:
            if not line.strip():
                continue
            match = re_time_line.match(line)
            if match is not None:
                header_read = True
                shows.append(match.group(1))
                hides.append(match.group(2))
                texts.append(u'')
            elif header_read:
                texts[-1] += line.strip()
            else:
                header += line
        if header:
            self.header = header.strip()

        shows = list(x.replace('.', ',') + '0' for x in shows)
        hides = list(x.replace('.', ',') + '0' for x in hides)
        texts = list(x.replace('[br]', '\n')   for x in texts)

        return shows, hides, texts

    def write(self, shows, hides, texts):
        """
        Write SubViewer 2.0 file.

        Raise IOError if writing fails.
        Raise UnicodeError if encoding fails.
        """
        shows = shows[:]
        hides = hides[:]
        texts = texts[:]
        calc = TimeFrameCalculator()
        newline_char = self._get_newline_character()

        texts = list(x.replace('\n', '[br]')  for x in texts)
        shows = list(calc.round_time(x, 2)    for x in shows)
        hides = list(calc.round_time(x, 2)    for x in hides)
        shows = list(x[:11].replace(',', '.') for x in shows)
        hides = list(x[:11].replace(',', '.') for x in hides)

        fobj = codecs.open(self.path, 'w', self.encoding)
        try:
            fobj.write(self.header + newline_char * 2)
            for i in range(len(shows)):
                fobj.write('%s,%s%s%s%s%s' % (
                    shows[i], hides[i], newline_char,
                    texts[i], newline_char,
                    newline_char
                ))
        finally:
            fobj.close()
