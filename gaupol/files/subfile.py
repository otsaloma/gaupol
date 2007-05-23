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
from gaupol.base import Contractual


class SubtitleFile(object):

    """Base class for subtitle files.

    Class or instance variables:
     * encoding: Character encoding
     * format: FORMAT constant
     * header: Header text
     * mode: MODE constant
     * newline: NEWLINE constant
     * path: Path to the file

    Depending on their mode, files handle data in either time or frame format.
    It is up to the caller to first check the class variable 'mode' before
    receiving read data or before sending data to write.

    If the file format contains a header, it will default to a template header
    read upon instantiation of the class, from paths.PROFILE_DIR/headers or
    paths.DATA_DIR/headers. If the read file has a header, it will replace the
    template.
    """

    __metaclass__ = Contractual
    format = None
    mode = None

    def __init__(self, path, encoding, newline=None):

        self.encoding = encoding
        self.header = ""
        self.newline = newline
        self.path = path

        if self.format.has_header:
            self.header = self.get_template_header()

    def _invariant(self):
        assert enclib.is_valid(self.encoding)

    def _read_lines_require(self):
        assert os.path.isfile(self.path)

    def _read_lines(self):
        """Read file to a unicoded list of lines.

        All newlines are converted to '\\n'.
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

    def copy_from(self, file):
        """Copy generic properties from file of same format."""

        self.header = file.header

    def get_template_header_require(self):
        assert self.format.has_header

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
        Return starts, ends, texts.
        """
        raise NotImplementedError

    def write_require(self, starts, ends, texts):
        assert self.newline is not None

    def write(self, starts, ends, texts):
        """Write file.

        Raise IOError if writing fails.
        Raise UnicodeError if encoding fails.
        """
        raise NotImplementedError
