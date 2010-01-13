# Copyright (C) 2006-2008 Osmo Salomaa
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

import gaupol
import gtk


class TestModule(gaupol.TestCase):

    def run__text_view(self):

        text_view = gtk.TextView()
        text_buffer = text_view.get_buffer()
        text = ("Everything has been said\n"
                "provided words do not change\n"
                "their meanings\n"
                "and meanings their words")
        text_buffer.insert_at_cursor(text)
        gaupol.ruler.connect_text_view(text_view)
        scroller = gtk.ScrolledWindow()
        scroller.set_shadow_type(gtk.SHADOW_IN)
        scroller.add(text_view)
        window = gtk.Window()
        window.connect("delete-event", gtk.main_quit)
        window.set_position(gtk.WIN_POS_CENTER)
        window.set_default_size(300, 100)
        window.set_border_width(12)
        window.add(scroller)
        window.show_all()
        gtk.main()

    def test_connect_text_view(self):

        text_view = gtk.TextView()
        gaupol.ruler.connect_text_view(text_view)
        text_buffer = text_view.get_buffer()
        text_buffer.insert_at_cursor("test\ntest")

    def test_disconnect_text_view(self):

        text_view = gtk.TextView()
        gaupol.ruler.connect_text_view(text_view)
        gaupol.ruler.disconnect_text_view(text_view)
        text_buffer = text_view.get_buffer()
        text_buffer.insert_at_cursor("test\ntest")

    def test_get_length_function(self):

        unit = gaupol.length_units.CHAR
        function = gaupol.ruler.get_length_function(unit)
        assert function("iii") == 3
        unit = gaupol.length_units.EM
        function = gaupol.ruler.get_length_function(unit)
        assert 0.5 < function("M") < 1.5

    def test_get_lengths__char(self):

        unit = gaupol.length_units.CHAR
        gaupol.conf.editor.length_unit = unit
        lengths = gaupol.ruler.get_lengths("MMM\n<i>iii</i>")
        assert lengths == (3, 3)

    def test_get_lengths__em(self):

        unit = gaupol.length_units.EM
        gaupol.conf.editor.length_unit = unit
        gaupol.conf.editor.use_custom_font = False
        lengths = gaupol.ruler.get_lengths("MMM\n<i>i</i>")
        assert lengths == (3, 0)
