# Copyright (C) 2006-2008 Osmo Salomaa
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

"""MPsub file."""

import gaupol
import re

__all__ = ("MPsub",)


class MPsub(gaupol.SubtitleFile):

    """MPsub file.

    Instance variables framerate and mode depend on what is written on the
    first line of the file header. They will be determined when the file is
    read and are changed when the 'set_header' method is called.
    """

    _re_position_line = re.compile(r"^(-?[\d.]+) (-?[\d.]+)\s*$")
    format = gaupol.formats.MPSUB
    mode = gaupol.modes.TIME

    def __init__(self, path, encoding, newline=None):

        gaupol.SubtitleFile.__init__(self, path, encoding, newline)
        self.framerate = gaupol.framerates.NONE
        self.mode = gaupol.modes.TIME

    def _get_frames(self, subtitles):
        """Return MPsub style start and end frames."""

        starts = [x.start_frame for x in subtitles]
        ends = [x.end_frame for x in subtitles]
        for i in reversed(range(1, len(subtitles))):
            ends[i] = ends[i] - starts[i]
            starts[i] = starts[i] - ends[i - 1]
        ends[0] = ends[0] - starts[0]
        return map(str, starts), map(str, ends)

    def _get_positions(self, subtitles):
        """Return MPsub style start and end positions."""

        if self.mode == gaupol.modes.TIME:
            return self._get_times(subtitles)
        if self.mode == gaupol.modes.FRAME:
            return self._get_frames(subtitles)
        raise ValueError

    def _get_times(self, subtitles):
        """Return MPsub style start and end times."""

        starts = [x.start_seconds for x in subtitles]
        ends = [x.end_seconds for x in subtitles]
        deviation = 0
        # Avoid cumulation of rounding errors by keeping track of deviations
        # and adjusting times so that the deviation stays close to zero.
        for i in reversed(range(1, len(subtitles))):
            real_diff = ends[i] - starts[i]
            ends[i] = round(real_diff - deviation, 2)
            deviation += (ends[i] - real_diff)
            real_diff = starts[i] - ends[i - 1]
            starts[i] = round(real_diff - deviation, 2)
            deviation += (starts[i] - real_diff)
        ends[0] = ends[0] - starts[0]
        to_string = lambda x: ("%.2f" % x).replace("-0.00", "0.00")
        return map(to_string, starts), map(to_string, ends)

    def _read_header(self, lines):
        """Read header and remove its lines."""

        header = ""
        while not self._re_position_line.match(lines[0]):
            header += "\n"
            header += lines.pop(0)
        header = header.lstrip()
        self.set_header(header)

    def _read_lines(self):
        """Read file to a unicoded list of lines."""

        lines = ["\n"]
        for line in gaupol.SubtitleFile._read_lines(self):
            lines.append(line)
            match = self._re_position_line.match(line)
            if match is None: continue
            # Remove blank lines above position lines.
            if not lines[-2].strip(): lines.pop(-2)
        return lines

    def copy_from(self, other):
        """Copy generic properties from file of same format."""

        gaupol.SubtitleFile.copy_from(self, other)
        if self.format == other.format:
            self.mode = other.mode
            self.framerate = other.framerate

    def read(self):
        """Read file and return subtitles.

        Raise IOError if reading fails.
        Raise UnicodeError if decoding fails.
        """
        subtitles = []
        lines = self._read_lines()
        self._read_header(lines)
        convert = (float if self.mode == gaupol.modes.TIME else int)
        end = convert("0")
        for line in lines:
            match = self._re_position_line.match(line)
            if match is None:
                if subtitles[-1].main_text:
                    subtitles[-1].main_text += "\n"
                subtitles[-1].main_text += line
                continue
            subtitle = self._get_subtitle()
            start = end + convert(match.group(1))
            end = start + convert(match.group(2))
            subtitle.start = start
            subtitle.end = end
            subtitles.append(subtitle)
        return subtitles

    def set_header(self, header):
        """Parse and set header, mode and framerate.

        Raise ValueError if FORMAT line is invalid.
        """
        mode = gaupol.modes.NONE
        framerates = dict((x.mpsub, x) for x in gaupol.framerates)
        for line in header.split("\n"):
            if line.startswith("FORMAT="):
                mode = line[7:].strip()
        if mode == "TIME":
            self.mode = gaupol.modes.TIME
            self.framerate = gaupol.framerates.NONE
        elif mode in framerates.keys():
            self.mode = gaupol.modes.FRAME
            self.framerate = framerates[mode]
        else: raise ValueError
        self.header = header

    def write_to_file(self, subtitles, doc, fobj):
        """Write subtitles from document to given file.

        Raise IOError if writing fails.
        Raise UnicodeError if encoding fails.
        """
        n = self.newline.value
        starts, ends = self._get_positions(subtitles)
        fobj.write("%s%s%s" % (self.header, n, n))
        for i, subtitle in enumerate(subtitles):
            if i > 0: fobj.write(n)
            fobj.write("%s %s%s" % (starts[i], ends[i], n))
            text = subtitle.get_text(doc).replace("\n", n)
            fobj.write("%s%s" % (text, n))
