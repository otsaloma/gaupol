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


"""Dialog for shifting timings."""


try:
    from psyco.classes import *
except ImportError:
    pass

from gettext import gettext as _

import gobject
import gtk

from gaupol.constants import Mode
from gaupol.gtk.util  import config, gtklib


class TimingShiftDialog(gobject.GObject):

    """Dialog for shifting timings."""

    __gsignals__ = {
        'preview': (
            gobject.SIGNAL_RUN_LAST,
            None,
            (int,)
        ),
    }

    def __init__(self, parent, page):

        gobject.GObject.__init__(self)

        glade_xml = gtklib.get_glade_xml('tmgshift-dialog.glade')
        get_widget = glade_xml.get_widget

        self._all_radio         = get_widget('all_radio_button')
        self._amount_spin       = get_widget('amount_spin_button')
        self._amount_unit_label = get_widget('amount_unit_label')
        self._dialog            = get_widget('dialog')
        self._preview_button    = get_widget('preview_button')
        self._selected_radio    = get_widget('selected_radio_button')

        self._page = page

        self._init_widgets()
        self._init_data()
        self._init_sensitivities()
        self._init_signals()

        self._dialog.set_transient_for(parent)
        self._dialog.set_default_response(gtk.RESPONSE_OK)

    def _init_data(self):
        """Initialize default values."""

        self._all_radio.set_active(config.timing_shift.all_subtitles)

        if self._page.edit_mode == Mode.TIME:
            value = float(config.timing_shift.seconds)
        elif self._page.edit_mode == Mode.FRAME:
            value = config.timing_shift.frames
        self._amount_spin.set_value(value)

    def _init_sensitivities(self):
        """Initialize widget sensitivities."""

        if self._page.project.video_path is None:
            self._preview_button.set_sensitive(False)
        if self._page.project.main_file is None:
            self._preview_button.set_sensitive(False)

        if not self._page.view.get_selected_rows():
            self._all_radio.set_active(True)
            self._selected_radio.set_sensitive(False)

    def _init_signals(self):
        """Initialize signals."""

        method = self._on_amount_spin_value_changed
        self._amount_spin.connect('value-changed', method)

        method = self._on_preview_button_clicked
        self._preview_button.connect('clicked', method)

        method = self._on_all_radio_toggled
        self._all_radio.connect('toggled', method)

    def _init_widgets(self):
        """Initialize widgets."""

        self._amount_spin.set_numeric(True)

        if self._page.edit_mode == Mode.TIME:
            self._amount_unit_label.set_text(_('seconds'))
            self._amount_spin.set_digits(3)
            self._amount_spin.set_increments(0.1, 1)
            self._amount_spin.set_range(-99999, 99999)

        elif self._page.edit_mode == Mode.FRAME:
            self._amount_unit_label.set_text(_('frames'))
            self._amount_spin.set_digits(0)
            self._amount_spin.set_increments(1, 10)
            self._amount_spin.set_range(-9999999, 9999999)

    def destroy(self):
        """Destroy the dialog."""

        self._dialog.destroy()

    def get_amount(self):
        """
        Get shift amount.

        Return seconds or frames depending on edit mode.
        """
        self._amount_spin.update()
        if self._page.edit_mode == Mode.TIME:
            return self._amount_spin.get_value()
        elif self._page.edit_mode == Mode.FRAME:
            return self._amount_spin.get_value_as_int()

    def get_shift_all(self):
        """Get shift all setting."""

        return self._all_radio.get_active()

    def _on_all_radio_toggled(self, radio_button):
        """Save radio button value."""

        config.timing_shift.all_subtitles = radio_button.get_active()

    def _on_amount_spin_value_changed(self, spin_button):
        """Save spin button value."""

        if self._page.edit_mode == Mode.TIME:
            config.timing_shift.seconds = '%.3f' % spin_button.get_value()
        elif self._page.edit_mode == Mode.FRAME:
            config.timing_shift.frames = spin_button.get_value_as_int()

    def _on_preview_button_clicked(self, *args):
        """Preview changes."""

        if self.get_shift_all():
            row = 0
        else:
            row = self._page.view.get_selected_rows()[0]

        self.emit('preview', row)

    def run(self):
        """Show and run the dialog."""

        self._dialog.show()
        return self._dialog.run()


if __name__ == '__main__':

    from gaupol.gtk.application import Application
    from gaupol.test            import Test

    class TestTimingShiftDialog(Test):

        def __init__(self):

            Test.__init__(self)
            self.application = Application()
            self.application.open_main_files([self.get_subrip_path()])
            self.page = self.application.get_current_page()
            self.dialog = TimingShiftDialog(gtk.Window(), self.page)

        def destroy(self):

            self.application.window.destroy()

        def test_get_amount(self):

            if self.page.edit_mode == Mode.TIME:
                assert isinstance(self.dialog.get_amount(), float)
            elif self.page.edit_mode == Mode.FRAME:
                assert isinstance(self.dialog.get_amount(), int)

        def test_get_shift_all(self):

            assert isinstance(self.dialog.get_shift_all(), bool)

        def test_signals(self):

            self.dialog._amount_spin.set_value(33)
            self.dialog._all_radio.set_active(True)
            self.dialog._all_radio.set_active(False)

    TestTimingShiftDialog().run()
