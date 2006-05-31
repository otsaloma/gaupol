# Copyright (C) 2005-2006 Osmo Salomaa
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


from gaupol.gtk.entry.time import EntryTime
from gaupol.test           import Test


class TestEntryTime(Test):

    def test_init(self):

        EntryTime()


if __name__ == '__main__':

    import gtk

    entry = EntryTime()
    entry.set_text('12:34:56,789')
    window = gtk.Window()
    window.connect('delete-event', gtk.main_quit)
    window.set_position(gtk.WIN_POS_CENTER)
    window.set_default_size(200, 50)
    window.add(entry)
    window.show_all()
    gtk.main()
