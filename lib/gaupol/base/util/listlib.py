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


"""Functions for manipulating lists."""


def sorted_unique(lst):
    """Return sorted list with duplicates removed."""

    lst = sorted(lst)
    for i in reversed(range(1, len(lst))):
        if lst[i] == lst[i - 1]:
            lst.pop(i)
    return lst

def unique(lst):
    """Return list with duplicates removed."""

    lst = lst[:]
    for i in reversed(range(len(lst))):
        for j in range(0, i):
            if lst[j] == lst[i]:
                lst.pop(i)
                break
    return lst
