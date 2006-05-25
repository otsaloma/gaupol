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


"""MicroDVD file."""


try:
    from psyco.classes import *
except ImportError:
    pass

import codecs
import re

from gaupol.base.file import SubtitleFile
from gaupol.base.cons  import Format, Mode


class MicroDVD(SubtitleFile):

    """MicroDVD file."""

    FORMAT     = Format.MICRODVD
    HAS_HEADER = False
    MODE       = Mode.FRAME

    id_pattern = r'^\{\d+\}\{\d+\}.*?$', None

    def read(self):
        """
        Read MicroDVD file.

        Raise IOError if reading fails.
        Raise UnicodeError if decoding fails.
        Return show frames, hide frames, texts.
        """
        # Compile regular expressions.
        re_line = re.compile(r'^\{(\d+)\}\{(\d+)\}(.*?)$')

        lines = self._read_lines()

        shows = []
        hides = []
        texts = []

        # Split lines list to components.
        for line in lines:
            match = re_line.match(line)
            if match is not None:
                shows.append(match.group(1))
                hides.append(match.group(2))
                texts.append(match.group(3))

        # Frames should be integers.
        shows = list(int(frame) for frame in shows)
        hides = list(int(frame) for frame in hides)

        # Replace pipes in texts with Python internal newline characters.
        for i in range(len(texts)):
            texts[i] = texts[i].replace('|', '\n')

        return shows, hides, texts

    def write(self, shows, hides, texts):
        """
        Write MicroDVD file.

        Raise IOError if writing fails.
        Raise UnicodeError if encoding fails.
        """
        texts = texts[:]
        newline_character = self._get_newline_character()

        # Replace Python internal newline characters in text with pipes.
        texts = list(text.replace('\n', '|') for text in texts)

        subtitle_file = codecs.open(self.path, 'w', self.encoding)

        try:
            for i in range(len(shows)):
                subtitle_file.write('{%.0f}{%.0f}%s%s' % (
                    shows[i], hides[i], texts[i], newline_character
                ))
        finally:
            subtitle_file.close()


if __name__ == '__main__':

    from gaupol.test import Test

    class TestMicroDVD(Test):

        def test_all(self):

            path = self.get_micro_dvd_path()
            micro_dvd_file = MicroDVD(path, 'utf_8')
            data_1 = micro_dvd_file.read()
            micro_dvd_file.write(*data_1)
            data_2 = micro_dvd_file.read()
            assert data_2 == data_1

    TestMicroDVD().run()
