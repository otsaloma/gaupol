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
import sys

__all__ = ("SubtitleFile",)


class SubtitleFile(object):

    """Base class for subtitle files.

    Class or instance variables:
     * encoding: Character encoding used to read and write file
     * format: Format enumeration corresponding to file
     * has_utf_16_bom: True if BOM found for UTF-16-BE or UTF-16-LE
     * header: String of generic information at the top of the file
     * mode: Mode enumeration corresponding to the native positions
     * newline: Newline enumeration, detected upon read and written as such
     * path: Full, absolute path to the file on disk

    If the file format contains a header, it will default to a fairly blank
    template header read upon instantiation of the class, from either
    paths.DATA_DIR/headers or paths.DATA_HOME_DIR/headers. If the read file
    contains a header, it will replace the template.
    """

    __metaclass__ = gaupol.Contractual
    format = gaupol.formats.NONE
    mode = gaupol.modes.NONE

    def __init__(self, path, encoding, newline=None):
        """Initialize a SubtitleFile object."""

        self.encoding = encoding
        self.has_utf_16_bom = False
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
        decode = lambda x: x.decode(self.encoding)
        with contextlib.closing(open(self.path, "rU")) as fobj:
            lines = map(decode, fobj.readlines())
            chars = fobj.newlines
            assert chars is not None
        lines = [x[:-1] if x.endswith("\n") else x for x in lines]
        for index in (0, -1):
            while lines and (not lines[index].strip()):
                lines.pop(index)
        if isinstance(chars, tuple):
            chars = chars[0]
        self.newline = gaupol.newlines.find_item("value", chars)
        if self.encoding == "utf_8":
            bom = unicode(codecs.BOM_UTF8, "utf_8")
            if lines and lines[0].startswith(bom):
                # If a UTF-8 BOM (a.k.a. signature) is found, reread file with
                # UTF-8-SIG encoding, which automatically strips the BOM when
                # reading and adds it when writing.
                self.encoding = "utf_8_sig"
                return SubtitleFile._read_lines(self)
        if self.encoding.startswith("utf_16"):
            # Python automatically strips the UTF-16 BOM when reading, but only
            # when using UTF-16. If using UTF-16-BE or UTF-16-LE, the BOM is
            # kept at the beginning of the first line. It is read correctly, so
            # it should FE FF for both BE and LE.
            bom = unicode(codecs.BOM_UTF16_BE, "utf_16_be")
            if lines and lines[0].startswith(bom):
                self.has_utf_16_bom = True
                lines[0] = lines[0].replace(bom, "")
            # Handle erroneous (?) UTF-16 encoded subtitles that use
            # NULL-character filled linebreaks '\x00\r\x00\n', which
            # readlines interprets as two separate linebreaks.
            if not any(lines[i] for i in range(1, len(lines), 2)):
                lines = [lines[i] for i in range(0, len(lines), 2)]
        return lines

    def copy_from_require(self, other):
        assert isinstance(other, SubtitleFile)

    def copy_from(self, other):
        """Copy generic properties from other file."""

        if self.format == other.format:
            self.header = other.header
        self.has_utf_16_bom = other.has_utf_16_bom

    def get_template_header_require(self):
        assert self.format.has_header

    def get_template_header(self):
        """Read and return the header from a template file.

        Raise IOError if reading global header file fails.
        Raise UnicodeError if decoding global header file fails.
        """
        basename = self.format.name.lower()
        directory = os.path.join(gaupol.DATA_HOME_DIR, "headers")
        path = os.path.join(directory, basename)
        if os.path.isfile(path):
            try: return gaupol.util.read(path, None)
            except (IOError, UnicodeError):
                gaupol.util.print_read_io(sys.exc_info(), path)
        directory = os.path.join(gaupol.DATA_DIR, "headers")
        path = os.path.join(directory, basename)
        return gaupol.util.read(path, "ascii")

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
            # UTF-8-SIG automatically adds the UTF-8 signature BOM. Likewise,
            # UTF-16 automatically adds the system default BOM, but
            # UTF-16-BE and UTF-16-LE don't. For the latter two, add the BOM,
            # if it was originally read in the file.
            if self.has_utf_16_bom and (self.encoding == "utf_16_be"):
                fobj.write(unicode(codecs.BOM_UTF16_BE, "utf_16_be"))
            if self.has_utf_16_bom and (self.encoding == "utf_16_le"):
                fobj.write(unicode(codecs.BOM_UTF16_LE, "utf_16_le"))
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
