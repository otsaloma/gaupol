# Copyright (C) 2005 Osmo Salomaa
#
# This file is part of Gaupol.
#
# Gaupol is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Gaupol is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Gaupol; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA


"""Subtitle file format determiner."""


import re

try:
    from psyco.classes import *
except ImportError:
    pass

from gaupol.constants import FORMAT
from gaupol.base.files.classes import *
from gaupol.base.files.subfile import SubtitleFile


class FileFormatDeterminer(SubtitleFile):
    
    """Subtitle file format determiner."""
    
    def determine_file_format(self):
        """
        Determine the file format.
        
        Read file and once an identifier assiciated with a specific subtitle
        format is found, return that format.

        Raise IOError if reading fails.
        Raise UnicodeError if decoding fails.
        Raise UnknownFileFormatError if unable to detect file format.
        """
        lines = self._read_lines()

        # Assemble a list of regular expressions.
        re_ids = []
        for format in range(len(FORMAT.NAMES)):
            pattern = eval(FORMAT.NAMES[format]).ID_PATTERN
            try:
                re_id = re.compile(pattern[0], pattern[1])
            except TypeError:
                re_id = re.compile(pattern[0])
            re_ids.append((format, re_id))

        # Find correct format.
        for line in lines:
            for format, re_id in re_ids:
                if re_id.search(line) is not None:
                    return format
            
        raise FileFormatError(_('Unrecognized subtitle file format'))

        
class FileFormatError(Exception):
    
    """Bad subtitle file format."""
    
    pass
