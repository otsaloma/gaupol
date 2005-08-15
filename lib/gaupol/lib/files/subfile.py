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


import codecs

try:
    from psyco.classes import *
except ImportError:
    pass


from gaupol.constants import NEWLINE


class SubtitleFile(object):
    
    """
    Base class for subtitle files.
    
    encoding: Python name of encoding used
    newlines: "Mac", "Unix" or "Windows"
    """
    
    def __init__(self, path, encoding, newlines=None):
        """
        Initialize a SubtitleFile object.
        
        newlines can be omitted if creating a file object only for reading.
        """
        self.path     = path
        self.encoding = encoding
        self.newlines = newlines

        self.FORMAT    = None
        self.EXTENSION = None
        self.MODE      = None

    def _get_newline_character(self):
        """Get character used for newlines."""
        
        return NEWLINE.VALUES[self.newlines]

    def _read_lines(self):
        """
        Read subtitle file to a unicoded list containing lines of the file.
        
        Raise IOError if reading fails.
        Raise UnicodeError if decoding fails.
        """
        subtitle_file = codecs.open(self.path, 'rU', self.encoding)

        try:
            lines = subtitle_file.readlines()
            newline_characters = subtitle_file.newlines
        finally:
            subtitle_file.close()

        if isinstance(newline_characters, tuple):
            self.newlines = NEWLINE.VALUES.index(newline_characters[0])
        elif isinstance(newline_characters, basestring):
            self.newlines = NEWLINE.VALUES.index(newline_characters)
            
        return lines

    def _strip_spaces(self, strings):
        """Strip leading and trailing spaces in list of strings."""

        return [string.strip() for string in strings]
