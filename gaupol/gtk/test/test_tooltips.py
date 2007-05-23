# Copyright (C) 2007 Osmo Salomaa
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


import gtk

from gaupol.gtk.unittest import TestCase
from .. import tooltips


class TestTooltips(TestCase):

    def run(self):

        button = gtk.Button("Hover over this")
        text = "<b>Bold</b>\n<i>Italic</i>\n<u>Underline</u>"
        self.tooltips.set_tip(button, text)
        window = gtk.Window()
        window.connect("delete-event", gtk.main_quit)
        window.set_position(gtk.WIN_POS_CENTER)
        window.add(button)
        window.show_all()
        gtk.main()

    def setup_method(self, method):

        self.tooltips = tooltips.Tooltips()

    def test__on_label_notify_use_markup(self):

        self.tooltips.tip_label.set_use_markup(False)
