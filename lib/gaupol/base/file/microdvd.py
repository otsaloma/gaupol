# Copyright (C) 2005-2006 Osmo Salomaa
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


import codecs
import re

from gaupol.base.cons import Format, Mode
from gaupol.base.file import SubtitleFile


class MicroDVD(SubtitleFile):

    """MicroDVD file."""

    format     = Format.MICRODVD
    mode       = Mode.FRAME
    has_header = False
    identifier = r'^\{\d+\}\{\d+\}.*?$', 0

    def read(self):
        """
        Read MicroDVD file.

        Raise IOError if reading fails.
        Raise UnicodeError if decoding fails.
        Return show frames, hide frames, texts.
        """
        re_line = re.compile(r'^\{(\d+)\}\{(\d+)\}(.*?)$')

        # Split to components.
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

        shows = list(int(frame)              for frame in shows)
        hides = list(int(frame)              for frame in hides)
        texts = list(text.replace('|', '\n') for text  in texts)

        return shows, hides, texts

    def write(self, shows, hides, texts):
        """
        Write MicroDVD file.

        Raise IOError if writing fails.
        Raise UnicodeError if encoding fails.
        """
        texts = texts[:]
        newline_char = self._get_newline_character()
        texts = list(text.replace('\n', '|') for text in texts)

        fobj = codecs.open(self.path, 'w', self.encoding)
        try:
            for i in range(len(shows)):
                fobj.write('{%.0f}{%.0f}%s%s' % (
                    shows[i], hides[i], texts[i], newline_char
                ))
        finally:
            fobj.close()
