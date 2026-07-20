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
# along with this program. If not, see <https://www.gnu.org/licenses/>.

"""Dialog for inserting new subtitles."""

import gaupol

from aeidon.i18n   import _
from gi.repository import Gtk

class InsertDialog(gaupol.BuilderDialog):

    """Dialog for inserting new subtitles."""

    _widgets = ["above_button", "amount_spin", "below_button"]

    def __init__(self, parent, application):
        """Initialize an :class:`InsertDialog` instance."""
        gaupol.BuilderDialog.__init__(self, "insert-dialog.ui")
        self.application = application
        self._init_dialog(parent)
        self._init_values()

    def _init_dialog(self, parent):
        """Initialize the dialog."""
        self.add_button(_("_Cancel"), Gtk.ResponseType.CANCEL)
        self.add_button(_("_Insert"), Gtk.ResponseType.OK)
        self.set_default_response(Gtk.ResponseType.OK)
        self.set_transient_for(parent)
        self.set_modal(True)

    def _init_values(self):
        """Initialize default values for widgets."""
        self._amount_spin.set_value(1)
        if gaupol.conf.subtitle_insert.above:
            self._above_button.set_active(True)
        else:
            self._below_button.set_active(True)
        page = self.application.get_current_page()
        sensitive = bool(page.project.subtitles)
        self._above_button.set_sensitive(sensitive)
        self._below_button.set_sensitive(sensitive)

    def _insert_subtitles(self, amount, above):
        """Insert `amount` of subtitles to project."""
        page = self.application.get_current_page()
        if page.project.subtitles:
            index = page.view.get_selected_rows()[-1]
            if not above: index += 1
        else: # No subtitles in project.
            index = 0
        indices = list(range(index, index + amount))
        page.project.insert_subtitles(indices)

    def _on_response(self, dialog, response):
        """Save default values and insert subtitles."""
        amount = self._amount_spin.get_value_as_int()
        above = self._above_button.get_active()
        gaupol.conf.subtitle_insert.above = above
        if response == Gtk.ResponseType.OK:
            self._insert_subtitles(amount, above)
