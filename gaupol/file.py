# Copyright (C) 2005-2008 Osmo Salomaa
#
# This file is part of Gaupol.
#
# Gaupol is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# Gaupol is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# Gaupol. If not, see <http://www.gnu.org/licenses/>.

"""Base class for subtitle files."""

from __future__ import with_statement

import codecs
import contextlib
import gaupol
import os

__all__ = ("SubtitleFile",)


class SubtitleFile(object):

    """Base class for subtitle files.

    Class or instance variables:
     * encoding: Character encoding used to read and write file
     * format: Format enumeration corresponding to file
     * has_bom_utf8: True if an UTF-8 BOM was read
     * header: String of generic information at the top of the file
     * mode: Mode enumeration corresponding to the native positions
     * newline: Newline enumeration, detected upon read and written as such
     * path: Full, absolute path to the file on disk

    If the file format contains a header, it will default to a fairly blank
    template header read upon instantiation of the class, from either
    paths.PROFILE_DIR/headers or paths.DATA_DIR/headers. If the read file
    contains a header, it will replace the template.
    """

    __metaclass__ = gaupol.Contractual
    format = gaupol.formats.NONE
    mode = gaupol.modes.NONE

    def __init__(self, path, encoding, newline=None):

        self.encoding = encoding
        self.has_bom_utf8 = False
        self.header = ""
        self.newline = newline
        self.path = os.path.abspath(path)

        if self.format.has_header:
            self.header = self.get_template_header()

    def _get_subtitle(self):
        """Return a new subtitle instance with proper properties."""

        return gaupol.Subtitle(self.mode)

    def _invariant(self):
        assert gaupol.encodings.is_valid_code(self.encoding)

    def _read_lines(self):
        """Read file to a unicoded list of lines.

        All newlines are stripped.
        All blank lines from beginning and end are removed.
        Raise IOError if reading fails.
        Raise UnicodeError if decoding fails.
        Return a list of the lines.
        """
        args = (self.path, "rU", self.encoding)
        with contextlib.closing(codecs.open(*args)) as fobj:
            lines = fobj.readlines()
            chars = fobj.newlines
        lines = [x[:-1] if x.endswith("\n") else x for x in lines]
        for index in (0, -1):
            while lines and (not lines[index].strip()):
                lines.pop(index)
        if isinstance(chars, tuple):
            chars = chars[0]
        self.newline = gaupol.newlines.find_item("value", chars)
        if lines and lines[0].startswith(codecs.BOM_UTF8):
            self.has_bom_utf8 = True
            lines[0] = lines[0].replace(codecs.BOM_UTF8, "")
        return lines

    def copy_from_require(self, other):
        assert isinstance(other, self.__class__)

    def copy_from(self, other):
        """Copy generic properties from file of same format."""

        self.has_bom_utf8 = other.has_bom_utf8
        self.header = other.header

    def get_template_header_require(self):
        assert self.format.has_header

    def get_template_header(self):
        """Read and return the header from a template file."""

        basename = self.format.name.lower()
        read = gaupol.deco.silent(IOError, UnicodeError)(gaupol.util.read)
        directory = os.path.join(gaupol.PROFILE_DIR, "headers")
        path = os.path.join(directory, basename)
        if os.path.isfile(path):
            return read(path, None)
        directory = os.path.join(gaupol.DATA_DIR, "headers")
        path = os.path.join(directory, basename)
        return read(path, "ascii")

    def read(self):
        """Read file and return subtitles.

        Raise IOError if reading fails.
        Raise UnicodeError if decoding fails.
        """
        raise NotImplementedError

    def write_require(self, subtitles, doc):
        assert self.newline is not None

    def write(self, subtitles, doc):
        """Write subtitles from document to file.

        Raise IOError if writing fails.
        Raise UnicodeError if encoding fails.
        """
        args = (self.path, "w", self.encoding)
        with contextlib.closing(codecs.open(*args)) as fobj:
            if (self.encoding == "utf_8") and self.has_bom_utf8:
                fobj.write(codecs.BOM_UTF8)
            self.write_to_file(subtitles, doc, fobj)

    def write_to_file_require(self, subtitles, doc, fobj):
        assert hasattr(fobj, "write")
        assert self.newline is not None

    def write_to_file(self, subtitles, doc, fobj):
        """Write subtitles from document to given file.

        Raise IOError if writing fails.
        Raise UnicodeError if encoding fails.
        """
        raise NotImplementedError
