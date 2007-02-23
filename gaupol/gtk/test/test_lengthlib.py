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


import gtk

from gaupol.gtk import conf, cons
from gaupol.gtk.unittest import TestCase
from .. import lengthlib


class TestModule(TestCase):

    def run(self):

        text_view = gtk.TextView()
        text_buffer = text_view.get_buffer()
        text = \
            "Everything has been said\n" + \
            "provided words do not change\n" + \
            "their meanings\n" + \
            "and meanings their words"
        text_buffer.insert_at_cursor(text)
        lengthlib.connect_text_view(text_view)
        window = gtk.Window()
        window.connect("delete-event", gtk.main_quit)
        window.set_position(gtk.WIN_POS_CENTER)
        window.set_default_size(300, 100)
        window.set_border_width(12)
        window.add(text_view)
        window.show_all()
        gtk.main()

    def teardown_method(self, method):

        TestCase.teardown_method(self, method)
        reload(conf)
        reload(lengthlib)

    def test_connect_text_view(self):

        text_view = gtk.TextView()
        lengthlib.connect_text_view(text_view)
        text_buffer = text_view.get_buffer()
        text_buffer.insert_at_cursor("test\ntest")

    def test_disconnect_text_view(self):

        text_view = gtk.TextView()
        lengthlib.connect_text_view(text_view)
        lengthlib.disconnect_text_view(text_view)
        text_buffer = text_view.get_buffer()
        text_buffer.insert_at_cursor("test\ntest")

    def test_func(self):

        conf.editor.length_unit = cons.LENGTH_UNIT.CHAR
        assert lengthlib.func("MMMMM<i>iiiii</i>") == 17

    def test_get_lengths_char(self):

        conf.editor.length_unit = cons.LENGTH_UNIT.CHAR
        lengths = lengthlib.get_lengths("MMMMM\n<i>iiiii</i>")
        assert lengths == [5, 5]

    def test_get_lengths_em(self):

        conf.editor.length_unit = cons.LENGTH_UNIT.EM
        conf.editor.use_default_font = True
        lengths = lengthlib.get_lengths("MMMMM\n<i>iiiii</i>")
        assert lengths[0] == 5
        assert lengths[1] < 5
