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


"""Advanced Sub Station Alpha tag library."""


import re

from .ssa import SubStationAlpha


class AdvSubStationAlpha(SubStationAlpha):

    """Advanced Sub Station Alpha tag library.

    Class variables:

        _re_redundant: Regular expression for a redundant tag pair
    """

    decode_tags = [
        # Underline opening
        (r"\{\\u1\}", re.IGNORECASE,
            r"<u>"),
        # Underline closing
        (r"\{\\u0\}", re.IGNORECASE,
            r"</u>")
    ] + SubStationAlpha.decode_tags

    encode_tags = [
        # Underline opening
        (r"<u>", re.IGNORECASE,
            r"{\\u1}"),
        # Underline closing
        (r"</u>", re.IGNORECASE,
            r"{\\u0}")
    ] + SubStationAlpha.encode_tags

    # \061 = 1
    _re_redundant = re.compile(
        r"\{\\([ibu])0\}([^\w\n]*?)\{\\\1\061\}", re.UNICODE)

    @classmethod
    def remove_redundant(cls, text):
        """Remove redundant tags from text."""

        return cls._re_redundant.sub(r"\2", text)
