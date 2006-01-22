# Copyright (C) 2005 Osmo Salomaa
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


"""SubViewer 2.0 file."""


try:
    from psyco.classes import *
except ImportError:
    pass

import codecs
import re

from gaupol.base.files       import SubtitleFile
from gaupol.base.timing.calc import TimeFrameCalculator
from gaupol.base.util        import listlib
from gaupol.constants        import Format, Mode


class SubViewer2(SubtitleFile):

    """
    SubViewer 2.0 file.

    SubViewer 2.0 format quick reference:
    [INFORMATION]
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
    [COLF]&HFFFFFF,[STYLE]bd,[SIZE]18,[FONT]Arial
    00:00:00.00,00:00:03.38
    And that completes my final report[br]until we reach touchdown.

    00:00:03.68,00:00:05.61
    We're now on full automatic,[br]in the hands of the computers.
    """

    FORMAT     = Format.SUBVIEWER2
    HAS_HEADER = True
    MODE       = Mode.TIME

    id_pattern = r'^\d\d:\d\d:\d\d.\d\d,\d\d:\d\d:\d\d.\d\d\s*$', None

    HEADER_TEMPLATE = \
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
        # Compile regular expressions.
        re_blank_line = re.compile(r'^\s*$')
        re_header = re.compile(r'^\[[A-Z ]+\]')
        time = r'\d\d:\d\d:\d\d.\d\d'
        re_time_line = re.compile(r'^(%s),(%s)\s*$' % (time, time))

        shows  = []
        hides  = []
        texts  = []

        lines = self._read_lines()
        header_read = False

        for line in lines:

            if re_blank_line.match(line) is not None:
                continue

            # Read header.
            if not header_read:
                if re_header.search(line) is not None:
                    self.header += line
                    continue

            # Read subtitles.
            match = re_time_line.match(line)
            if match is not None:
                header_read = True
                shows.append(match.group(1))
                hides.append(match.group(2))
                texts.append(u'')
            else:
                texts[-1] += line

        # Remove leading and trailing spaces.
        self.header = self.header.strip()
        listlib.strip_spaces(texts)

        # Replace decimal character and add milliseconds.
        shows = list(time.replace('.', ',') + '0' for time in shows)
        hides = list(time.replace('.', ',') + '0' for time in hides)

        # Replace [br]s with newlines.
        texts = list(text.replace('[br]', '\n') for text in texts)

        return shows, hides, texts

    def write(self, shows, hides, texts):
        """
        Write SubViewer 2.0 file.

        Raise IOError if writing fails.
        Raise UnicodeError if encoding fails.
        """
        newline_character = self._get_newline_character()
        calc = TimeFrameCalculator()

        # Replace Python internal newline characters in text with [br]s.
        texts = list(text.replace('\n', '[br]') for text in texts)

        # Round times to centiseconds.
        shows = list(calc.round_time(time, 2) for time in shows)
        hides = list(calc.round_time(time, 2) for time in hides)

        # Replace decimal character and remove milliseconds.
        shows = list(time[:11].replace(',', '.') for time in shows)
        hides = list(time[:11].replace(',', '.') for time in hides)

        subtitle_file = codecs.open(self.path, 'w', self.encoding)

        try:
            if self.header:
                subtitle_file.write(self.header + newline_character)
            for i in range(len(shows)):
                subtitle_file.write('%s,%s' % (shows[i], hides[i]))
                subtitle_file.write(newline_character)
                subtitle_file.write(texts[i])
                subtitle_file.write(newline_character * 2)
        finally:
            subtitle_file.close()
