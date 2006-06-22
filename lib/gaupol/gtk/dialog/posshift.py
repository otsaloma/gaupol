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


"""Dialogs for shifting positions."""


from gettext import gettext as _

import gobject
import gtk

from gaupol.gtk      import cons
from gaupol.gtk.util import conf, gtklib


class _PositionShiftDialog(gobject.GObject):

    """Base class for dialogs for shifting positions."""

    __gsignals__ = {
        'preview': (
            gobject.SIGNAL_RUN_LAST,
            None,
            (int,)
        ),
    }

    def __init__(self, parent, page):

        gobject.GObject.__init__(self)

        self._page = page

        glade_xml = gtklib.get_glade_xml('posshift-dialog')
        self._amount_spin    = glade_xml.get_widget('amount_spin')
        self._current_radio  = glade_xml.get_widget('current_radio')
        self._dialog         = glade_xml.get_widget('dialog')
        self._preview_button = glade_xml.get_widget('preview_button')
        self._selected_radio = glade_xml.get_widget('selected_radio')
        self._unit_label     = glade_xml.get_widget('unit_label')

        self._init_widgets()
        self._init_data()
        self._init_sensitivities()
        self._init_signals()
        self._dialog.set_transient_for(parent)
        self._dialog.set_default_response(gtk.RESPONSE_OK)

    def _init_sensitivities(self):
        """Initialize widget sensitivities."""

        if self._page.project.video_path is None:
            self._preview_button.set_sensitive(False)
        if self._page.project.main_file is None:
            self._preview_button.set_sensitive(False)

        if not self._page.view.get_selected_rows():
            self._current_radio.set_active(True)
            self._selected_radio.set_sensitive(False)

    def _init_signals(self):
        """Initialize signals."""

        gtklib.connect(self, '_dialog'        , 'response')
        gtklib.connect(self, '_preview_button', 'clicked' )

    def _on_preview_button_clicked(self, *args):
        """Preview changes."""

        target = self.get_target()
        if target == cons.Target.CURRENT:
            row = 0
        elif target == cons.Target.SELECTED:
            row = self._page.view.get_selected_rows()[0]
        self.emit('preview', row)

    def destroy(self):
        """Destroy dialog."""

        self._dialog.destroy()

    def get_target(self):
        """Get target."""

        if self._current_radio.get_active():
            return cons.Target.CURRENT
        elif self._selected_radio.get_active():
            return cons.Target.SELECTED

    def run(self):
        """Run dialog."""

        self._dialog.show()
        return self._dialog.run()


class FrameShiftDialog(_PositionShiftDialog):

    """Dialog for shifting frames."""

    def _init_widgets(self):
        """Initialize widgets."""

        self._amount_spin.set_numeric(True)
        self._amount_spin.set_digits(0)
        self._amount_spin.set_increments(1, 10)
        self._amount_spin.set_range(-9999999, 9999999)
        self._unit_label.set_text(_('frames'))

    def _init_data(self):
        """Initialize default values."""

        self._amount_spin.set_value(conf.position_shift.frames)

        target = conf.position_shift.target
        self._current_radio.set_active(target == cons.Target.CURRENT)
        self._selected_radio.set_active(target == cons.Target.SELECTED)

    def _on_dialog_response(self, dialog, response):
        """Save settings."""

        if response == gtk.RESPONSE_OK:
            conf.position_shift.frames = self.get_amount()
            conf.position_shift.target = self.get_target()

    def get_amount(self):
        """Get frames."""

        return self._amount_spin.get_value_as_int()


class TimeShiftDialog(_PositionShiftDialog):

    """Dialog for shifting times."""

    def _init_widgets(self):
        """Initialize widgets."""

        self._amount_spin.set_numeric(True)
        self._amount_spin.set_digits(3)
        self._amount_spin.set_increments(0.1, 1)
        self._amount_spin.set_range(-99999, 99999)
        self._unit_label.set_text(_('seconds'))

    def _init_data(self):
        """Initialize default values."""

        self._amount_spin.set_value(conf.position_shift.seconds)

        target = conf.position_shift.target
        self._current_radio.set_active(target == cons.Target.CURRENT)
        self._selected_radio.set_active(target == cons.Target.SELECTED)

    def _on_dialog_response(self, dialog, response):
        """Save settings."""

        if response == gtk.RESPONSE_OK:
            conf.position_shift.seconds = self.get_amount()
            conf.position_shift.target  = self.get_target()

    def get_amount(self):
        """Get seconds."""

        return self._amount_spin.get_value()
