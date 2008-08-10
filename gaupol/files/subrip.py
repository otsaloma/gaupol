# Copyright (C) 2005-2008 Osmo Salomaa
#
# This file is part of Gaupol.
#
# Gaupol is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# Gaupol is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# Gaupol. If not, see <http://www.gnu.org/licenses/>.

"""SubRip file."""

import gaupol
import re

__all__ = ("SubRip",)


class SubRip(gaupol.SubtitleFile):

    """SubRip file."""

    _re_time_line = re.compile((
        r"^(-?\d\d:\d\d:\d\d,\d\d\d) -->"
        r" (-?\d\d:\d\d:\d\d,\d\d\d)"
        r"(  X1:(\d+) X2:(\d+) Y1:(\d+) Y2:(\d+))?\s*$"))
    format = gaupol.formats.SUBRIP
    mode = gaupol.modes.TIME

    def _read_lines(self):
        """Read file to a unicoded list of lines."""

        lines = ["\n"]
        for line in gaupol.SubtitleFile._read_lines(self):
            lines.append(line)
            match = self._re_time_line.match(line)
            if match is None: continue
            # Remove numbers and blank lines above them.
            if lines[-2].strip().isdigit():
                if not lines[-3].strip(): lines.pop(-3)
                lines.pop(-2)
        return lines

    def read(self):
        """Read file and return subtitles.

        Raise IOError if reading fails.
        Raise UnicodeError if decoding fails.
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
            subtitle.start = match.group(1).replace(",", ".")
            subtitle.end = match.group(2).replace(",", ".")
            if match.group(3) is not None:
                subtitle.subrip.x1 = int(match.group(4))
                subtitle.subrip.x2 = int(match.group(5))
                subtitle.subrip.y1 = int(match.group(6))
                subtitle.subrip.y2 = int(match.group(7))
            subtitles.append(subtitle)
        return subtitles

    def write_to_file(self, subtitles, doc, fobj):
        """Write subtitles from document to given file.

        Raise IOError if writing fails.
        Raise UnicodeError if encoding fails.
        """
        n = self.newline.value
        for i, subtitle in enumerate(subtitles):
            if i > 0: fobj.write(n)
            fobj.write("%d%s" % ((i + 1), n))
            start = subtitle.start_time.replace(".", ",")
            end = subtitle.end_time.replace(".", ",")
            fobj.write("%s --> %s" % (start, end))
            # Write Extended SubRip coordinates only if the container
            # has been initialized and the coordinates make some sense.
            if subtitle.has_container("subrip"):
                x1 = subtitle.subrip.x1
                x2 = subtitle.subrip.x2
                y1 = subtitle.subrip.y1
                y2 = subtitle.subrip.y2
                if not (x1 == x2 == y1 == y2 == 0):
                    fobj.write("  X1:%03d X2:%03d" % (x1, x2))
                    fobj.write( " Y1:%03d Y2:%03d" % (y1, y2))
            text = subtitle.get_text(doc).replace("\n", n)
            fobj.write("%s%s%s" % (n, text, n))
