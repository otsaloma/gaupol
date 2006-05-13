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


"""Sub Station Alpha file."""


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


class SubStationAlpha(SubtitleFile):

    """Sub Station Alpha file."""

    FORMAT     = Format.SSA
    HAS_HEADER = True
    MODE       = Mode.TIME

    id_pattern = r'^ScriptType: v4.00\s*$', None

    HEADER_TEMPLATE = \
'''[Script Info]
Title:
Original Script:
Original Translation:
Original Editing:
Original Timing:
Synch Point:
Script Updated By:
Update Details:
ScriptType: v4.00
Collisions: Normal
PlayResY:
PlayResX:
PlayDepth:
Timer: 100.0000

[V4 Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, TertiaryColour, BackColour, Bold, Italic, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, AlphaLevel, Encoding
Style: Default,Arial,18,&Hffffff,&H00ffff,&H000000,&H000000,0,0,1,2,2,2,30,30,10,0,0'''

    def read(self):
        """
        Read Sub Station Alpha file.

        Raise IOError if reading fails.
        Raise UnicodeError if decoding fails.
        Return show times, hide times, texts.
        """
        # Compile regular expressions.
        re_comma = re.compile(r',\s*')

        shows  = []
        hides  = []
        texts  = []
        header = ''

        # Indexes of data on dialog lines.
        show_index = None
        hide_index = None
        text_index = None

        # Amount of dialog fields minus one.
        max_split = None

        lines = self._read_lines()
        header_read = False

        for line in lines:

            if header_read and line.startswith('Dialogue:'):
                line = line.replace('Dialogue:', '').strip()
                fields = re_comma.split(line, max_split)
                shows.append(fields[show_index])
                hides.append(fields[hide_index])
                texts.append(fields[text_index])

            elif line.startswith('[Events]'):
                header_read = True

            elif header_read and line.startswith('Format:'):
                line = line.replace('Format:', '').strip()
                fields = re_comma.split(line)
                show_index = fields.index('Start')
                hide_index = fields.index('End')
                text_index = fields.index('Text')
                max_split  = len(fields) - 1

            elif not header_read:
                header += line

        # Remove leading and trailing spaces.
        if header:
            self.header = header.strip()
        texts = listlib.strip(texts)

        # Replace decimal character and add zeros.
        shows = list('0' + time.replace('.', ',') + '0' for time in shows)
        hides = list('0' + time.replace('.', ',') + '0' for time in hides)

        # Replace \ns and \Ns with newlines.
        texts = list(text.replace('\\n', '\n') for text in texts)
        texts = list(text.replace('\\N', '\n') for text in texts)

        return shows, hides, texts

    def write(self, shows, hides, texts):
        """
        Write Sub Station Alpha file.

        Raise IOError if writing fails.
        Raise UnicodeError if encoding fails.
        """
        shows = shows[:]
        hides = hides[:]
        texts = texts[:]

        newline_character = self._get_newline_character()
        calc = TimeFrameCalculator()

        # Replace Python internal newline characters in text with \ns.
        texts = list(text.replace('\n', '\\n') for text in texts)

        # Round times to centiseconds.
        shows = list(calc.round_time(time, 2) for time in shows)
        hides = list(calc.round_time(time, 2) for time in hides)

        # Replace decimal character and remove extra digits.
        shows = list(time[1:11].replace(',', '.') for time in shows)
        hides = list(time[1:11].replace(',', '.') for time in hides)

        subtitle_file = codecs.open(self.path, 'w', self.encoding)

        try:
            subtitle_file.write(self.header)
            subtitle_file.write(newline_character * 2)
            subtitle_file.write('[Events]')
            subtitle_file.write(newline_character)
            subtitle_file.write('Format: Marked, Start, End, Style, Name, ')
            subtitle_file.write('MarginL, MarginR, MarginV, Effect, Text')
            subtitle_file.write(newline_character)
            for i in range(len(shows)):
                subtitle_file.write(
                    'Dialogue: 0,%s,%s,Default,,0000,0000,0000,,%s%s' % \
                    (shows[i], hides[i], texts[i], newline_character)
                )
        finally:
            subtitle_file.close()


if __name__ == '__main__':

    from gaupol.base.files.subrip import SubRip
    from gaupol.test              import Test

    class TestSubStationAlpha(Test):

        def test_all(self):

            path = self.get_subrip_path()
            subrip_file = SubRip(path, 'utf_8')
            data = subrip_file.read()

            ssa_file = SubStationAlpha(path, 'utf_8', subrip_file.newlines)
            ssa_file.write(*data)
            data_1 = ssa_file.read()
            ssa_file.write(*data_1)
            data_2 = ssa_file.read()
            assert data_2 == data_1

    TestSubStationAlpha().run()
