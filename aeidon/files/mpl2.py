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

"""MPL2 file."""

import aeidon
import re

__all__ = ("MPL2",)


class MPL2(aeidon.SubtitleFile):

    """MPL2 file."""

    format = aeidon.formats.MPL2
    mode = aeidon.modes.TIME
    _re_line = re.compile(r"^\[(-?\d+)\]\[(-?\d+)\](.*?)$")

    def read(self):
        """
        Read file and return subtitles.

        Raise :exc:`IOError` if reading fails.
        Raise :exc:`UnicodeError` if decoding fails.
        """
        subtitles = []
        for line in self._read_lines():
            match = self._re_line.match(line)
            if match is None: continue
            subtitle = self._get_subtitle()
            subtitle.start_seconds = float(match.group(1)) / 10
            subtitle.end_seconds = float(match.group(2)) / 10
            subtitle.main_text = match.group(3).replace("|", "\n")
            subtitles.append(subtitle)
        return subtitles

    def write_to_file(self, subtitles, doc, f):
        """
        Write `subtitles` from `doc` to file `f`.

        Raise :exc:`IOError` if writing fails.
        Raise :exc:`UnicodeError` if encoding fails.
        """
        for subtitle in subtitles:
            text = subtitle.get_text(doc).replace("\n", "|")
            f.write(("[{:.0f}][{:.0f}]{}\n"
                     .format(subtitle.start_seconds * 10,
                             subtitle.end_seconds * 10,
                             text)))
