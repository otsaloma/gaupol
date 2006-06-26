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

from gaupol.base               import cons
from gaupol.base.file          import SubtitleFile
from gaupol.base.position.calc import Calculator


class MPsub(SubtitleFile):

    """MPsub file."""

    format     = cons.Format.MPSUB
    framerate  = None
    has_header = True
    identifier = r'^FORMAT=(TIME|[\d\.]+)\s*$', 0
    mode       = cons.Mode.TIME

    def _get_mpsub_frames(self, shows, hides):
        """
        Get MPsub style frames.

        Return shows, hides.
        """
        shows = shows[:]
        hides = hides[:]
        for i in reversed(range(len(shows))):
            hides[i] = str(hides[i] - shows[i])
            if i > 0:
                shows[i] = str(shows[i] - hides[i - 1])

        return shows, hides

    def _get_mpsub_times(self, shows, hides):
        """Get MPsub style times."""

        calc = Calculator()
        shows = list(calc.time_to_seconds(x) for x in shows)
        hides = list(calc.time_to_seconds(x) for x in hides)
        for i in reversed(range(len(shows))):
            hides[i] -= shows[i]
            if i > 0:
                shows[i] -= hides[i - 1]

        # Avoid cumulation of rounding errors.
        bank = 0
        for i in range(len(shows)):
            orig_show = shows[i]
            shows[i] = round(shows[i] - bank, 2)
            bank = bank + shows[i] - orig_show
            orig_hide = hides[i]
            hides[i] = round(hides[i] - bank, 2)
            bank = bank + hides[i] - orig_hide

        shows = list('%.2f' % x for x in shows)
        hides = list('%.2f' % x for x in hides)

        return shows, hides

    def read(self):
        """
        Read file.

        Raise IOError if reading fails.
        Raise UnicodeError if decoding fails.
        Raise ValueError if bad FORMAT line.
        Return shows, hides, texts.
        """
        re_time_line = re.compile(r'^([\d\.]+) ([\d\.]+)\s*$')
        calc = Calculator()

        shows  = []
        hides  = []
        texts  = []
        header = ''
        header_read = False
        lines = self._read_lines()
        for line in lines:
            if not line.strip():
                continue
            match = re_time_line.match(line)
            if match is not None:
                header_read = True
                try:
                    shows.append(hides[-1] + float(match.group(1)))
                except IndexError:
                    shows.append(float(match.group(1)))
                hides.append(shows[-1] + float(match.group(2)))
                texts.append(u'')
            elif header_read:
                texts[-1] += line
            else:
                header += line
        if header:
            self.set_header(header.strip())

        if self.mode == cons.Mode.TIME:
            shows = list(calc.seconds_to_time(x) for x in shows)
            hides = list(calc.seconds_to_time(x) for x in hides)
        elif self.mode == cons.Mode.FRAME:
            shows = list(int(round(x, 0)) for x in shows)
            hides = list(int(round(x, 0)) for x in hides)
        texts = list(x.strip() for x in texts)

        return shows, hides, texts

    def set_header(self, header):
        """
        Parse and set header and mode.

        Raise ValueError if bad FORMAT line.
        """
        mode = None
        for line in header.split('\n'):
            if line.startswith('FORMAT='):
                mode = line[7:].strip()
                break

        if mode == 'TIME':
            self.framerate = None
            self.mode = cons.Mode.TIME
            self.header = header
            return
        if mode in cons.Framerate.mpsub_names:
            self.framerate = cons.Framerate.mpsub_names.index(mode)
            self.mode = cons.Mode.FRAME
            self.header = header
            return
        raise ValueError

    def write(self, shows, hides, texts):
        """
        Write file.

        Raise IOError if writing fails.
        Raise UnicodeError if encoding fails.
        """
        newline_char = self._get_newline_character()

        if self.mode == cons.Mode.TIME:
            shows, hides = self._get_mpsub_times(shows, hides)
        elif self.mode == cons.Mode.FRAME:
            shows, hides = self._get_mpsub_frames(shows, hides)
        texts = list(x.replace('\n', newline_char) for x in texts)

        fobj = codecs.open(self.path, 'w', self.encoding)
        try:
            fobj.write(self.header + newline_char * 2)
            for i in range(len(shows)):
                fobj.write('%s %s%s%s%s%s' % (
                    shows[i], hides[i], newline_char,
                    texts[i], newline_char,
                    newline_char
                ))
        finally:
            fobj.close()
