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


"""Base class for subtitle files."""


from __future__ import with_statement

import codecs
import contextlib
import os

from gaupol import const, enclib, paths, util


class SubtitleFile(object):

    """Base class for subtitle files.

    Class variables:

        format:     FORMAT constant
        has_header: True if file has a header
        identifier: Regular expression object
        mode:       MODE constant

    Instance variables:

        encoding: Character encoding
        header:   Header text
        newline:  NEWLINE constant
        path:     Path to the file

    Depending on their mode, files handle data in either time or frame format.
    It is up to the caller to first check the class variable 'mode' before
    receiving read data or before sending data to write.

    If the file format contains a header, it will default to a template header
    read upon instantiation of the class, from path.PROFILE_DIR/headers or
    paths.DATA_DIR/headers. If the read file has a header, it will replace the
    template.
    """

    format = None
    has_header = None
    identifier = None
    mode = None

    def __init__(self, path, encoding, newline=None):

        self.path = path
        self.encoding = encoding
        self.newline = newline
        self.header = (self.get_template_header() if self.has_header else "")

    def __setattr___require(self, name, value):
        if name == "encoding":
            assert enclib.is_valid(value)

    @util.contractual
    def __setattr__(self, name, value):

        return object.__setattr__(self, name, value)

    def _read_lines_require(self):
        assert os.path.isfile(self.path)

    @util.contractual
    def _read_lines(self):
        """Read file to a unicoded list of lines.

        All newlines are converted to '\n'.
        All blank lines from the end are removed.
        Raise IOError if reading fails.
        Raise UnicodeError if decoding fails.
        Return a list of the lines.
        """
        args = (self.path, "rU", self.encoding)
        with contextlib.closing(codecs.open(*args)) as fobj:
            lines = fobj.readlines()
            chars = fobj.newlines
        while lines and lines[-1] == "\n":
            lines.pop()
        if isinstance(chars, tuple):
            chars = chars[0]
        index = const.NEWLINE.values.index(chars)
        self.newline = const.NEWLINE.members[index]
        return lines

    def get_template_header_require(self):
        assert self.has_header

    @util.contractual
    def get_template_header(self):
        """Read and return the header from a template file."""

        basename = self.format.name.lower() + ".txt"
        read = util.silent(IOError, UnicodeError)(util.read)
        directory = os.path.join(paths.PROFILE_DIR, "headers")
        path = os.path.join(directory, basename)
        if os.path.isfile(path):
            return read(path, None)
        directory = os.path.join(paths.DATA_DIR, "headers")
        path = os.path.join(directory, basename)
        return read(path, "ascii")

    def read(self):
        """Read file.

        Raise IOError if reading fails.
        Raise UnicodeError if decoding fails.
        Return shows, hides, texts.
        """
        raise NotImplementedError

    def write_require(self, shows, hides, texts):
        assert self.newline is not None

    @util.contractual
    def write(self, shows, hides, texts):
        """Write file.

        Raise IOError if writing fails.
        Raise UnicodeError if encoding fails.
        """
        raise NotImplementedError
