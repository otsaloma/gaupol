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

"""Sub Station Alpha file."""

import gaupol
import re

__all__ = ("SubStationAlpha",)


class SubStationAlpha(gaupol.SubtitleFile):

    """Sub Station Alpha file."""

    _re_file_time = re.compile(r"^(-?)(.+)$")
    _re_separator = re.compile(r",\s*")
    _re_subtitle_time = re.compile(r"(-?)\d(.{10})\d")

    format = gaupol.formats.SSA
    mode = gaupol.modes.TIME

    def __init__(self, path, encoding, newline=None):

        gaupol.SubtitleFile.__init__(self, path, encoding, newline)
        self.event_fields = ("Marked", "Start", "End", "Style", "Name",
            "MarginL", "MarginR", "MarginV", "Effect", "Text",)

    def _decode_field(self, field_name, value, subtitle):
        """Save string value from file as a subtitle attribute."""

        if field_name == "Marked":
            value = value.split("=")[-1]
            return setattr(subtitle.ssa, "marked", int(value))
        if field_name == "Start":
            value = self._re_file_time.sub(r"\1\060\2\060", value)
            return setattr(subtitle, "start", value)
        if field_name == "End":
            value = self._re_file_time.sub(r"\1\060\2\060", value)
            return setattr(subtitle, "end", value)
        if field_name == "Text":
            value = value.replace("\\n", "\n")
            value = value.replace("\\N", "\n")
            return setattr(subtitle, "main_text", value)
        if field_name in ("MarginL", "MarginR", "MarginV"):
            name = gaupol.util.title_to_lower_case(field_name)
            return setattr(subtitle.ssa, name, int(value))
        # Set plain string container attribute value.
        name = gaupol.util.title_to_lower_case(field_name)
        setattr(subtitle.ssa, name, value)

    def _encode_field(self, field_name, subtitle, doc):
        """Return value of field as string to be written to file."""

        if field_name == "Marked":
            return "Marked=%d" % subtitle.ssa.marked
        if field_name == "Start":
            value = subtitle.calc.round_time(subtitle.start_time, 2)
            return self._re_subtitle_time.sub(r"\1\2", value)
        if field_name == "End":
            value = subtitle.calc.round_time(subtitle.end_time, 2)
            return self._re_subtitle_time.sub(r"\1\2", value)
        if field_name == "Text":
            value = subtitle.get_text(doc)
            return value.replace("\n", "\\n")
        if field_name in ("MarginL", "MarginR", "MarginV"):
            name = gaupol.util.title_to_lower_case(field_name)
            return "%04d" % getattr(subtitle.ssa, name)
        # Return plain string container attribute value.
        name = gaupol.util.title_to_lower_case(field_name)
        return getattr(subtitle.ssa, name)

    def _read_header(self, lines):
        """Read header and remove its lines."""

        self.header = ""
        while not lines[0].startswith("[Events]"):
            self.header += "\n"
            self.header += lines.pop(0)
        self.header = self.header.strip()

    def copy_from(self, other):
        """Copy generic properties from file of same format."""

        gaupol.SubtitleFile.copy_from(self, other)
        self.event_fields = tuple(other.event_fields)

    def read(self):
        """Read file and return subtitles.

        Raise IOError if reading fails.
        Raise UnicodeError if decoding fails.
        """
        subtitles = []
        lines = self._read_lines()
        self._read_header(lines)
        for line in (x for x in lines if x.startswith("Format:")):
            line = line.replace("Format:", "").strip()
            fields = self._re_separator.split(line)
            indices = dict((x, fields.index(x)) for x in fields)
            max_split = len(fields) - 1
        for line in (x for x in lines if x.startswith("Dialogue:")):
            subtitle = self._get_subtitle()
            line = line.replace("Dialogue:", "").lstrip()
            values = self._re_separator.split(line, max_split)
            for name, index in indices.items():
                self._decode_field(name, values[index], subtitle)
            subtitles.append(subtitle)
        self.event_fields = tuple(fields)
        return subtitles

    def write_to_file(self, subtitles, doc, fobj):
        """Write subtitles from document to given file.

        Raise IOError if writing fails.
        Raise UnicodeError if encoding fails.
        """
        encode = self._encode_field
        fields = self.event_fields
        fobj.write(self.header)
        fobj.write(self.newline.value * 2)
        fobj.write("[Events]")
        fobj.write(self.newline.value)
        fobj.write("Format: %s" % ", ".join(fields))
        fobj.write(self.newline.value)
        for subtitle in subtitles:
            values = [encode(x, subtitle, doc) for x in fields]
            fobj.write("Dialogue: %s" % ",".join(values))
            fobj.write(self.newline.value)
