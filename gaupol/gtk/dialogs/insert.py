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


"""Dialog for inserting new subtitles."""


import gtk

from gaupol.gtk import conf, util
from .glade import GladeDialog


class InsertDialog(GladeDialog):

    """Dialog for inserting new subtitles.

    Instance variables:

        _amount_spin:    gtk.SpinButton
        _position_combo: gtk.ComboBox
        _position_label: gtk.Label
        application:     Associated application
    """

    def __init__(self, parent, application):

        GladeDialog.__init__(self, "insert-dialog")
        self._amount_spin    = self._glade_xml.get_widget("amount_spin")
        self._position_combo = self._glade_xml.get_widget("position_combo")
        self._position_label = self._glade_xml.get_widget("position_label")
        self.application     = application

        self._init_data()
        self._init_signal_handlers()
        self._dialog.set_transient_for(parent)
        self._dialog.set_default_response(gtk.RESPONSE_OK)

    def _init_data(self):
        """Initialize default values for widgets."""

        self._amount_spin.set_value(conf.subtitle_insert.amount)
        active = (0 if conf.subtitle_insert.above else 1)
        self._position_combo.set_active(active)

        page = self.application.get_current_page()
        if not page.project.times:
            self._position_combo.set_sensitive(False)
            self._position_label.set_sensitive(False)

    def _init_signal_handlers(self):
        """Initialize signal handlers."""

        util.connect(self, self, "response")

    def _insert_subtitles(self, amount, above):
        """Insert subtitles."""

        row = 0
        page = self.application.get_current_page()
        if page.project.times:
            row = page.view.get_selected_rows()[0]
            if not above:
                row += 1
        rows = range(row, row + amount)
        page.project.insert_blank_subtitles(rows)

    def _on_response(self, dialog, response):
        """Save values and insert subtitles."""

        amount = self._amount_spin.get_value_as_int()
        above = (self._position_combo.get_active() == 0)
        conf.subtitle_insert.amount = amount
        conf.subtitle_insert.above = above
        if response == gtk.RESPONSE_OK:
            self._insert_subtitles(amount, above)
