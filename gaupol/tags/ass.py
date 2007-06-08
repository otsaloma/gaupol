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


"""Advanced Sub Station Alpha tag library."""


import gaupol
import re

from .ssa import SubStationAlpha


class AdvSubStationAlpha(SubStationAlpha):

    """Advanced Sub Station Alpha tag library."""

    format = gaupol.FORMAT.ASS

    @gaupol.util.once
    def _get_decode_tags(self):
        """Get list of tuples of regular expression, replacement, count."""

        FLAGS = re.IGNORECASE

        tags = [
            # Underline opening
            (r"\{\\u1\}", FLAGS,
                r"<u>", 1),
            # Underline closing
            (r"\{\\u0\}", FLAGS,
                r"</u>", 1),]

        for i, (pattern, flags, replacement, count) in enumerate(tags):
            tags[i] = (re.compile(pattern, flags), replacement, count)
        return tags + SubStationAlpha._get_decode_tags(self)

    @gaupol.util.once
    def _get_encode_tags(self):
        """Get list of tuples of regular expression, replacement, count."""

        FLAGS = re.IGNORECASE

        tags = [
            # Underline opening
            (r"<u>", FLAGS,
                r"{\\u1}", 1),
            # Underline closing
            (r"</u>", FLAGS,
                r"{\\u0}", 1),]

        for i, (pattern, flags, replacement, count) in enumerate(tags):
            tags[i] = (re.compile(pattern, flags), replacement, count)
        return tags + SubStationAlpha._get_encode_tags(self)
