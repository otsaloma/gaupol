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


"""Searching for and replacing text."""


import gaupol.gtk


class SearchAgent(gaupol.Delegate):

    """Searching for and replacing text.

    Instance variables:
     * _search_dialog: Existing SearchDialog or None
    """

    # pylint: disable-msg=E0203,W0201

    def __init__(self, master):

        gaupol.Delegate.__init__(self, master)
        self._search_dialog = None

    def _on_search_dialog_response(self, *args):
        """Hide the search dialog."""

        self._search_dialog.hide()

    def on_find_and_replace_activate(self, *args):
        """Search for and replace text."""

        if self._search_dialog is not None:
            return self._search_dialog.present()
        self._search_dialog = gaupol.gtk.SearchDialog(self)
        gaupol.gtk.util.connect(self, "_search_dialog", "response")
        self._search_dialog.show()

    def on_find_next_activate(self, *args):
        """Search forwards for same text."""

        self._search_dialog.next()

    def on_find_previous_activate(self, *args):
        """Search backwards for same text."""

        self._search_dialog.previous()
