# Copyright (C) 2006-2009 Osmo Salomaa
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
import gaupol


class TestBuilderDialog(gaupol.TestCase):

    def setup_method(self, method):
        self.dialog = gaupol.LanguageDialog(gtk.Window())
        self.dialog.show()

    def test___getattr__(self):
        self.dialog.hide()
        self.dialog.show()

    def test___init__(self):
        assert hasattr(self.dialog, "_builder")
        assert hasattr(self.dialog, "_dialog")

    def test___setattr__(self):
        self.dialog.props.visible = False
        self.dialog.props.visible = True
        self.dialog.props.visible = False

    def test__setattr_widgets(self):
        self.dialog._setattr_widgets(("tree_view",))

    def test_run(self):
        self.dialog._dialog.run = lambda: None
        self.dialog.run()
