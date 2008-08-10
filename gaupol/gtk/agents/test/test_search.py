# Copyright (C) 2005-2008 Osmo Salomaa
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

import gaupol.gtk
import gtk


class TestSearchAgent(gaupol.gtk.TestCase):

    def setup_method(self, method):

        self.application = self.get_application()
        self.delegate = self.application.on_find_next_activate.im_self

    def test__on_search_dialog_response(self):

        self.application.get_action("find_and_replace").activate()
        self.delegate._search_dialog.response(gtk.RESPONSE_CLOSE)

    def test_on_find_and_replace_activate(self):

        self.application.get_action("find_and_replace").activate()
        self.application.get_action("find_and_replace").activate()

    def test_on_find_next_activate(self):

        self.application.get_action("find_and_replace").activate()
        self.delegate._search_dialog._pattern_entry.set_text("a")
        self.delegate._search_dialog.next()
        self.application.get_action("find_next").activate()
        self.delegate._search_dialog.response(gtk.RESPONSE_CLOSE)
        self.application.get_action("find_next").activate()

    def test_on_find_previous_activate(self):

        self.application.get_action("find_and_replace").activate()
        self.delegate._search_dialog._pattern_entry.set_text("a")
        self.delegate._search_dialog.previous()
        self.delegate._search_dialog.emit("delete-event", None)
        self.application.get_action("find_previous").activate()
        self.delegate._search_dialog.response(gtk.RESPONSE_CLOSE)
        self.application.get_action("find_previous").activate()
