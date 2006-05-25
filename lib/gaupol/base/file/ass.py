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


"""Advanced Sub Station Alpha file."""


try:
    from psyco.classes import *
except ImportError:
    pass

import codecs

from gaupol.base.files.ssa      import SubStationAlpha
from gaupol.base.position.calc import TimeFrameCalculator
from gaupol.base.util           import listlib
from gaupol.base.cons           import Format, Mode



class AdvancedSubStationAlpha(SubStationAlpha):

    """Advanced Sub Station Alpha file."""

    FORMAT = Format.ASS

    id_pattern = r'^ScriptType: v4.00\+\s*$', None

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
ScriptType: v4.00+
Collisions: Normal
PlayResY:
PlayResX:
PlayDepth:
Timer: 100.0000
WrapStyle:

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Arial,18,&H00ffffff,&H0000ffff,&H00000000,&H00000000,0,0,0,0,100,100,0,0.00,1,2,2,2,30,30,10,0'''

    def write(self, shows, hides, texts):
        """
        Write Advanced Sub Station Alpha file.

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
            subtitle_file.write('Format: Layer, Start, End, Style, Name, ')
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

    class TestAdvancedSubStationAlpha(Test):

        def test_all(self):

            path = self.get_subrip_path()
            subrip_file = SubRip(path, 'utf_8')
            data = subrip_file.read()

            args = path, 'utf_8', subrip_file.newlines
            ass_file = AdvancedSubStationAlpha(*args)
            ass_file.write(*data)
            data_1 = ass_file.read()
            ass_file.write(*data_1)
            data_2 = ass_file.read()
            assert data_2 == data_1

    TestAdvancedSubStationAlpha().run()
