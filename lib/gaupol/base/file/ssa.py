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


"""Sub Station Alpha file."""


import codecs
import re

from gaupol.base               import cons
from gaupol.base.file          import SubtitleFile
from gaupol.base.position.calc import TimeFrameCalculator


class SubStationAlpha(SubtitleFile):

    """Sub Station Alpha file."""

    format     = cons.Format.SSA
    mode       = cons.Mode.TIME
    has_header = True
    identifier = r'^ScriptType: v4.00\s*$', 0

    header_template = \
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

    event_fields = (
        'Marked',
        'Start',
        'End',
        'Style',
        'Name',
        'MarginL',
        'MarginR',
        'MarginV',
        'Effect',
        'Text'
    )

    def read(self):
        """
        Read Sub Station Alpha file.

        Raise IOError if reading fails.
        Raise UnicodeError if decoding fails.
        Return show times, hide times, texts.
        """
        re_comma = re.compile(r',\s*')

        # Indexes of data on dialog lines
        show_index = None
        hide_index = None
        text_index = None

        # Amount of dialog fields minus one
        max_split = None

        shows  = []
        hides  = []
        texts  = []
        header = ''
        header_read = False
        lines = self._read_lines()
        for line in lines:
            if header_read and line.startswith('Dialogue:'):
                line = line.replace('Dialogue:', '').strip()
                fields = re_comma.split(line, max_split)
                shows.append(fields[show_index])
                hides.append(fields[hide_index])
                texts.append(fields[text_index].strip())
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
        if header:
            self.header = header.strip()

        shows = list('0' + x.replace('.', ',') + '0' for x in shows)
        hides = list('0' + x.replace('.', ',') + '0' for x in hides)
        texts = list(x.replace('\\n', '\n')          for x in texts)
        texts = list(x.replace('\\N', '\n')          for x in texts)

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
        newline_char = self._get_newline_character()
        calc = TimeFrameCalculator()

        texts = list(x.replace('\n', '\\n')    for x in texts)
        shows = list(calc.round_time(x, 2)     for x in shows)
        hides = list(calc.round_time(x, 2)     for x in hides)
        shows = list(x[1:11].replace(',', '.') for x in shows)
        hides = list(x[1:11].replace(',', '.') for x in hides)

        fobj = codecs.open(self.path, 'w', self.encoding)
        try:
            fobj.write(self.header)
            fobj.write(newline_char * 2)
            fobj.write('[Events]')
            fobj.write(newline_char)
            fobj.write('Format: ' + ', '.join(self.event_fields))
            fobj.write(newline_char)
            for i in range(len(shows)):
                fobj.write('Dialogue: 0,%s,%s,Default,,0000,0000,0000,,%s%s' %(
                    shows[i], hides[i], texts[i], newline_char))
        finally:
            fobj.close()
