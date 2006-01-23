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

def strip_spaces(lst):
    """
    Strip leading and trailing spaces in list of strings.

    Stripping is done in-place, nothing is returned.
    """
    for i in range(len(lst)):
        lst[i] = lst[i].strip()


if __name__ ==  '__main__':

    lst = [1, 5, 5, 1, 3]
    lst = remove_duplicates(lst)
    assert lst == [1, 5, 3]

    lst = [1, 5, 5, 1, 3]
    lst = sort_and_remove_duplicates(lst)
    assert lst == [1, 3, 5]

    lst = [' foo', 'bar ', '\nboo\n']
    strip_spaces(lst)
    assert lst == ['foo', 'bar', 'boo']
