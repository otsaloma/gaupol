# -*- coding: utf-8 -*-

# Copyright (C) 2005 Osmo Salomaa
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""Base class for subtitle files."""

import aeidon
import codecs
import os
import re

__all__ = ("SubtitleFile",)


class SubtitleFile:

    """
    Base class for subtitle files.

    :cvar format: :attr:`aeidon.formats` item corresponding to file format
    :cvar mode: :attr:`aeidon.modes` item corresponding to native positions
    :ivar encoding: Character encoding used to read and write file
    :ivar has_utf_16_bom: True if BOM found for UTF-16-BE or UTF-16-LE
    :ivar header: String of metadata at the top of the file
    :ivar newline: :attr:`aeidon.newlines` item, detected upon read
    :ivar path: Full, absolute path to the file on disk

    If the file format contains a header, it will default to a fairly blank
    template header read upon instantiation of the class, from either
    ``aeidon.DATA_DIR/headers`` or ``aeidon.DATA_HOME_DIR/headers``. If the
    read file contains a header, it will replace the template.
    """
    format = aeidon.formats.NONE
    mode = aeidon.modes.NONE

    def __init__(self, path, encoding, newline=None):
        """Initialize a :class:`SubtitleFile` instance."""
        self.encoding = encoding
        self.has_utf_16_bom = False
        self.header = (aeidon.util.get_template_header(self.format)
                       if self.format.has_header else "")

        self.newline = newline or aeidon.util.get_default_newline()
        self.path = os.path.abspath(path)

    def copy_from(self, other):
        """Copy generic properties from `other`."""
        self.has_utf_16_bom = other.has_utf_16_bom
        if self.format != other.format: return
        self.header = other.header

    def _get_subtitle(self):
        """Return a new subtitle instance with proper properties."""
        return aeidon.Subtitle(self.mode)

    def read(self):
        """
        Read file and return subtitles.

        Raise :exc:`IOError` if reading fails.
        Raise :exc:`UnicodeError` if decoding fails.
        """
        raise NotImplementedError

    def _read_lines(self):
        """
        Read file to a list of lines.

        All newlines are stripped.
        All blank lines from beginning and end are removed.
        Raise :exc:`IOError` if reading fails.
        Raise :exc:`UnicodeError` if decoding fails.
        Return a list of lines read.
        """
        re_newline_char = re.compile(r"\r?\n?$")
        with open(self.path, "r", encoding=self.encoding) as f:
            lines = f.readlines()
            lines = [re_newline_char.sub("", x) for x in lines]
        for index in (0, -1):
            while lines and not lines[index].strip():
                lines.pop(index)
        newline = aeidon.util.detect_newlines(self.path)
        if newline is not None:
            self.newline = newline
        if self.encoding == "utf_8":
            bom = str(codecs.BOM_UTF8, "utf_8")
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
            bom = str(codecs.BOM_UTF16_BE, "utf_16_be")
            if lines and lines[0].startswith(bom):
                self.has_utf_16_bom = True
                lines[0] = lines[0].replace(bom, "")
            # Handle erroneous (?) UTF-16 encoded subtitles that use
            # NULL-character filled linebreaks '\x00\r\x00\n', which
            # readlines interprets as two separate linebreaks.
            if not any(lines[i] for i in range(1, len(lines), 2)):
                lines = [lines[i] for i in range(0, len(lines), 2)]
        return lines

    def write(self, subtitles, doc):
        """
        Write `subtitles` with text from `doc` to file.

        Raise :exc:`IOError` if writing fails.
        Raise :exc:`UnicodeError` if encoding fails.
        """
        with aeidon.util.atomic_open(self.path,
                                     mode="w",
                                     encoding=self.encoding,
                                     newline=self.newline.value) as f:

            # UTF-8-SIG automatically adds the UTF-8 signature BOM. Likewise,
            # UTF-16 automatically adds the system default BOM, but
            # UTF-16-BE and UTF-16-LE don't. For the latter two, add the BOM,
            # if it was originally read in the file.
            if self.has_utf_16_bom and self.encoding == "utf_16_be":
                f.write(str(codecs.BOM_UTF16_BE, "utf_16_be"))
            if self.has_utf_16_bom and self.encoding == "utf_16_le":
                f.write(str(codecs.BOM_UTF16_LE, "utf_16_le"))
            self.write_to_file(subtitles, doc, f)

    def write_to_file(self, subtitles, doc, f):
        """
        Write `subtitles` with text from `doc` to file `f`.

        Raise :exc:`IOError` if writing fails.
        Raise :exc:`UnicodeError` if encoding fails.
        """
        raise NotImplementedError
