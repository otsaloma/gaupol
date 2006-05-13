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

from gaupol.base.files          import SubtitleFile
from gaupol.base.timeframe.calc import TimeFrameCalculator
from gaupol.base.util           import listlib
from gaupol.constants           import Format, Mode


class SubViewer2(SubtitleFile):

    """SubViewer 2.0 file."""

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
        time = r'\d\d:\d\d:\d\d.\d\d'
        re_time_line = re.compile(r'^(%s),(%s)\s*$' % (time, time))

        shows  = []
        hides  = []
        texts  = []
        header = ''

        lines = self._read_lines()
        header_read = False

        for line in lines:
            if re_blank_line.match(line) is not None:
                continue
            match = re_time_line.match(line)
            if match is not None:
                header_read = True
                shows.append(match.group(1))
                hides.append(match.group(2))
                texts.append(u'')
            elif header_read:
                texts[-1] += line
            else:
                header += line

        # Remove leading and trailing spaces.
        if header:
            self.header = header.strip()
        texts = listlib.strip(texts)

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
        shows = shows[:]
        hides = hides[:]
        texts = texts[:]

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
            subtitle_file.write(self.header)
            subtitle_file.write(newline_character * 2)
            for i in range(len(shows)):
                subtitle_file.write('%s,%s' % (shows[i], hides[i]))
                subtitle_file.write(newline_character)
                subtitle_file.write(texts[i])
                subtitle_file.write(newline_character * 2)
        finally:
            subtitle_file.close()


if __name__ == '__main__':

    from gaupol.base.files.subrip import SubRip
    from gaupol.test              import Test

    class TestSubViewer2(Test):

        def test_all(self):

            path = self.get_subrip_path()
            subrip_file = SubRip(path, 'utf_8')
            data = subrip_file.read()

            subviewer_2_file = SubViewer2(path, 'utf_8', subrip_file.newlines)
            subviewer_2_file.write(*data)
            data_1 = subviewer_2_file.read()
            subviewer_2_file.write(*data_1)
            data_2 = subviewer_2_file.read()
            assert data_2 == data_1

    TestSubViewer2().run()
