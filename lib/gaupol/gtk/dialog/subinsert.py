# Copyright (C) 2005-2006 Osmo Salomaa
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

from gaupol.gtk.util import conf, gtklib


_ABOVE = 0
_BELOW = 1


class SubtitleInsertDialog(object):

    """Dialog for inserting new subtitles."""

    def __init__(self, parent, project):

        glade_xml = gtklib.get_glade_xml('subinsert-dialog')
        self._amount_spin    = glade_xml.get_widget('amount_spin')
        self._dialog         = glade_xml.get_widget('dialog')
        self._position_combo = glade_xml.get_widget('position_combo')
        self._position_label = glade_xml.get_widget('position_label')

        self._init_data(project)
        gtklib.connect(self, '_dialog', 'response')
        self._dialog.set_transient_for(parent)
        self._dialog.set_default_response(gtk.RESPONSE_OK)

    def _init_data(self, project):
        """Initialize default values."""

        self._amount_spin.set_value(conf.subtitle_insert.amount)

        if conf.subtitle_insert.above:
            self._position_combo.set_active(_ABOVE)
        else:
            self._position_combo.set_active(_BELOW)

        if not project.times:
            self._position_label.set_sensitive(False)
            self._position_combo.set_sensitive(False)

    def _init_signals(self):
        """Initialize signals."""

        gtklib.connect(self, '_amount_spin'   , 'value-changed')
        gtklib.connect(self, '_position_combo', 'changed'      )

    def _on_dialog_response(self, dialog, response):
        """Save settings."""

        if response == gtk.RESPONSE_OK:
            conf.subtitle_insert.amount = self.get_amount()
            conf.subtitle_insert.above  = self.get_above()

    def destroy(self):
        """Destroy dialog."""

        self._dialog.destroy()

    def get_above(self):
        """Return True if insert above selection."""

        return self._position_combo.get_active() == _ABOVE

    def get_amount(self):
        """Get amount of subtitles."""

        return self._amount_spin.get_value_as_int()

    def run(self):
        """Run dialog."""

        self._dialog.show()
        return self._dialog.run()
