# Copyright (C) 2006-2007 Osmo Salomaa
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


import gaupol.gtk
import gtk

from gaupol.gtk import unittest
from .. import ruler


class TestModule(unittest.TestCase):

    def run(self):

        text_view = gtk.TextView()
        text_buffer = text_view.get_buffer()
        text = \
            "Everything has been said\n" + \
            "provided words do not change\n" + \
            "their meanings\n" + \
            "and meanings their words"
        text_buffer.insert_at_cursor(text)
        ruler.connect_text_view(text_view)
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

    def setup_method(self, method):

        gaupol.gtk.conf.read()
        reload(ruler)

    def test_connect_text_view(self):

        text_view = gtk.TextView()
        ruler.connect_text_view(text_view)
        text_buffer = text_view.get_buffer()
        text_buffer.insert_at_cursor("test\ntest")

    def test_disconnect_text_view(self):

        text_view = gtk.TextView()
        ruler.connect_text_view(text_view)
        ruler.disconnect_text_view(text_view)
        text_buffer = text_view.get_buffer()
        text_buffer.insert_at_cursor("test\ntest")

    def test_func(self):

        gaupol.gtk.conf.editor.length_unit = gaupol.gtk.LENGTH_UNIT.CHAR
        assert ruler.func("MMM<i>iii</i>") == 13

    def test_get_lengths__char(self):

        gaupol.gtk.conf.editor.length_unit = gaupol.gtk.LENGTH_UNIT.CHAR
        lengths = ruler.get_lengths("MMM\n<i>iii</i>")
        assert lengths == [3, 3]

    def test_get_lengths__em(self):

        gaupol.gtk.conf.editor.length_unit = gaupol.gtk.LENGTH_UNIT.EM
        gaupol.gtk.conf.editor.use_default_font = True
        lengths = ruler.get_lengths("MMM\n<i>i</i>")
        assert lengths == [3, 0]
