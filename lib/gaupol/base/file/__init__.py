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


"""Base class for subtitle file classes."""


import codecs

from gaupol.base.cons import Newlines


class SubtitleFile(object):

    """Base class for subtitle file classes."""

    format          = None
    mode            = None
    has_header      = None
    header_template = None
    identifier      = None, None

    def __init__(self, path, encoding, newlines=None):

        self.path     = path
        self.encoding = encoding
        self.newlines = newlines
        self.header   = self.header_template

    def __setattr__(self, name, value):
        """Set value of attribute"""

        if name in (
            'format',
            'mode',
            'has_header',
            'header_template'
            'identifier'
        ):
            raise ValueError

        object.__setattr__(self, name, value)

    def _get_newline_character(self):
        """Get character(s) used for newlines."""

        return Newlines.values[self.newlines]

    def read(self):
        """Read file."""

        raise NotImplementedError

    def _read_lines(self):
        """
        Read file to a unicoded list of lines.

        Raise IOError if reading fails.
        Raise UnicodeError if decoding fails.
        """
        fobj = codecs.open(self.path, 'rU', self.encoding)
        try:
            lines = fobj.readlines()
            newline_chars = fobj.newlines
        finally:
            fobj.close()

        if isinstance(newline_chars, tuple):
            self.newlines = Newlines.values.index(newline_chars[0])
        elif isinstance(newline_chars, basestring):
            self.newlines = Newlines.values.index(newline_chars)

        return lines

    def write(self, shows, hides, texts):
        """Write file."""

        raise NotImplementedError
