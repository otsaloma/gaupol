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


"""Base class for subtitle files."""


try:
    from psyco.classes import *
except ImportError:
    pass

import codecs

from gaupol.constants import Newlines


class SubtitleFile(object):

    """Base class for subtitle files."""

    FORMAT     = None
    HAS_HEADER = None
    MODE       = None

    # Regular expression that is used to identify this file format.
    # Pattern, flags
    id_pattern = None, None

    HEADER_TEMPLATE = None

    def __init__(self, path, encoding, newlines=None):
        """
        Initialize a SubtitleFile object.

        newlines can be omitted if creating an instance only for reading.
        """
        self.path     = path
        self.encoding = encoding
        self.newlines = newlines
        self.header   = ''

        self.format     = self.__class__.FORMAT
        self.has_header = self.__class__.HAS_HEADER
        self.mode       = self.__class__.MODE

    def _get_newline_character(self):
        """Get character(s) used for newlines."""

        return Newlines.values[self.newlines]

    def read(self):
        """Read file."""

        raise NotImplementedError

    def _read_lines(self):
        """
        Read subtitle file to a unicoded list containing the lines of the file.

        Raise IOError if reading fails.
        Raise UnicodeError if decoding fails.
        """
        subtitle_file = codecs.open(self.path, 'rU', self.encoding)

        # Read.
        try:
            lines = subtitle_file.readlines()
            newline_characters = subtitle_file.newlines
        finally:
            subtitle_file.close()

        # Save newline format.
        if isinstance(newline_characters, tuple):
            self.newlines = Newlines.values.index(newline_characters[0])
        elif isinstance(newline_characters, basestring):
            self.newlines = Newlines.values.index(newline_characters)

        return lines

    def write(self, shows, hides, texts):
        """Write file."""

        raise NotImplementedError
