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
import re

from gaupol import const, enclib
from gaupol.base import Contractual, Singleton
from gaupol.errors import FormatError
from gaupol.files import *


class FormatDeterminer(Singleton):

    """Subtitle file format determiner.

    Instance variables:
     * _re_ids: List of tuples of format, regular expression
    """

    __metaclass__ = Contractual

    # pylint: disable-msg=W0231
    def __init__(self):

        self._re_ids = []
        for format in const.FORMAT.members:
            re_id = re.compile(format.identifier)
            self._re_ids.append((format, re_id))

    def determine_require(self, path, encoding):
        assert os.path.isfile(path)
        assert enclib.is_valid(encoding)

    def determine(self, path, encoding):
        """Determine the format of the file.

        Raise IOError if reading fails.
        Raise UnicodeError if decoding fails.
        Raise FormatError if unable to detect the format.
        Return FORMAT constant.
        """
        args = (path, "r", encoding)
        with contextlib.closing(codecs.open(*args)) as fobj:
            for line in fobj:
                for format, re_id in self._re_ids:
                    if re_id.search(line) is not None:
                        return format
        raise FormatError
