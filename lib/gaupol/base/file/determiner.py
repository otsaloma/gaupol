# Copyright (C) 2005-2006 Osmo Salomaa
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


"""Subtitle file format determiner."""


import re

from gaupol.base              import cons
from gaupol.base.error        import FileFormatError
from gaupol.base.file         import SubtitleFile
from gaupol.base.file.classes import *


class FileFormatDeterminer(SubtitleFile):

    """Subtitle file format determiner."""

    def determine(self):
        """
        Determine the file format.

        Raise IOError if reading fails.
        Raise UnicodeError if decoding fails.
        Raise FileFormatError if unable to detect file format.
        """
        re_ids = []
        for format, name in enumerate(cons.Format.class_names):
            re_id = re.compile(*eval(name).identifier)
            re_ids.append((format, re_id))

        lines = self._read_lines()
        for line in lines:
            for format, re_id in re_ids:
                if re_id.search(line) is not None:
                    return format

        raise FileFormatError
