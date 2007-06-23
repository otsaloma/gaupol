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


"""Dialogs for shifting positions."""


import gaupol.gtk
import gtk
_ = gaupol.i18n._

from .glade import GladeDialog


class _PositionShiftDialog(GladeDialog):

    """Base class for dialogs for shifting positions."""

    def __init__(self, parent, application):

        GladeDialog.__init__(self, "shift-dialog")
        get_widget = self._glade_xml.get_widget
        self._amount_spin = get_widget("amount_spin")
        self._current_radio = get_widget("current_radio")
        self._preview_button = get_widget("preview_button")
        self._selected_radio = get_widget("selected_radio")
        self._unit_label = get_widget("unit_label")
        self.application = application

        self._init_widgets()
        self._init_signal_handlers()
        self._init_values()
        self._dialog.set_transient_for(parent)
        self._dialog.set_default_response(gtk.RESPONSE_OK)

    def _get_preview_row(self):
        """Get the row to start preview from."""

        target = self._get_target()
        if target == gaupol.gtk.TARGET.SELECTED:
            page = self.application.get_current_page()
            return page.view.get_selected_rows()[0]
        return 0

    def _get_target(self):
        """Get the selected target."""

        if self._selected_radio.get_active():
            return gaupol.gtk.TARGET.SELECTED
        if self._current_radio.get_active():
            return gaupol.gtk.TARGET.CURRENT
        raise ValueError

    def _init_signal_handlers(self):
        """Initialize signal handlers."""

        gaupol.gtk.util.connect(self, "_amount_spin", "value-changed")
        gaupol.gtk.util.connect(self, "_preview_button", "clicked" )
        gaupol.gtk.util.connect(self, self, "response")

    def _init_values(self):
        """Intialize default values for widgets."""

        TARGET = gaupol.gtk.TARGET
        target = gaupol.gtk.conf.position_shift.target
        self._selected_radio.set_active(target == TARGET.SELECTED)
        self._current_radio.set_active(target == TARGET.CURRENT)
        page = self.application.get_current_page()
        rows = page.view.get_selected_rows()
        if (not rows) and (target == TARGET.SELECTED):
            self._current_radio.set_active(True)
            self._selected_radio.set_sensitive(False)
        if page.project.video_path is None:
            self._preview_button.set_sensitive(False)
        if page.project.main_file is None:
            self._preview_button.set_sensitive(False)
        self._amount_spin.emit("value-changed")

    def _on_amount_spin_value_changed(self, spin_button):
        """Set the response sensitivity."""

        sensitive = (spin_button.get_value() != 0.0)
        self.set_response_sensitive(gtk.RESPONSE_OK, sensitive)

    def _on_preview_button_clicked(self, *args):
        """Preview  a temporary file with shifted subtitles."""

        page = self.application.get_current_page()
        row = self._get_preview_row()
        target = self._get_target()
        rows = self.application.get_target_rows(target)
        doc = gaupol.gtk.DOCUMENT.MAIN
        method = self._get_shift_method()
        args = (rows, self._get_amount())
        self.application.preview_changes(page, row, doc, method, args)

    @gaupol.gtk.util.asserted_return
    def _on_response(self, dialog, response):
        """Save settings and shift positions."""

        domain = gaupol.gtk.conf.position_shift
        domain.target = self._get_target()
        assert response == gtk.RESPONSE_OK
        self._shift_positions()

    def _shift_positions(self):
        """Shift positions in subtitles."""

        page = self.application.get_current_page()
        target = self._get_target()
        rows = self.application.get_target_rows(target)
        amount = self._get_amount()
        page.project.shift_positions(rows, amount)


class FrameShiftDialog(_PositionShiftDialog):

    """Dialog for shifting frames."""

    __metaclass__ = gaupol.Contractual

    def _get_amount_ensure(self, value):
        assert isinstance(value, int)

    def _get_amount(self):
        """Get the amount of frames to shift."""

        return self._amount_spin.get_value_as_int()

    def _init_widgets(self):
        """Initialize the widgets."""

        self._amount_spin.set_numeric(True)
        self._amount_spin.set_digits(0)
        self._amount_spin.set_increments(1, 10)
        self._amount_spin.set_range(-9999999, 9999999)
        self._amount_spin.set_value(0)
        self._unit_label.set_text(_("frames"))


class TimeShiftDialog(_PositionShiftDialog):

    """Dialog for shifting times."""

    __metaclass__ = gaupol.Contractual

    def _get_amount_ensure(self, value):
        assert isinstance(value, float)

    def _get_amount(self):
        """Get the amount of seconds to shift."""

        return self._amount_spin.get_value()

    def _init_widgets(self):
        """Initialize the widgets."""

        self._amount_spin.set_numeric(True)
        self._amount_spin.set_digits(3)
        self._amount_spin.set_increments(0.1, 1)
        self._amount_spin.set_range(-99999, 99999)
        self._amount_spin.set_value(0.000)
        self._unit_label.set_text(_("seconds"))
