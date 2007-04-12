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


"""Subtitle file format determiner."""


from __future__ import with_statement

import codecs
import contextlib
import os

from gaupol import const, enclib, util
from gaupol.errors import FormatError
from gaupol.files import *


class FormatDeterminer(object):

    """Subtitle file format determiner.

    Instance variables:

        _re_ids:  List of tuples of format, regular expression
        encoding: Character encoding to open the file with
        path:     Path to the file
    """

    def __init___require(self, path, encoding):
        assert os.path.isfile(path)
        assert enclib.is_valid(encoding)

    @util.contractual
    def __init__(self, path, encoding):

        self._re_ids = []
        self.encoding = encoding
        self.path = path

        for format in const.FORMAT.members:
            re_id = eval(format.class_name).identifier
            self._re_ids.append((format, re_id))

    def determine_ensure(self, value):
        assert value in const.FORMAT.members

    @util.contractual
    def determine(self):
        """Determine the format of the file.

        Raise IOError if reading fails.
        Raise UnicodeError if decoding fails.
        Raise FormatError if unable to detect the format.
        Return FORMAT constant.
        """
        args = (self.path, "r", self.encoding)
        with contextlib.closing(codecs.open(*args)) as fobj:
            for line in fobj:
                for format, re_id in self._re_ids:
                    if re_id.search(line) is not None:
                        return format
        raise FormatError
