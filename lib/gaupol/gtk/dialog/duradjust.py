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


"""Dialog for adjusting durations."""


import gtk

from gaupol.gtk      import cons
from gaupol.gtk.util import config, gtklib


class DurationAdjustDialog(object):

    """Dialog for adjusting positions."""

    def __init__(self, parent, has_selection):

        glade_xml = gtklib.get_glade_xml('duradjust-dialog')
        self._all_radio      = glade_xml.get_widget('all_radio')
        self._current_radio  = glade_xml.get_widget('current_radio')
        self._dialog         = glade_xml.get_widget('dialog')
        self._gap_check      = glade_xml.get_widget('gap_check')
        self._gap_spin       = glade_xml.get_widget('gap_spin')
        self._lengthen_check = glade_xml.get_widget('lengthen_check')
        self._max_check      = glade_xml.get_widget('max_check')
        self._max_spin       = glade_xml.get_widget('max_spin')
        self._min_check      = glade_xml.get_widget('min_check')
        self._min_spin       = glade_xml.get_widget('min_spin')
        self._optimal_spin   = glade_xml.get_widget('optimal_spin')
        self._selected_radio = glade_xml.get_widget('selected_radio')
        self._shorten_check  = glade_xml.get_widget('shorten_check')

        self._init_sensitivities(has_selection)
        self._init_signals()
        self._init_data()
        self._dialog.set_transient_for(parent)
        self._dialog.set_default_response(gtk.RESPONSE_OK)

    def _init_data(self):
        """Initialize default values."""

        self._gap_check.set_active(config.duration_adjust.use_gap)
        self._gap_spin.set_value(config.duration_adjust.gap)
        self._lengthen_check.set_active(config.duration_adjust.lengthen)
        self._max_check.set_active(config.duration_adjust.use_max)
        self._max_spin.set_value(config.duration_adjust.max)
        self._min_check.set_active(config.duration_adjust.use_min)
        self._min_spin.set_value(config.duration_adjust.min)
        self._optimal_spin.set_value(config.duration_adjust.optimal)
        self._shorten_check.set_active(config.duration_adjust.shorten)

        target = config.duration_adjust.target
        self._all_radio.set_active(target == cons.Target.ALL)
        self._current_radio.set_active(target == cons.Target.CURRENT)
        self._selected_radio.set_active(target == cons.Target.SELECTED)

    def _init_sensitivities(self, has_selection):
        """Initialize widget sensitivities."""

        self._gap_spin.set_sensitive(False)
        self._max_spin.set_sensitive(False)
        self._min_spin.set_sensitive(False)
        self._optimal_spin.set_sensitive(False)
        self._selected_radio.set_sensitive(has_selection)

    def _init_signals(self):
        """Initialize signals."""

        gtklib.connect(self, '_dialog'        , 'response')
        gtklib.connect(self, '_gap_check'     , 'toggled' )
        gtklib.connect(self, '_lengthen_check', 'toggled' )
        gtklib.connect(self, '_max_check'     , 'toggled' )
        gtklib.connect(self, '_min_check'     , 'toggled' )
        gtklib.connect(self, '_shorten_check' , 'toggled' )

    def _on_dialog_response(self, dialog, response):
        """Save settings before emitting response."""

        if response != gtk.RESPONSE_OK:
            return

        config.duration_adjust.gap      = self.get_gap()
        config.duration_adjust.lengthen = self.get_lengthen()
        config.duration_adjust.max      = self.get_maximum()
        config.duration_adjust.min      = self.get_minimum()
        config.duration_adjust.optimal  = self.get_optimal()
        config.duration_adjust.shorten  = self.get_shorten()
        config.duration_adjust.target   = self.get_target()
        config.duration_adjust.use_gap  = self.get_use_gap()
        config.duration_adjust.use_max  = self.get_use_maximum()
        config.duration_adjust.use_min  = self.get_use_minimum()

    def _on_gap_check_toggled(self, check_button):
        """Set gap spin button sensitivity."""

        self._gap_spin.set_sensitive(check_button.get_active())

    def _on_lengthen_check_toggled(self, *args):
        """Set optimal spin button sensitivity."""

        self._optimal_spin.set_sensitive(True in (
            self._lengthen_check.get_active(),
            self._shorten_check.get_active()
        ))

    def _on_max_check_toggled(self, check_button):
        """Set maximum spin button sensitivity."""

        self._max_spin.set_sensitive(check_button.get_active())

    def _on_min_check_toggled(self, check_button):
        """Set minimum spin button sensitivity."""

        self._min_spin.set_sensitive(check_button.get_active())

    def _on_shorten_check_toggled(self, *args):
        """Set optimal spin button sensitivity."""

        self._optimal_spin.set_sensitive(True in (
            self._lengthen_check.get_active(),
            self._shorten_check.get_active()
        ))

    def destroy(self):
        """Destroy dialog."""

        self._dialog.destroy()

    def get_gap(self):
        """Get gap."""

        return self._gap_spin.get_value()

    def get_lengthen(self):
        """Return True if allow lengthening."""

        return self._lengthen_check.get_active()

    def get_maximum(self):
        """Get maximum."""

        return self._max_spin.get_value()

    def get_minimum(self):
        """Get minimum."""

        return self._min_spin.get_value()

    def get_optimal(self):
        """Get optimal."""

        return self._optimal_spin.get_value()

    def get_shorten(self):
        """Return True if allow shortening."""

        return self._shorten_check.get_active()

    def get_target(self):
        """Get target."""

        if self._all_radio.get_active():
            return cons.Target.ALL
        elif self._current_radio.get_active():
            return cons.Target.CURRENT
        elif self._selected_radio.get_active():
            return cons.Target.SELECTED

    def get_use_gap(self):
        """Return True if use gap."""

        return self._gap_check.get_active()

    def get_use_maximum(self):
        """Return True if use maximum."""

        return self._max_check.get_active()

    def get_use_minimum(self):
        """Return True if use minimum."""

        return self._min_check.get_active()

    def run(self):
        """Run dialog."""

        self._dialog.show()
        return self._dialog.run()
