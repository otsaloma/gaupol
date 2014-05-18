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

"""SubViewer 2.0 file."""

import aeidon
import re

__all__ = ("SubViewer2",)


class SubViewer2(aeidon.SubtitleFile):

    """SubViewer 2.0 file."""

    format = aeidon.formats.SUBVIEWER2
    mode = aeidon.modes.TIME
    _re_time_line = re.compile((r"^(-?\d\d:\d\d:\d\d.\d\d)"
                                r",(-?\d\d:\d\d:\d\d.\d\d)\s*$"))

    def read(self):
        """
        Read file and return subtitles.

        Raise :exc:`IOError` if reading fails.
        Raise :exc:`UnicodeError` if decoding fails.
        """
        self.header = ""
        subtitles = []
        lines = self._read_lines()
        while lines[0].startswith("["):
            self.header += "\n"
            self.header += lines.pop(0)
        self.header = self.header.lstrip()
        for i, line in enumerate(lines + [""]):
            match = self._re_time_line.match(line)
            if match is None: continue
            subtitle = self._get_subtitle()
            subtitle.start_time = match.group(1) + "0"
            subtitle.end_time = match.group(2) + "0"
            text = lines[i+1].replace("[br]", "\n")
            subtitle.main_text = text
            subtitles.append(subtitle)
        return subtitles

    def write_to_file(self, subtitles, doc, f):
        """
        Write `subtitles` from `doc` to file `f`.

        Raise :exc:`IOError` if writing fails.
        Raise :exc:`UnicodeError` if encoding fails.
        """
        f.write(self.header + "\n")
        for subtitle in subtitles:
            start = subtitle.calc.round(subtitle.start_time, 2)[:-1]
            end = subtitle.calc.round(subtitle.end_time, 2)[:-1]
            text = subtitle.get_text(doc).replace("\n", "[br]")
            f.write("\n{},{}\n{}\n".format(start, end, text))
