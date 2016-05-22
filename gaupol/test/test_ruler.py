# -*- coding: utf-8 -*-

# Copyright (C) 2006 Osmo Salomaa
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import gaupol

from gi.repository import Gtk


class TestModule(gaupol.TestCase):

    def test_connect_text_view(self):
        text_view = Gtk.TextView()
        gaupol.ruler.connect_text_view(text_view)
        text_buffer = text_view.get_buffer()
        text_buffer.insert_at_cursor("test\ntest")

    def test_disconnect_text_view(self):
        text_view = Gtk.TextView()
        gaupol.ruler.connect_text_view(text_view)
        gaupol.ruler.disconnect_text_view(text_view)
        text_buffer = text_view.get_buffer()
        text_buffer.insert_at_cursor("test\ntest")

    def test_get_length_function__char(self):
        unit = gaupol.length_units.CHAR
        function = gaupol.ruler.get_length_function(unit)
        assert function("iii") == 3

    def test_get_length_function__em(self):
        unit = gaupol.length_units.EM
        function = gaupol.ruler.get_length_function(unit)
        assert 0.5 < function("M") < 1.5

    def test_get_lengths__char(self):
        unit = gaupol.length_units.CHAR
        gaupol.conf.editor.length_unit = unit
        lengths = gaupol.ruler.get_lengths("MMM\n<i>iii</i>")
        assert tuple(lengths) == (3, 3)

    def test_get_lengths__em(self):
        unit = gaupol.length_units.EM
        gaupol.conf.editor.length_unit = unit
        lengths = gaupol.ruler.get_lengths("MMM\n<i>iii</i>")
        assert -1 < lengths[1] < 1 < lengths[0]
