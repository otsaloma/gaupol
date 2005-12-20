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


"""Additional functions for manipulating lists."""


try:
    from psyco.classes import *
except ImportError:
    pass


def remove_duplicates(lst):
    """
    Remove duplicates from list.

    If duplicates exist, the first one will be kept and others removed.
    Return a copy of the original list with duplicates removed.
    """
    lst = lst[:]

    for i in reversed(range(len(lst))):
        for k in range(0, i):
            if lst[i] == lst[k]:
                lst.pop(i)
                break

    return lst

def sort_and_remove_duplicates(lst):
    """
    Sort list and remove duplicates from it.

    Return a copy of the original list with sorted and with duplicates removed.
    """
    lst = lst[:]
    lst.sort()

    for i in reversed(range(1, len(lst))):
        if lst[i] == lst[i - 1]:
            lst.pop(i)

    return lst

def strip_spaces(strings):
    """
    Strip leading and trailing spaces in list of strings.

    Stripping is done in-place, nothing is returned.
    """
    for i in range(len(strings)):
        strings[i] = strings[i].strip()
