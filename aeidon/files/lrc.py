# -*- coding: utf-8 -*-

# Copyright (C) 2017 Osmo Salomaa
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

"""LRC file."""

import aeidon
import re

__all__ = ("LRC",)


class LRC(aeidon.SubtitleFile):

    """
    LRC file.

    https://en.wikipedia.org/wiki/LRC_(file_format)
    """

    format = aeidon.formats.LRC
    mode = aeidon.modes.TIME
    _re_line = re.compile(r"^\[(-?\d\d:\d\d.\d\d)\](.*)$")

    def read(self):
        """
        Read file and return subtitles.

        Raise :exc:`IOError` if reading fails.
        Raise :exc:`UnicodeError` if decoding fails.
        """
        self.header = ""
        subtitles = [self._get_subtitle()]
        for line in self._read_lines():
            match = self._re_line.match(line)
            if match is None and len(subtitles) == 1:
                # Read line into file header.
                if self.header:
                    self.header += "\n"
                self.header += line
            elif match is not None:
                subtitle = self._get_subtitle()
                normalize = subtitle.calc.normalize_time
                subtitle.start_time = normalize(match.group(1))
                subtitles[-1].end_time = subtitle.start_time
                subtitle.main_text = match.group(2) or ""
                subtitles.append(subtitle)
        subtitles[-1].duration_seconds = 5
        return subtitles[1:]

    def write_to_file(self, subtitles, doc, f):
        """
        Write `subtitles` from `doc` to file `f`.

        Raise :exc:`IOError` if writing fails.
        Raise :exc:`UnicodeError` if encoding fails.
        """
        if self.header.strip():
            f.write(self.header.strip() + "\n\n")
        for subtitle in subtitles:
            start = subtitle.calc.round(subtitle.start_time, 2)
            sign = "-" if start.startswith("-") else ""
            first = 4 if start.startswith("-") else 3
            start = sign + start[first:-1]
            text = subtitle.get_text(doc).replace("\n", " ")
            f.write("[{}]{}\n".format(start, text))
