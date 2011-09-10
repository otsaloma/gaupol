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

"""Dialog for inserting new subtitles."""

import aeidon
import gaupol
import gtk
_ = aeidon.i18n._

__all__ = ("InsertDialog",)


class InsertDialog(gaupol.BuilderDialog):

    """Dialog for inserting new subtitles."""

    _widgets = ("amount_spin", "position_combo", "position_label")

    def __init__(self, parent, application):
        """Initialize an :class:`InsertDialog` object."""
        gaupol.BuilderDialog.__init__(self, "insert-dialog.ui")
        self.application = application
        self._init_position_combo()
        self._init_values()
        self._dialog.set_transient_for(parent)
        self._dialog.set_default_response(gtk.RESPONSE_OK)

    def _init_position_combo(self):
        """Initialize the position combo box."""
        store = gtk.ListStore(str)
        self._position_combo.set_model(store)
        store.append((_("Above selection"),))
        store.append((_("Below selection"),))
        renderer = gtk.CellRendererText()
        self._position_combo.pack_start(renderer, True)
        self._position_combo.add_attribute(renderer, "text", 0)

    def _init_values(self):
        """Initialize default values for widgets."""
        self._amount_spin.set_value(1)
        index = (0 if gaupol.conf.subtitle_insert.above else 1)
        self._position_combo.set_active(index)
        page = self.application.get_current_page()
        sensitive = bool(page.project.subtitles)
        self._position_combo.set_sensitive(sensitive)
        self._position_label.set_sensitive(sensitive)

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
        above = (self._position_combo.get_active() == 0)
        gaupol.conf.subtitle_insert.above = above
        if response == gtk.RESPONSE_OK:
            self._insert_subtitles(amount, above)
