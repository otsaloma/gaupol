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


# Documentation:
# http://netti.nic.fi/~temp/easydivx/help/mdvddoc


try:
    from psyco.classes import *
except ImportError:
    pass

import codecs
import re

from gaupol.base.files import SubtitleFile
from gaupol.constants  import Format, Mode


class MicroDVD(SubtitleFile):

    """
    MicroDVD file.

    MicroDVD format quick reference:
    {436}{531}And that completes my final report|until we reach touchdown.
    {533}{624}We're now on full automatic,|in the hands of the computers.
    """

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
