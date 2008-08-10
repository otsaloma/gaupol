# Copyright (C) 2005-2007 Osmo Salomaa
#
# This file is part of Gaupol.
#
# Gaupol is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# Gaupol is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# Gaupol. If not, see <http://www.gnu.org/licenses/>.

import gtk
import gaupol.gtk


class TestTimeEntry(gaupol.gtk.TestCase):

    def run__entry(self):

        self.entry.set_text("12:34:56.789")
        window = gtk.Window()
        window.connect("delete-event", gtk.main_quit)
        window.set_position(gtk.WIN_POS_CENTER)
        window.set_default_size(200, 50)
        window.add(self.entry)
        window.show_all()
        gtk.main()

    def setup_method(self, method):

        self.entry = gaupol.gtk.TimeEntry()

    def test_set_text(self):

        self.entry.set_text("12:34:56.789")
        self.entry.set_text("-12:34:56.789")
