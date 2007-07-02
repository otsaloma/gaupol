# Copyright (C) 2005-2007 Osmo Salomaa
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
# A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# Gaupol.  If not, see <http://www.gnu.org/licenses/>.


import gaupol.gtk
import gtk

from gaupol.gtk import unittest
from .. import previewerr


class TestPreviewErrorDialog(unittest.TestCase):

    def run(self):

        self.dialog.run()
        self.dialog.destroy()

    def setup_method(self, method):

        output = self.get_file_text(gaupol.gtk.FORMAT.SUBRIP)
        self.dialog = previewerr.PreviewErrorDialog(gtk.Window(), output)

    def test___init__(self):

        pass
