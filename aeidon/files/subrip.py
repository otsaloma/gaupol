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

"""SubRip file."""

import aeidon
import re

__all__ = ("SubRip",)


class SubRip(aeidon.SubtitleFile):

    """SubRip file."""

    format = aeidon.formats.SUBRIP
    mode = aeidon.modes.TIME

    _re_time_line = re.compile((
        # Techically all these fields should have fixed widths, but in the
        # name of being liberal in accepting input, accept lesser widths
        # assuming that they are just lacking zero-padding from the side
        # that is farther from the decimal point.
        r"^(-?\d{1,2}:\d{1,2}:\d{1,2},\d{1,3}) -->"
        r" (-?\d{1,2}:\d{1,2}:\d{1,2},\d{1,3})"
        r"(  X1:(\d+) X2:(\d+) Y1:(\d+) Y2:(\d+))?\s*$"))

    def read(self):
        """
        Read file and return subtitles.

        Raise :exc:`IOError` if reading fails.
        Raise :exc:`UnicodeError` if decoding fails.
        """
        subtitles = []
        for line in self._read_lines():
            match = self._re_time_line.match(line)
            if match is None:
                if subtitles[-1].main_text:
                    subtitles[-1].main_text += "\n"
                subtitles[-1].main_text += line
                continue
            subtitle = self._get_subtitle()
            subtitle.start_time = subtitle.calc.normalize_time(match.group(1))
            subtitle.end_time = subtitle.calc.normalize_time(match.group(2))
            if match.group(3) is not None:
                subtitle.subrip.x1 = int(match.group(4))
                subtitle.subrip.x2 = int(match.group(5))
                subtitle.subrip.y1 = int(match.group(6))
                subtitle.subrip.y2 = int(match.group(7))
            subtitles.append(subtitle)
        return subtitles

    def _read_lines(self):
        """Read file to a unicoded list of lines."""
        lines = ["\n"]
        for line in aeidon.SubtitleFile._read_lines(self):
            lines.append(line)
            match = self._re_time_line.match(line)
            if match is None: continue
            # Remove numbers and blank lines above them.
            if lines[-2].strip().isdigit():
                if not lines[-3].strip():
                    lines.pop(-3)
                lines.pop(-2)
        return lines

    def write_to_file(self, subtitles, doc, f):
        """
        Write `subtitles` from `doc` to file `f`.

        Raise :exc:`IOError` if writing fails.
        Raise :exc:`UnicodeError` if encoding fails.
        """
        for i, subtitle in enumerate(subtitles):
            if i > 0: f.write("\n")
            f.write("{:d}\n".format(i + 1))
            start = subtitle.start_time.replace(".", ",")
            end = subtitle.end_time.replace(".", ",")
            f.write("{} --> {}".format(start, end))
            # Write Extended SubRip coordinates only if the container
            # has been initialized and the coordinates make some sense.
            if subtitle.has_container("subrip"):
                x1 = subtitle.subrip.x1
                x2 = subtitle.subrip.x2
                y1 = subtitle.subrip.y1
                y2 = subtitle.subrip.y2
                if not x1 == x2 == y1 == y2 == 0:
                    f.write("  X1:{:03d} X2:{:03d}".format(x1, x2))
                    f.write( " Y1:{:03d} Y2:{:03d}".format(y1, y2))
            f.write("\n{}\n".format(subtitle.get_text(doc)))
