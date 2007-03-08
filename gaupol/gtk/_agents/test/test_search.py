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

from gaupol.gtk.unittest import TestCase


class TestSearchAgent(TestCase):

    def setup_method(self, method):

        self.application = self.get_application()
        self.delegate = self.application.on_find_next_activate.im_self

    def test__on_search_dialog_response(self):

        self.application.on_find_and_replace_activate()
        self.delegate._search_dialog.response(gtk.RESPONSE_CLOSE)

    def test_on_find_and_replace_activate(self):

        self.application.on_find_and_replace_activate()
        self.application.on_find_and_replace_activate()

    def test_on_find_next_activate(self):

        self.application.on_find_and_replace_activate()
        self.delegate._search_dialog._pattern_entry.set_text("a")
        self.application.on_find_next_activate()
        self.delegate._search_dialog.response(gtk.RESPONSE_CLOSE)
        self.application.on_find_next_activate()

    def test_on_find_previous_activate(self):

        self.application.on_find_and_replace_activate()
        self.delegate._search_dialog._pattern_entry.set_text("a")
        self.application.on_find_previous_activate()
        self.delegate._search_dialog.response(gtk.RESPONSE_CLOSE)
        self.application.on_find_previous_activate()
