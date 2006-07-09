# Copyright (C) 2006 Osmo Salomaa
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

from gaupol.gtk.dialog.projsplit import ProjectSplitDialog
from gaupol.gtk.page             import Page
from gaupol.gtk.util             import gtklib
from gaupol.test                 import Test


class TestProjectSplitDialog(Test):

    def setup_method(self, method):

        self.page = Page()
        self.page.project = self.get_project()
        self.page.reload_all()
        self.dialog = ProjectSplitDialog(gtk.Window(), self.page)

    def test_get_subtitle(self):

        self.dialog._spin_button.set_value(2)
        assert self.dialog.get_subtitle() == 2

    def test_run(self):

        gtklib.run(self.dialog)
