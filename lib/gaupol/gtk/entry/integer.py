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


"""Entry for integer data."""


import gtk


class EntryInteger(gtk.Entry):

    """Entry for integer data."""

    def __init__(self):

        gtk.Entry.__init__(self)
        self.connect('insert-text', self._on_insert_text)

    def _on_insert_text(self, entry, text, length, pos):
        """Insert text if it is digits."""

        if not text.isdigit():
            self.stop_emission('insert-text')
