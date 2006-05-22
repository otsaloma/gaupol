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


"""SubRip file."""


try:
    from psyco.classes import *
except ImportError:
    pass

import codecs
import re

from gaupol.base.files import SubtitleFile
from gaupol.base.util  import listlib
from gaupol.base.cons  import Format, Mode


class SubRip(SubtitleFile):

    """SubRip file."""

    FORMAT     = Format.SUBRIP
    HAS_HEADER = False
    MODE       = Mode.TIME

    id_pattern = r'^\d\d:\d\d:\d\d,\d\d\d --> \d\d:\d\d:\d\d,\d\d\d\s*$', None

    def read(self):
        """
        Read Subrip file.

        Raise IOError if reading fails.
        Raise UnicodeError if decoding fails.
        Return show times, hide times, texts.
        """
        # Compile regular expressions.
        re_blank_line = re.compile(r'^\s*$')
        time = r'\d\d:\d\d:\d\d,\d\d\d'
        re_time_line = re.compile(r'^(%s) --> (%s)\s*$' % (time, time))

        lines = self._read_lines()
        good_lines = []

        # Remove blank lines and unit numbers.
        for line in lines:
            if re_blank_line.match(line) is not None:
                continue
            elif re_time_line.match(line) is not None:
                good_lines[-1] = line
            else:
                good_lines.append(line)

        shows = []
        hides = []
        texts = []

        # Split to components.
        for line in good_lines:
            match = re_time_line.match(line)
            if match is not None:
                shows.append(match.group(1))
                hides.append(match.group(2))
                texts.append(u'')
            else:
                texts[-1] += line

        # Remove leading and trailing spaces.
        texts = listlib.strip(texts)

        return shows, hides, texts

    def write(self, shows, hides, texts):
        """
        Write SubRip file.

        Raise IOError if writing fails.
        Raise UnicodeError if encoding fails.
        """
        texts = texts[:]
        newline_character = self._get_newline_character()

        # Replace Python internal newline characters in text with desired
        # newline characters.
        texts = list(text.replace('\n', newline_character) for text in texts)

        subtitle_file = codecs.open(self.path, 'w', self.encoding)

        try:
            for i in range(len(shows)):
                subtitle_file.write('%.0f%s%s --> %s%s%s%s%s' % (
                    i + 1, newline_character,
                    shows[i], hides[i], newline_character,
                    texts[i], newline_character, newline_character
                ))
        finally:
            subtitle_file.close()


if __name__ == '__main__':

    from gaupol.test import Test

    class TestSubRip(Test):

        def test_all(self):

            path = self.get_subrip_path()
            subrip_file = SubRip(path, 'utf_8')
            data_1 = subrip_file.read()
            subrip_file.write(*data_1)
            data_2 = subrip_file.read()
            assert data_2 == data_1

    TestSubRip().run()
