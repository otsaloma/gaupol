# -*- coding: utf-8 -*-

# Copyright (C) 2017 Osmo Salomaa
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

"""WebVTT file."""

import aeidon
import re

__all__ = ("WebVTT",)


class WebVTT(aeidon.SubtitleFile):

    """
    WebVTT file.

    https://developer.mozilla.org/en-US/docs/Web/API/WebVTT_API
    """

    format = aeidon.formats.WEBVTT
    mode = aeidon.modes.TIME

    _re_comment = re.compile(r"^\s*NOTE\b")
    _re_style = re.compile(r"^\s*STYLE\b")
    _re_time_line = re.compile((
        # Techically all these fields should have fixed widths, but in the
        # name of being liberal in accepting input, accept lesser widths
        # assuming that they are just lacking zero-padding from the side
        # that is farther from the decimal point.
        r"^(-?(?:\d{1,2}:)?\d{1,2}:\d{1,2}\.\d{1,3}) -->"
        r" (-?(?:\d{1,2}:)?\d{1,2}:\d{1,2}\.\d{1,3})"
        r"(\s+.+)?\s*$"))

    def read(self):
        """
        Read file and return subtitles.

        Raise :exc:`IOError` if reading fails.
        Raise :exc:`UnicodeError` if decoding fails.
        """
        subtitles = []
        current = "header"
        self.header = ""
        lines = list(self._read_lines()) + [""]
        for i, line in enumerate(lines):
            if not line.strip():
                # A blank line terminates the preceding block.
                if current in ("header", "text"):
                    subtitles.append(self._get_subtitle())
                current = None
            elif current == "header":
                # Header should be one line, but allow a block.
                if self.header:
                    self.header += "\n"
                self.header += line
            elif (self._re_style.match(line) or
                  current == "style"):
                # Bind CSS styles to following subtitle.
                subtitle = subtitles[-1]
                if subtitle.webvtt.style:
                    subtitle.webvtt.style += "\n"
                subtitle.webvtt.style += line
                current = "style"
            elif (self._re_comment.match(line) or
                  current == "comment"):
                # Bind comments to following subtitle.
                subtitle = subtitles[-1]
                if subtitle.webvtt.comment:
                    subtitle.webvtt.comment += "\n"
                subtitle.webvtt.comment += line
                current = "comment"
            elif self._re_time_line.match(line):
                # Time lines form a block with an optional preceding
                # cue identifier and following text.
                subtitle = subtitles[-1]
                if lines[i-1].strip():
                    subtitle.webvtt.id = lines[i-1]
                match = self._re_time_line.match(line)
                normalize = subtitle.calc.normalize_time
                subtitle.start_time = normalize(match.group(1))
                subtitle.end_time = normalize(match.group(2))
                subtitle.webvtt.settings = match.group(3) or ""
                current = "text"
            elif current == "text":
                # Append inividual lines to text block.
                subtitle = subtitles[-1]
                if subtitle.main_text:
                    subtitle.main_text += "\n"
                subtitle.main_text += line
        # The last blank line has opened a new subtitle without times or text,
        # which we skip. This also means that any possible styles or comments
        # after the last actual subtitle are thrown out as well.
        return subtitles[:-1]

    def write_to_file(self, subtitles, doc, f):
        """
        Write `subtitles` from `doc` to file `f`.

        Raise :exc:`IOError` if writing fails.
        Raise :exc:`UnicodeError` if encoding fails.
        """
        writen = lambda x: f.write(x + "\n")
        nwriten = lambda x: f.write("\n" + x + "\n")
        writen(self.header.strip() or "WEBVTT")
        first = 3 if subtitles[-1].end_seconds < 3600 else 0
        for i, subtitle in enumerate(subtitles):
            if subtitle.webvtt.style:
                nwriten(subtitle.webvtt.style)
            if subtitle.webvtt.comment:
                nwriten(subtitle.webvtt.comment)
            f.write("\n")
            if subtitle.webvtt.id:
                writen(subtitle.webvtt.id)
            # Write times as MM:SS.SSS if all times are less
            # than an hour, else the usual HH:MM:SS.SSS.
            start = subtitle.start_time[first:]
            end = subtitle.end_time[first:]
            f.write("{} --> {}".format(start, end))
            if subtitle.webvtt.settings:
                f.write(" {}".format(subtitle.webvtt.settings.strip()))
            f.write("\n{}\n".format(subtitle.get_text(doc)))
