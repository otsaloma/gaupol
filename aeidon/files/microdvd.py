# -*- coding: utf-8 -*-

# Copyright (C) 2005 Osmo Salomaa
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""MicroDVD file."""

import aeidon
import re

__all__ = ("MicroDVD",)


class MicroDVD(aeidon.SubtitleFile):

    """MicroDVD file."""

    format = aeidon.formats.MICRODVD
    mode = aeidon.modes.FRAME
    _re_line = re.compile(r"^\{(-?\d+)\}\{(-?\d+)\}(.*?)$")

    def read(self):
        """
        Read file and return subtitles.

        Raise :exc:`IOError` if reading fails.
        Raise :exc:`UnicodeError` if decoding fails.
        """
        subtitles = []
        for line in self._read_lines():
            match = self._re_line.match(line)
            if match is not None:
                subtitle = self._get_subtitle()
                subtitle.start_frame = int(match.group(1))
                subtitle.end_frame = int(match.group(2))
                subtitle.main_text = match.group(3).replace("|", "\n")
                subtitles.append(subtitle)
            elif line.startswith("{DEFAULT}"):
                self.header = line
        return subtitles

    def write_to_file(self, subtitles, doc, f):
        """
        Write `subtitles` from `doc` to file `f`.

        Raise :exc:`IOError` if writing fails.
        Raise :exc:`UnicodeError` if encoding fails.
        """
        if self.header.strip():
            f.write(self.header + "\n")
        for subtitle in subtitles:
            text = subtitle.get_text(doc).replace("\n", "|")
            f.write(("{{{:d}}}{{{:d}}}{}\n"
                     .format(subtitle.start_frame,
                             subtitle.end_frame,
                             text)))
