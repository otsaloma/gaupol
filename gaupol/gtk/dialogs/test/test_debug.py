# Copyright (C) 2005-2007 Osmo Salomaa
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
import sys

from gaupol.gtk import unittest
from .. import debug


class TestDebugDialog(unittest.TestCase):

    def run(self):

        try:
            self.dialog.foo()
        except Exception:
            self.dialog.set_text(*sys.exc_info())
        self.dialog.run()
        self.dialog.destroy()

    def run__show_editor_error_dialog(self):

        self.dialog._show_editor_error_dialog()

    def setup_method(self, method):

        self.dialog = debug.DebugDialog()

    def test__on_response__close(self):

        self.dialog.response(gtk.RESPONSE_CLOSE)

    def test__on_response__no(self):

        self.dialog.response(gtk.RESPONSE_NO)

    def test__on_response__yes(self):

        self.dialog.response(gtk.RESPONSE_YES)
