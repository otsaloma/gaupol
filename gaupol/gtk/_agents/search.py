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


"""Searching for and replacing text."""


from gaupol.base import Delegate
from gaupol.gtk import util
from gaupol.gtk.dialogs import SearchDialog


class SearchAgent(Delegate):

    """Searching for and replacing text.

    Instance variables:

        _pref_dialog: PreferencesDialog or None
    """

    # pylint: disable-msg=E0203,W0201

    def __init__(self, master):

        Delegate.__init__(self, master)
        self._search_dialog = None

    def _on_search_dialog_response(self, *args):
        """Destroy the search dialog."""

        self._search_dialog.destroy()
        self._search_dialog = None

    def on_find_and_replace_activate(self, *args):
        """Search for and replace text."""

        if self._search_dialog is None:
            self._search_dialog = SearchDialog(self.master)
            util.connect(self, "_search_dialog", "response")
            self._search_dialog.show()
        self._search_dialog.present()

    def on_find_next_activate(self, *args):
        """Search forwards for same text."""

        if self._search_dialog is None:
            self._search_dialog = SearchDialog(self.master)
            util.connect(self, "_search_dialog", "response")
        self._search_dialog.next()

    def on_find_previous_activate(self, *args):
        """Search backwards for same text."""

        if self._search_dialog is None:
            self._search_dialog = SearchDialog(self.master)
            util.connect(self, "_search_dialog", "response")
        self._search_dialog.previous()
