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


"""Entry for integer data."""


import gtk


class IntegerEntry(gtk.Entry):

    """Entry for integer data."""

    def __init__(self):

        gtk.Entry.__init__(self)
        self.connect('insert-text', self._on_insert_text)

    def _on_insert_text(self, entry, text, length, position):
        """Insert text if it is digits."""

        if not text.isdigit():
            self.emit_stop_by_name('insert-text')


if __name__ == '__main__':

    from gaupol.test import Test

    class TestIntegerEntry(Test):

        def test_init(self):

            entry = IntegerEntry()
            entry.set_text('333')
            window = gtk.Window()
            window.connect('delete-event', gtk.main_quit)
            window.set_position(gtk.WIN_POS_CENTER)
            window.set_default_size(200, 50)
            window.add(entry)
            window.show_all()
            gtk.main()

    TestIntegerEntry().run()
