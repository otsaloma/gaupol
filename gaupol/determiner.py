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


"""Subtitle file format determiner."""


import re

from gaupol import const, util
from gaupol.errors import FormatError
from gaupol.files import *


class FormatDeterminer(object):

    """Subtitle file format determiner.

    Instance variables:

        encoding: Character encoding to open the file with
        path:     Filepath
        re_ids:   List of tuples of format, regular expression
    """

    def __init__(self, path, encoding):

        self.encoding = encoding
        self.path     = path
        self.re_ids   = []

        for format in const.FORMAT.members:
            re_id = re.compile(*eval(format.class_name).identifier)
            self.re_ids.append((format, re_id))

    def determine(self):
        """Determine the format of the file.

        Raise IOError if reading fails.
        Raise UnicodeError if decoding fails.
        Raise FormatError if unable to detect the format.
        Return FORMAT constant.
        """
        for line in util.readlines(self.path, self.encoding):
            for format, re_id in self.re_ids:
                if re_id.search(line) is not None:
                    return format
        raise FormatError
