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
import gtk.glade

from gaupol.gtk.unittest import TestCase
from .. import glade


class TestGladeDialog(TestCase):

    def setup_method(self, method):

        self.dialog = glade.GladeDialog("debug-dialog")

    def test___getattr__(self):

        self.dialog.hide()
        self.dialog.show()

    def test___init__(self):

        assert isinstance(self.dialog._dialog, gtk.Dialog)
        assert isinstance(self.dialog._glade_xml, gtk.glade.XML)

    def test___setattr__(self):

        self.dialog.props.visible = False
        self.dialog.props.visible = True
