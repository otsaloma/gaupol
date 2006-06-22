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


"""Subtitle files."""


import codecs
import os

from gaupol.base       import cons
from gaupol.base.paths import DATA_DIR, PROFILE_DIR
from gaupol.base.util  import enclib, filelib


_GLOBAL_HEADER_DIR = os.path.join(DATA_DIR   , 'headers')
_LOCAL_HEADER_DIR  = os.path.join(PROFILE_DIR, 'headers')


class SubtitleFile(object):

    """
    Base class for subtitle file classes.

    Class variables:

        format:     Format constant
        has_header: True if file has a header
        identifier: Regular expression pattern, flags
        mode:       Mode constant

    Instance variables:

        encoding: String
        header:   String
        newlines: Newlines constant
        path:     File path

    """

    format     = None
    has_header = None
    identifier = None, None
    mode       = None

    def __init__(self, path, encoding, newlines=None):

        self.encoding = encoding
        self.header   = ''
        self.newlines = newlines
        self.path     = path

        if self.has_header:
            self.header = self.get_template_header()

    def __setattr__(self, name, value):

        if name in ('format', 'has_header', 'identifier', 'mode'):
            raise ValueError
        object.__setattr__(self, name, value)

    def _get_newline_character(self):
        """Get character(s) used for newlines."""

        return cons.Newlines.values[self.newlines]

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
            self.newlines = cons.Newlines.values.index(newline_chars[0])
        elif isinstance(newline_chars, basestring):
            self.newlines = cons.Newlines.values.index(newline_chars)

        return lines

    def read(self):
        """Read file."""

        raise NotImplementedError

    def get_template_header(self):
        """Read and return header from template file."""

        basename = cons.Format.get_name(self.format).lower() + '.txt'

        try:
            encoding = enclib.get_locale_encoding()[0]
        except ValueError:
            encoding = 'utf_8'
        path = os.path.join(_LOCAL_HEADER_DIR, basename)
        if os.path.isfile(path):
            try:
                return filelib.read(path, encoding)
            except (IOError, UnicodeError):
                pass

        path = os.path.join(_GLOBAL_HEADER_DIR, basename)
        try:
            return filelib.read(path, 'utf_8')
        except (IOError, UnicodeError):
            pass

        return ''

    def write(self, shows, hides, texts):
        """Write file."""

        raise NotImplementedError
