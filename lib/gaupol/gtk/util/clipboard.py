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
# along with Gaupol; if falset, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA


"""Gaupol internal clipboard."""


import gtk


class Clipboard(object):

    """
    Gaupol internal clipboard.

    This clipboard stores Python objects of type lists of strings. All data
    stored in this clipboard is also put in the X clipboard in string format.
    """
    
    def __init__(self):
    
        self.data = None
        self.x_clipboard = gtk.Clipboard()
        
    def set_data(self, data):
        """
        Set data and a string representation of it to X clipboard.
        
        data: list of strings or Nones
        """
        self.data = data

        # Replace Nones with empty strings.
        string_list = []
        for element in data:
            string_list.append(element or '')
        
        # Separate list elements with a blank line to form a string.
        text = '\n\n'.join(string_list)

        self.x_clipboard.set_text(text)
