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


from __future__ import with_statement

import codecs
import contextlib
import gaupol
import re

from .subfile import SubtitleFile


class SubStationAlpha(SubtitleFile):

    """Sub Station Alpha file.

    Class variables:
     * event_fields: Tuple of the names of fields under the 'Events' section
    """

    __metaclass__ = gaupol.Contractual
    format = gaupol.FORMAT.SSA
    mode = gaupol.MODE.TIME

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
        """Read and return starts, ends and texts."""

        starts = []
        ends = []
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
                starts.append(fields[show_index])
                ends.append(fields[hide_index])
                texts.append(fields[text_index])

        starts = ["0%s0" % x for x in starts]
        ends = ["0%s0" % x for x in ends]
        texts = [x.replace("\\n", "\n") for x in texts]
        texts = [x.replace("\\N", "\n") for x in texts]
        return starts, ends, texts

    def _read_header(self, lines):
        """Read header and return leftover lines."""

        header = ""
        lines = lines[:]
        while not lines[0].startswith("[Events]"):
            header += lines.pop(0)
        if header:
            self.header = header.strip()
        return lines

    def read(self):
        """Read file.

        Raise IOError if reading fails.
        Raise UnicodeError if decoding fails.
        Return start times, end times, texts.
        """
        lines = self._read_lines()
        lines = self._read_header(lines)
        return self._read_components(lines)

    def write(self, starts, ends, texts):
        """Write file.

        Raise IOError if writing fails.
        Raise UnicodeError if encoding fails.
        """
        calc = gaupol.Calculator()
        starts = [calc.round_time(x, 2)[1:11] for x in starts]
        ends = [calc.round_time(x, 2)[1:11] for x in ends]
        texts = [x.replace("\n", "\\n") for x in texts]

        args = (self.path, "w", self.encoding)
        with contextlib.closing(codecs.open(*args)) as fobj:
            fobj.write(self.header)
            fobj.write(self.newline.value)
            fobj.write(self.newline.value)
            fobj.write("[Events]")
            fobj.write(self.newline.value)
            fobj.write("Format: " + ", ".join(self.event_fields))
            fobj.write(self.newline.value)
            for i in range(len(starts)):
                fobj.write("Dialogue: 0,")
                fobj.write(starts[i])
                fobj.write(",")
                fobj.write(ends[i])
                fobj.write(",Default,,0000,0000,0000,,")
                fobj.write(texts[i])
                fobj.write(self.newline.value)
