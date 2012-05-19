# -*- coding: utf-8-unix -*-

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

import aeidon
import gaupol

from gi.repository import Gtk


class TestMultiCloseDialog(gaupol.TestCase):

    def run__dialog__both(self):
        self.setup_both()
        self.dialog.run()
        self.dialog.destroy()

    def run__dialog__main(self):
        self.setup_main()
        self.dialog.run()
        self.dialog.destroy()

    def run__dialog__translation(self):
        self.setup_translation()
        self.dialog.run()
        self.dialog.destroy()

    def setup_both(self):
        self.application = self.new_application()
        for page in self.application.pages:
            page.project.remove_subtitles((0,))
        self.dialog = gaupol.MultiCloseDialog(self.application.window,
                                              self.application,
                                              self.application.pages)

        self.dialog.show()

    def setup_main(self):
        self.application = self.new_application()
        for page in self.application.pages:
            page.project.set_text(0, aeidon.documents.MAIN, "")
        self.dialog = gaupol.MultiCloseDialog(self.application.window,
                                              self.application,
                                              self.application.pages)

        self.dialog.show()

    def setup_method(self, method):
        return self.setup_both()

    def setup_translation(self):
        self.application = self.new_application()
        for page in self.application.pages:
            page.project.set_text(0, aeidon.documents.TRAN, "")
        self.dialog = gaupol.MultiCloseDialog(self.application.window,
                                              self.application,
                                              self.application.pages)

        self.dialog.show()

    def test___init__(self):
        assert self.dialog.pages is not self.application.pages

    def test__on_response__no(self):
        self.dialog.response(Gtk.ResponseType.NO)

    def test__on_response__yes(self):
        self.dialog.response(Gtk.ResponseType.YES)

    def test__on_tree_view_cell_toggled__main(self):
        column = self.dialog._main_tree_view.get_columns()[0]
        renderer = column.get_cells()[0]
        renderer.emit("toggled", 0)
        renderer.emit("toggled", 0)

    def test__on_tree_view_cell_toggled__translation(self):
        column = self.dialog._tran_tree_view.get_columns()[0]
        renderer = column.get_cells()[0]
        renderer.emit("toggled", 0)
        renderer.emit("toggled", 0)
