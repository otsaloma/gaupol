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


import gtk

from gaupol.gtk.cellrend.text import CellRendererText
from gaupol.test              import Test


class TestCellRendererText(Test):

    def setup_method(self, method):

        self.cell_renderer = CellRendererText()

    def test_get_and_set_property(self):

        self.cell_renderer.font = 'test'
        font = self.cell_renderer.font
        assert font == 'test'

    def test_on_get_size(self):

        size = self.cell_renderer.get_size(gtk.TreeView())
        assert isinstance(size[0], int)
        assert isinstance(size[1], int)
        assert isinstance(size[2], int)
        assert isinstance(size[3], int)
        assert size[0] < size[2]
        assert size[1] < size[3]

    def test_set_editable(self):

        self.cell_renderer.set_editable(False)
        mode = self.cell_renderer.props.mode
        assert mode == gtk.CELL_RENDERER_MODE_ACTIVATABLE

        self.cell_renderer.set_editable(True)
        mode = self.cell_renderer.props.mode
        assert mode == gtk.CELL_RENDERER_MODE_EDITABLE
