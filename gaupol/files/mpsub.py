# Copyright (C) 2006 Osmo Salomaa
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


"""MPsub file."""


import codecs
import re

from gaupol import const
from gaupol.calculator import Calculator
from ._subfile import SubtitleFile


class MPsub(SubtitleFile):

    """MPsub file.

    Class variables:

        mode: MODE constant
    """

    format = const.FORMAT.MPSUB
    framerate  = None
    has_header = True
    identifier = r"^FORMAT=(TIME|[\d\.]+)\s*$", 0
    mode = const.MODE.TIME

    def _clean_lines(self, all_lines, re_time_line):
        """Return lines without blank lines preceding time lines."""

        lines = ["\n"]
        for line in all_lines:
            if re_time_line.match(line) is not None:
                if not lines[-1].strip():
                    lines[-1] = line
                    continue
            lines.append(line)
        return lines

    def _get_mpsub_frames(self, shows, hides):
        """Get MPsub style shows and hides as frames."""

        shows = shows[:]
        hides = hides[:]
        for i in reversed(range(1, len(shows))):
            hides[i] = str(hides[i] - shows[i])
            shows[i] = str(shows[i] - hides[i - 1])
        hides[0] = str(hides[0] - shows[0])
        return shows, hides

    def _get_mpsub_times(self, shows, hides):
        """Get MPsub style shows and hides as times."""

        calc = Calculator()
        shows = [calc.time_to_seconds(x) for x in shows]
        hides = [calc.time_to_seconds(x) for x in hides]
        for i in reversed(range(1, len(shows))):
            hides[i] -= shows[i]
            shows[i] -= hides[i - 1]
        hides[0] -= shows[0]

        deviation = 0
        for i in range(len(shows)):
            orig_show = shows[i]
            shows[i] = round(shows[i] - deviation, 2)
            deviation = deviation + shows[i] - orig_show
            orig_hide = hides[i]
            hides[i] = round(hides[i] - deviation, 2)
            deviation = deviation + hides[i] - orig_hide

        shows = ["%.2f" % x for x in shows]
        hides = ["%.2f" % x for x in hides]
        return shows, hides

    def _read_components(self, lines, re_time_line):
        """Read and return shows, hides and texts."""

        shows = []
        hides = []
        texts = []
        for line in lines:
            match = re_time_line.match(line)
            if match is not None:
                show = float(match.group(1))
                show = (show + hides[-1] if hides else show)
                shows.append(show)
                hides.append(shows[-1] + float(match.group(2)))
                texts.append(u"")
            elif texts:
                texts[-1] += line

        calc = Calculator()
        if self.mode == const.MODE.TIME:
            shows = [calc.seconds_to_time(x) for x in shows]
            hides = [calc.seconds_to_time(x) for x in hides]
        elif self.mode == const.MODE.FRAME:
            shows = [int(round(x, 0)) for x in shows]
            hides = [int(round(x, 0)) for x in hides]
        re_trailer = re.compile(r"\n\Z", re.MULTILINE)
        texts = [re_trailer.sub("", x) for x in texts]
        return shows, hides, texts

    def _read_header(self, lines, re_time_line):
        """Read header and return leftover lines."""

        header = ""
        while re_time_line.match(lines[0]) is None:
            header += lines.pop(0)
        self.header = header[:-1]
        return lines

    def read(self):
        """Read file.

        Raise IOError if reading fails.
        Raise UnicodeError if decoding fails.
        Raise ValueError if bad FORMAT line.
        Return shows, hides, texts.
        """
        re_time_line = re.compile(r"^([\d\.]+) ([\d\.]+)\s*$")
        lines = self._read_lines()
        lines = self._clean_lines(lines, re_time_line)
        lines = self._read_header(lines, re_time_line)
        return self._read_components(lines, re_time_line)

    def set_header(self, header):
        """Parse and set header and mode.

        Raise ValueError if bad FORMAT line.
        """
        mode = None
        for line in header.split("\n"):
            if line.startswith("FORMAT="):
                mode = line[7:].strip()
        if not mode in (const.FRAMERATE.mpsub_names + ["TIME"]):
            raise ValueError

        self.header = header
        self.framerate = None
        self.mode = const.MODE.TIME
        if mode in const.FRAMERATE.mpsub_names:
            index = const.FRAMERATE.mpsub_names.index(mode)
            self.framerate = const.FRAMERATE.members[index]
            self.mode = const.MODE.FRAME

    def write(self, shows, hides, texts):
        """Write file.

        Raise IOError if writing fails.
        Raise UnicodeError if encoding fails.
        """
        method = (self._get_mpsub_times, self._get_mpsub_frames)[self.mode]
        shows, hides = method(shows, hides)
        texts = [x.replace("\n", self.newline.value) for x in texts]

        fobj = codecs.open(self.path, "w", self.encoding)
        try:
            fobj.write(self.header + self.newline.value * 2)
            for i in range(len(shows)):
                fobj.write("%s %s%s%s%s%s" % (
                    shows[i], hides[i], self.newline.value,
                    texts[i], self.newline.value, self.newline.value))
        finally:
            fobj.close()
