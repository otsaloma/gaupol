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


"""Dialog for inserting new subtitles."""


import gaupol.gtk
import gtk

from .glade import GladeDialog


class InsertDialog(GladeDialog):

    """Dialog for inserting new subtitles."""

    def __init__(self, parent, application):

        GladeDialog.__init__(self, "insert-dialog")
        get_widget = self._glade_xml.get_widget
        self._amount_spin = get_widget("amount_spin")
        self._position_combo = get_widget("position_combo")
        self._position_label = get_widget("position_label")
        self.application = application

        self._init_values()
        gaupol.gtk.util.connect(self, self, "response")
        self._dialog.set_transient_for(parent)
        self._dialog.set_default_response(gtk.RESPONSE_OK)

    def _init_values(self):
        """Initialize default values for widgets."""

        self._amount_spin.set_value(1)
        index = (0 if gaupol.gtk.conf.subtitle_insert.above else 1)
        self._position_combo.set_active(index)

        page = self.application.get_current_page()
        sensitive = bool(page.project.subtitles)
        self._position_combo.set_sensitive(sensitive)
        self._position_label.set_sensitive(sensitive)

    def _insert_subtitles(self, amount, above):
        """Insert amount of subtitles to project."""

        index = 0
        page = self.application.get_current_page()
        if page.project.subtitles:
            index = page.view.get_selected_rows()[0]
            index = (index + 1 if not above else index)
        indexes = range(index, index + amount)
        page.project.insert_blank_subtitles(indexes)

    @gaupol.gtk.util.asserted_return
    def _on_response(self, dialog, response):
        """Save values and insert subtitles."""

        amount = self._amount_spin.get_value_as_int()
        above = (self._position_combo.get_active() == 0)
        gaupol.gtk.conf.subtitle_insert.above = above
        assert response == gtk.RESPONSE_OK
        self._insert_subtitles(amount, above)
