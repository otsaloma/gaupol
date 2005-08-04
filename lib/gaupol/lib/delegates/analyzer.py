# Copyright (C) 2005 Osmo Salomaa
#
# This file is part of Gaupol.
#
# Gaupol is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Gaupol is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Gaupol; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA


"""Provider of statistics and information."""


import re

try:
    from psyco.classes import *
except ImportError:
    pass

from gaupol.lib.delegates.delegate import Delegate
from gaupol.lib.formats import tags as tags_module


class Analyzer(Delegate):
    
    """Provider of statistics and information."""

    def get_character_count(self, row, col):
        """
        Get character of text specified by row and col.
        
        Return: list of row lengths, total length
        """
        text   = self.texts[row][col]
        format = self.get_format(col)

        if format != None:
            re_tag = self.get_tag_re(col)
            text   = re_tag.sub('', text)

        lines = text.split('\n')

        lengths = [len(line) for line in lines]
        total   = len(text)
        
        return lengths, total
