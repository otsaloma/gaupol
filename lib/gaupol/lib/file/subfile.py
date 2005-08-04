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


NEWLINES = {
    '\n'  : 'Unix',
    '\r'  : 'Mac',
    '\r\n': 'Windows',
}


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
        """
        Get character used for newlines.

        Raise ValueError if self.newlines doesn't have a proper value.
        """
        for char, oper_syst in NEWLINES.items():
            if self.newlines == oper_syst:
                return char
        
        raise ValueError('Invalid newline class: "%s".' % self.newlines)

    def _read_lines(self):
        """
        Read subtitle file to a unicoded list containing lines of the file.
        
        Raise IOError if reading fails.
        Raise UnicodeError if decoding fails.
        """
        sub_file = codecs.open(self.path, 'rU', self.encoding)

        try:
            lines = sub_file.readlines()
            newline_chars = sub_file.newlines
        finally:
            sub_file.close()

        if isinstance(newline_chars, tuple):
            self.newlines = NEWLINES[newline_chars[0]]
        elif isinstance(newline_chars, basestring):
            self.newlines = NEWLINES[newline_chars]
            
        return lines

    def _strip_spaces(self, strings):
        """Strip leading and trailing spaces in list of strings."""
        
        for i in range(len(strings)):
            strings[i] = strings[i].strip()

        return strings
