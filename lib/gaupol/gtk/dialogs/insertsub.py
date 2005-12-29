# Copyright (C) 2005 Osmo Salomaa
#
# This file is part of Gaupol.
#
# Gaupol is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Gaupol is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Gaupol; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA


"""Dialog for inserting new subtitles."""


try:
    from psyco.classes import *
except ImportError:
    pass

import gtk

from gaupol.gtk.util import gui


class InsertSubtitleDialog(object):

    """Dialog for inserting new subtitles."""

    def __init__(self, parent):

        glade_xml = gui.get_glade_xml('insertsub-dialog.glade')
        get_widget = glade_xml.get_widget

        self._dialog             = get_widget('dialog')
        self._position_label     = get_widget('position_label')
        self._position_combo_box = get_widget('position_combo_box')
        self._amount_spin_button = get_widget('amount_spin_button')

        self._dialog.set_transient_for(parent)
        self._dialog.set_default_response(gtk.RESPONSE_OK)

        # Set mnemonics.
        self._position_label.set_mnemonic_widget(self._position_combo_box)
        amount_label = get_widget('amount_label')
        amount_label.set_mnemonic_widget(self._amount_spin_button)

    def destroy(self):
        """Destroy the dialog."""

        self._dialog.destroy()

    def get_amount(self):
        """Get amount of subtitles to insert."""

        self._amount_spin_button.update()
        return self._amount_spin_button.get_value_as_int()

    def get_position(self):
        """
        Get position to insert subtitles to.

        Return Position.ABOVE or Position.BELOW.
        """
        # ComboBox entry index corresponds to values of constants
        # Position.ABOVE and Position.BELOW.
        return self._position_combo_box.get_active()

    def run(self):
        """Show and run the dialog."""

        self._dialog.show()
        return self._dialog.run()

    def set_amount(self, value):
        """Set amount of subtitles to insert."""

        self._amount_spin_button.set_value(value)

    def set_position(self, position):
        """
        Set position to insert subtitles to.

        position: POSITION.ABOVE or POSITION.BELOW
        """
        # ComboBox entry index corresponds to values of constants
        # Position.ABOVE and Position.BELOW.
        self._position_combo_box.set_active(position)

    def set_position_sensitive(self, sensitive):
        """
        Set sensitivity of position-selecting.

        If no subtitles exist, the position-selecting becomes pointless and
        can be disabled.
        """
        self._position_label.set_sensitive(sensitive)
        self._position_combo_box.set_sensitive(sensitive)
