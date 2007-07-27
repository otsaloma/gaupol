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

import gtk

from gaupol.gtk import unittest
from .. import multiclose


class TestMultiCloseDialog(unittest.TestCase):

    def run(self):

        self.dialog.run()
        self.dialog.destroy()

    def setup_method(self, method):

        self.application = self.get_application()
        for page in self.application.pages:
            page.project.remove_subtitles([0])
        cls = multiclose.MultiCloseDialog
        parent = self.application.window
        application = self.application
        pages = self.application.pages
        self.dialog = cls(parent, application, pages)

    def test__on_response(self):

        self.dialog.response(gtk.RESPONSE_YES)
