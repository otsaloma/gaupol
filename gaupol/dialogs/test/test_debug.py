# -*- coding: utf-8 -*-

# Copyright (C) 2005-2008,2010 Osmo Salomaa
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
import sys

from gi.repository import Gtk


class TestDebugDialog(gaupol.TestCase):

    def run_dialog(self):
        self.dialog.run()
        self.dialog.destroy()

    def setup_method(self, method):
        self.dialog = gaupol.DebugDialog()
        try:
            self.dialog.foo()
        except AttributeError:
            self.dialog.set_text(*sys.exc_info())
        self.dialog.show()

    def test__on_response__close(self):
        self.dialog.response(Gtk.ResponseType.CLOSE)

    def test__on_response__no(self):
        self.dialog.response(Gtk.ResponseType.NO)

    def test__on_response__yes(self):
        self.dialog.response(Gtk.ResponseType.YES)
