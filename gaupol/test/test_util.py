# -*- coding: utf-8 -*-

# Copyright (C) 2005 Osmo Salomaa
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

from gi.repository import Gdk


class TestModule(gaupol.TestCase):

    def test_char_to_px(self):
        px1 = gaupol.util.char_to_px(1)
        px2 = gaupol.util.char_to_px(2)
        assert 2 < px1 < 10
        assert 4 < px2 < 20
        assert abs(2 * px1 - px2) <= 1

    def test_char_to_px__font(self):
        deft = gaupol.util.char_to_px(100)
        cust = gaupol.util.char_to_px(100, font="custom")
        mono = gaupol.util.char_to_px(100, font="monospace")
        assert 200 < deft < cust
        assert 200 < deft < mono

    def test_hex_to_rgba(self):
        color = gaupol.util.hex_to_rgba("#ff0000")
        assert color.equal(Gdk.RGBA(red=1, green=0, blue=0, alpha=1))

    def test_lines_to_px(self):
        px1 = gaupol.util.lines_to_px(1)
        px2 = gaupol.util.lines_to_px(2)
        assert 10 < px1 < 30
        assert 20 < px2 < 60
        assert abs(2 * px1 - px2) <= 1

    def test_lines_to_px__font(self):
        deft = gaupol.util.lines_to_px(10)
        cust = gaupol.util.lines_to_px(10, font="custom")
        mono = gaupol.util.lines_to_px(10, font="monospace")
        assert 50 < deft < 200
        assert 50 < cust < 200
        assert 50 < mono < 200

    def test_rgba_to_hex(self):
        rgba = Gdk.RGBA(red=1, green=0, blue=1)
        color = gaupol.util.rgba_to_hex(rgba)
        assert color == "#ff00ff"

    def test_tree_path_to_row(self):
        path = gaupol.util.tree_row_to_path(1)
        assert gaupol.util.tree_path_to_row(path) == 1
        assert gaupol.util.tree_path_to_row("1") == 1

    def test_tree_row_to_path(self):
        path = gaupol.util.tree_row_to_path(1)
        assert gaupol.util.tree_path_to_row(path) == 1
