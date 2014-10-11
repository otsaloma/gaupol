# -*- coding: utf-8 -*-

# Copyright (C) 2005 Osmo Salomaa
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""Searching for and replacing text."""

import aeidon
import gaupol


class SearchAgent(aeidon.Delegate):

    """Searching for and replacing text."""

    def __init__(self, master):
        """Initialize a :class:`SearchAgent` instance."""
        aeidon.Delegate.__init__(self, master)
        self._search_dialog = None

    def _on_search_dialog_response(self, *args):
        """Hide the search dialog."""
        self._search_dialog.hide()

    @aeidon.deco.export
    def _on_find_and_replace_activate(self, *args):
        """Search for and replace text."""
        if self._search_dialog is not None:
            return self._search_dialog.present()
        self._search_dialog = gaupol.SearchDialog(self.window, self)
        aeidon.util.connect(self, "_search_dialog", "response")
        # Do not destroy the dialog, but rather hide based on response.
        self._search_dialog.connect("delete-event", lambda *args: True)
        self._search_dialog.show()

    @aeidon.deco.export
    def _on_find_next_activate(self, *args):
        """Search forwards for same text."""
        self._search_dialog.next()

    @aeidon.deco.export
    def _on_find_previous_activate(self, *args):
        """Search backwards for same text."""
        self._search_dialog.previous()
