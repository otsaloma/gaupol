# Copyright (C) 2006-2009 Osmo Salomaa
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

"""TMPlayer file."""

import aeidon

__all__ = ("TMPlayer",)


class TMPlayer(aeidon.SubtitleFile):

    """TMPlayer file."""

    format = aeidon.formats.TMPLAYER
    mode = aeidon.modes.TIME

    def read(self):
        """Read file and return subtitles.

        Raise :exc:`IOError` if reading fails.
        Raise :exc:`UnicodeError` if decoding fails.
        """
        subtitles = [self._get_subtitle()]
        for line in self._read_lines():
            i = (10 if line.startswith("-") else 9)
            if len(line.strip()) < i: continue
            subtitle = self._get_subtitle()
            subtitle.start = line[:i - 1] + ".000"
            subtitles[-1].end = subtitle.start_time
            subtitle.main_text = line[i:].replace("|", "\n")
            subtitles.append(subtitle)
        subtitles.pop(0)
        calc = subtitles[-1].calc
        time = subtitles[-1].start_time
        time = calc.add_seconds_to_time(time, 5)
        subtitles[-1].end = time
        return subtitles

    def write_to_file(self, subtitles, doc, fobj):
        """Write `subtitles` from `doc` to `fobj`.

        Raise :exc:`IOError` if writing fails.
        Raise :exc:`UnicodeError` if encoding fails.
        """
        for subtitle in subtitles:
            start = subtitle.calc.round_time(subtitle.start_time, 0)
            fobj.write("%s:" % start[:-4])
            fobj.write(subtitle.get_text(doc).replace("\n", "|"))
            fobj.write(self.newline.value)
