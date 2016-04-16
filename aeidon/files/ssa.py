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

"""Sub Station Alpha file."""

import aeidon
import re

__all__ = ("SubStationAlpha",)


class SubStationAlpha(aeidon.SubtitleFile):

    """
    Sub Station Alpha file.

    :ivar event_fields: Tuple of field names for the ``[Events]`` section
    """

    format = aeidon.formats.SSA
    mode = aeidon.modes.TIME

    _re_file_time = re.compile(r"^(-?)(.+)$")
    _re_separator = re.compile(r",\s*")
    _re_subtitle_time = re.compile(r"(-?)\d(.{10})\d")

    def __init__(self, path, encoding, newline=None):
        """Initialize a :class:`SubStationAlpha` instance."""
        aeidon.SubtitleFile.__init__(self, path, encoding, newline)
        self.event_fields = (
            "Marked", "Start", "End", "Style", "Name",
            "MarginL", "MarginR", "MarginV", "Effect", "Text")

    def copy_from(self, other):
        """Copy generic properties from `other` file."""
        aeidon.SubtitleFile.copy_from(self, other)
        if self.format != other.format: return
        self.event_fields = tuple(other.event_fields)

    def _decode_field(self, field_name, value, subtitle):
        """Save string `value` from file as a subtitle attribute."""
        if field_name == "Marked":
            value = int(value.split("=")[-1])
            return setattr(subtitle.ssa, "marked", value)
        if field_name == "Start":
            value = self._re_file_time.sub(r"\1\060\2\060", value)
            return setattr(subtitle, "start_time", value)
        if field_name == "End":
            value = self._re_file_time.sub(r"\1\060\2\060", value)
            return setattr(subtitle, "end_time", value)
        if field_name == "Text":
            value = value.replace("\\n", "\n")
            value = value.replace("\\N", "\n")
            return setattr(subtitle, "main_text", value)
        if field_name in ("MarginL", "MarginR", "MarginV"):
            name = aeidon.util.title_to_lower_case(field_name)
            return setattr(subtitle.ssa, name, int(value))
        # Set plain string container attribute value.
        name = aeidon.util.title_to_lower_case(field_name)
        setattr(subtitle.ssa, name, value)

    def _encode_field(self, field_name, subtitle, doc):
        """Return value of field as string to be written to file."""
        if field_name == "Marked":
            return "Marked={:d}".format(subtitle.ssa.marked)
        if field_name == "Start":
            value = subtitle.calc.round(subtitle.start_time, 2)
            return self._re_subtitle_time.sub(r"\1\2", value)
        if field_name == "End":
            value = subtitle.calc.round(subtitle.end_time, 2)
            return self._re_subtitle_time.sub(r"\1\2", value)
        if field_name == "Text":
            value = subtitle.get_text(doc)
            return value.replace("\n", "\\N")
        if field_name in ("MarginL", "MarginR", "MarginV"):
            name = aeidon.util.title_to_lower_case(field_name)
            return "{:04d}".format(getattr(subtitle.ssa, name))
        # Return plain string container attribute value.
        name = aeidon.util.title_to_lower_case(field_name)
        return getattr(subtitle.ssa, name)

    def read(self):
        """
        Read file and return subtitles.

        Raise :exc:`IOError` if reading fails.
        Raise :exc:`UnicodeError` if decoding fails.
        """
        subtitles = []
        lines = self._read_lines()
        self._read_header(lines)
        for line in lines:
            if not line.startswith("Format:"): continue
            line = line.replace("Format:", "").strip()
            fields = self._re_separator.split(line)
            indices = dict((x, fields.index(x)) for x in fields)
            max_split = len(fields) - 1
        for line in lines:
            if not line.startswith("Dialogue:"): continue
            line = line.replace("Dialogue:", "").lstrip()
            values = self._re_separator.split(line, max_split)
            subtitle = self._get_subtitle()
            for name, index in indices.items():
                self._decode_field(name, values[index], subtitle)
            subtitles.append(subtitle)
        self.event_fields = tuple(fields)
        return subtitles

    def _read_header(self, lines):
        """Read header and remove its lines."""
        self.header = ""
        while not lines[0].startswith("[Events]"):
            self.header += "\n"
            self.header += lines.pop(0)
        self.header = self.header.strip()

    def write_to_file(self, subtitles, doc, f):
        """
        Write `subtitles` from `doc` to file `f`.

        Raise :exc:`IOError` if writing fails.
        Raise :exc:`UnicodeError` if encoding fails.
        """
        f.write(self.header + "\n\n")
        f.write("[Events]\n")
        fields = ", ".join(self.event_fields)
        f.write("Format: {}\n".format(fields))
        for subtitle in subtitles:
            f.write("Dialogue: {}\n".format(",".join([
                self._encode_field(x, subtitle, doc)
                for x in self.event_fields])))
