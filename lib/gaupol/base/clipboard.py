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


"""Gaupol internal clipboard."""


class Clipboard(object):

    """
    Gaupol internal clipboard.

    Data on the clipboard is directly available as attribute "data". Its value
    is [] if there's nothing on the clipboard. data is a one-dimensional list
    with multiple ranges made possible with elements having value None to
    express that the row is skipped in the range.
    """

    def __init__(self):

        self.data = []

    def get_data_as_string(self):
        """Get clipboard data as a single string."""

        # Replace Nones with empty strings.
        string_list = []
        for element in self.data:
            string_list.append(element or '')

        # Separate list elements with a blank line to form a string.
        return '\n\n'.join(string_list)


if __name__ == '__main__':

    clipboard = Clipboard()
    clipboard.data = ['foo', None, 'bar', None]
    string = clipboard.get_data_as_string()
    assert string == 'foo\n\n\n\nbar\n\n'
