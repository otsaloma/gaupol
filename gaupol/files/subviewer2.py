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

"""SubViewer 2.0 file."""

import gaupol
import re

__all__ = ("SubViewer2",)


class SubViewer2(gaupol.SubtitleFile):

    """SubViewer 2.0 file."""

    _re_time_line = re.compile((
        r"^(-?\d\d:\d\d:\d\d.\d\d)"
        r",(-?\d\d:\d\d:\d\d.\d\d)\s*$"))
    format = gaupol.formats.SUBVIEWER2
    mode = gaupol.modes.TIME

    def read(self):
        """Read file and return subtitles.

        Raise IOError if reading fails.
        Raise UnicodeError if decoding fails.
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
            subtitle.start = match.group(1) + "0"
            subtitle.end = match.group(2) + "0"
            text = lines[i + 1].replace("[br]", "\n")
            subtitle.main_text = text
            subtitles.append(subtitle)
        return subtitles

    def write_to_file(self, subtitles, doc, fobj):
        """Write subtitles from document to given file.

        Raise IOError if writing fails.
        Raise UnicodeError if encoding fails.
        """
        fobj.write(self.header)
        fobj.write(self.newline.value)
        for subtitle in subtitles:
            fobj.write(self.newline.value)
            start = subtitle.calc.round_time(subtitle.start_time, 2)[:-1]
            end = subtitle.calc.round_time(subtitle.end_time, 2)[:-1]
            fobj.write("%s,%s%s" % (start, end, self.newline.value))
            fobj.write(subtitle.get_text(doc).replace("\n", "[br]"))
            fobj.write(self.newline.value)
