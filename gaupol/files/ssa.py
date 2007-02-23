# Copyright (C) 2005-2007 Osmo Salomaa
#
# This file is part of Gaupol.
#
# Gaupol is free software; you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.
#
# Gaupol is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# Gaupol; if not, write to the Free Software Foundation, Inc., 51 Franklin
# Street, Fifth Floor, Boston, MA 02110-1301, USA.


"""Sub Station Alpha file."""


import codecs
import re

from gaupol import cons
from gaupol.calculator import Calculator
from ._subfile import SubtitleFile


class SubStationAlpha(SubtitleFile):

    """Sub Station Alpha file.

    Class variables:

        event_fields: Tuple of the fields under 'Events' section
    """

    format = cons.FORMAT.SSA
    has_header = True
    identifier = r"^ScriptType: [vV]4.00\s*$", 0
    mode = cons.MODE.TIME

    event_fields = (
        "Marked",
        "Start",
        "End",
        "Style",
        "Name",
        "MarginL",
        "MarginR",
        "MarginV",
        "Effect",
        "Text",)

    def _read_components(self, lines):
        """Read and return shows, hides and texts."""

        shows = []
        hides = []
        texts = []
        re_comma = re.compile(r",\s*")
        for line in lines:
            if line.startswith("Format:"):
                line = line.replace("Format:", "").strip()
                fields = re_comma.split(line)
                show_index = fields.index("Start")
                hide_index = fields.index("End")
                text_index = fields.index("Text")
                max_split = len(fields) - 1
            elif line.startswith("Dialogue:"):
                line = line.replace("Dialogue:", "")[:-1]
                fields = re_comma.split(line, max_split)
                shows.append(fields[show_index])
                hides.append(fields[hide_index])
                texts.append(fields[text_index])

        shows = list("0" + x + "0" for x in shows)
        hides = list("0" + x + "0" for x in hides)
        texts = list(x.replace("\\n", "\n") for x in texts)
        texts = list(x.replace("\\N", "\n") for x in texts)
        return shows, hides, texts

    def _read_header(self, lines):
        """Read header and return leftover lines."""

        header = ""
        while not lines[0].startswith("[Events]"):
            header += lines.pop(0)
        if header:
            self.header = header.strip()
        return lines

    def read(self):
        """Read file.

        Raise IOError if reading fails.
        Raise UnicodeError if decoding fails.
        Return show times, hide times, texts.
        """
        lines = self._read_lines()
        lines = self._read_header(lines)
        return self._read_components(lines)

    def write(self, shows, hides, texts):
        """Write file.

        Raise IOError if writing fails.
        Raise UnicodeError if encoding fails.
        """
        calc = Calculator()
        shows = list(calc.round_time(x, 2)[1:11] for x in shows)
        hides = list(calc.round_time(x, 2)[1:11] for x in hides)
        texts = list(x.replace("\n", "\\n") for x in texts)

        fobj = codecs.open(self.path, "w", self.encoding)
        try:
            fobj.write(self.header)
            fobj.write(self.newline.value * 2)
            fobj.write("[Events]")
            fobj.write(self.newline.value)
            fobj.write("Format: " + ", ".join(self.event_fields))
            fobj.write(self.newline.value)
            for i in range(len(shows)):
                fobj.write("Dialogue: 0,%s,%s,Default,,0000,0000,0000,,%s%s" \
                    % (shows[i], hides[i], texts[i], self.newline.value))
        finally:
            fobj.close()
