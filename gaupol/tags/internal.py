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


"""Internal tags."""


class Internal(object):

    """Internal tags.

    Class variables:

        opening_tag:     Regular expression pattern, flags
        closing_tag:     Regular expression pattern, flags
        closing_tag_end: Regular expression pattern, flags

    Internal tags:

        <b></b>
        <i></i>
        <u></u>
        <color="#RRGGBB"></color>
        <font="NAME"></font>
        <size="INT"></size>
    """

    opening_tag = r"<[^/].*?>", 0
    closing_tag = r"</.*?>", 0
    closing_tag_end = r"</.*?>\Z" , 0
