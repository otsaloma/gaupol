# Copyright (C) 2005-2007 Osmo Salomaa
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


"""Base class for subtitle files.

Module variables:

    _GLOBAL_HEADER_DIR: Directory path to global header templates
    _LOCAL_HEADER_DIR:  Directory path to local header templates
"""


import codecs
import os

from gaupol import cons, paths, util


_GLOBAL_HEADER_DIR = os.path.join(paths.DATA_DIR, "headers")
_LOCAL_HEADER_DIR = os.path.join(paths.PROFILE_DIR, "headers")


class SubtitleFile(object):

    """Base class for subtitle files.

    Class variables:

        format:     FORMAT constant
        has_header: True if file has a header
        identifier: Regular expression pattern, flags
        mode:       MODE constant

    Instance variables:

        encoding: Character encoding
        header:   Header string
        newline:  NEWLINE constant
        path:     Path to the file
    """

    format = None
    has_header = None
    identifier = None, None
    mode = None

    def __init__(self, path, encoding, newline=None):

        self.encoding = encoding
        self.header   = ""
        self.newline  = newline
        self.path     = path

        if self.has_header:
            self.header = self.get_template_header()

    def _read_lines(self):
        """Read file to a unicoded list of lines.

        All newlines are converted to '\\n'.
        All blank lines from the end are removed.
        Raise IOError if reading fails.
        Raise UnicodeError if decoding fails.
        Return a list of the lines.
        """
        fobj = codecs.open(self.path, "rU", self.encoding)
        try:
            lines = fobj.readlines()
            chars = fobj.newlines
        finally:
            fobj.close()
        while lines and lines[-1] == "\n":
            lines.pop(-1)
        if isinstance(chars, tuple):
            chars = chars[0]
        index = cons.NEWLINE.values.index(chars)
        self.newline = cons.NEWLINE.members[index]
        return lines

    def get_template_header(self):
        """Read and return the header from a template file."""

        # FIX: REWRITE WITHOUT EXCEPTIONAL.
        # @util.exceptional(IOError, util.handle_read_io, 0)
        # @util.exceptional(UnicodeError, util.handle_read_unicode, 0, 1)
        def read(path, encoding):
            return util.read(path, encoding)

        # pylint: disable-msg=E1101
        basename = self.format.name.lower() + ".txt"
        path = os.path.join(_LOCAL_HEADER_DIR, basename)
        if os.path.isfile(path):
            return read(path, None)
        path = os.path.join(_GLOBAL_HEADER_DIR, basename)
        if os.path.isfile(path):
            return read(path, "ascii")
        return ""

    def read(self):
        """Read file.

        Raise IOError if reading fails.
        Raise UnicodeError if decoding fails.
        Return shows, hides, texts.
        """
        raise NotImplementedError

    def write(self, shows, hides, texts):
        """Write file.

        Raise IOError if writing fails.
        Raise UnicodeError if encoding fails.
        """
        raise NotImplementedError
