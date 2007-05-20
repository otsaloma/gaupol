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


import gtk

from gaupol.gtk import conf, const, util
from gaupol.gtk.i18n import _
from .glade import GladeDialog


class _PositionShiftDialog(GladeDialog):

    """Base class for dialogs for shifting positions.

    Instance variables:

        _amount_spin:    gtk.SpinButton
        _current_radio:  gtk.RadioButton
        _preview_button: gtk.Button
        _selected_radio: gtk.RadioButton
        _unit_label:     gtk.Label
        application:     Associated Application
    """

    def __init__(self, parent, application):

        GladeDialog.__init__(self, "posshift-dialog")
        get_widget = self._glade_xml.get_widget
        self._amount_spin    = get_widget("amount_spin")
        self._current_radio  = get_widget("current_radio")
        self._preview_button = get_widget("preview_button")
        self._selected_radio = get_widget("selected_radio")
        self._unit_label     = get_widget("unit_label")
        self.application = application

        self._init_widgets()
        self._init_signal_handlers()
        self._init_data()
        self._dialog.set_transient_for(parent)
        self._dialog.set_default_response(gtk.RESPONSE_OK)

    def _get_preview_row(self):
        """Get the row to start preview from."""

        target = self._get_target()
        if target == const.TARGET.SELECTED:
            page = self.application.get_current_page()
            return page.view.get_selected_rows()[0]
        return 0

    def _get_target(self):
        """Get the selected target."""

        if self._selected_radio.get_active():
            return const.TARGET.SELECTED
        if self._current_radio.get_active():
            return const.TARGET.CURRENT
        raise ValueError

    def _get_target_rows(self):
        """Get rows corresponding to target."""

        target = self._get_target()
        if target == const.TARGET.SELECTED:
            page = self.application.get_current_page()
            return page.view.get_selected_rows()
        return None

    def _init_data(self):
        """Intialize default values for widgets."""

        target = conf.position_shift.target
        self._selected_radio.set_active(target == const.TARGET.SELECTED)
        self._current_radio.set_active(target == const.TARGET.CURRENT)

        page = self.application.get_current_page()
        rows = page.view.get_selected_rows()
        if not rows and target == const.TARGET.SELECTED:
            self._current_radio.set_active(True)
            self._selected_radio.set_sensitive(False)

        if page.project.video_path is None:
            self._preview_button.set_sensitive(False)
        if page.project.main_file is None:
            self._preview_button.set_sensitive(False)

    def _init_signal_handlers(self):
        """Initialize signal handlers."""

        util.connect(self, "_preview_button", "clicked" )
        util.connect(self, self, "response")

    def _on_preview_button_clicked(self, *args):
        """Preview changes."""

        page = self.application.get_current_page()
        row = self._get_preview_row()
        doc = const.DOCUMENT.MAIN
        method = self._get_shift_method()
        args = [self._get_target_rows(), self._get_amount()]
        self.application.preview_changes(page, row, doc, method, args)

    @util.asserted_return
    def _on_response(self, dialog, response):
        """Save settings and shift positions."""

        conf.position_shift.target = self._get_target()
        assert response == gtk.RESPONSE_OK
        self._shift()

    def _shift(self):
        """Shift positions in subtitles."""

        method = self._get_shift_method()
        rows = self._get_target_rows()
        amount = self._get_amount()
        method(rows, amount)


class FrameShiftDialog(_PositionShiftDialog):

    """Dialog for shifting frames."""

    def _get_amount(self):
        """Get the amount of frames to shift."""

        return self._amount_spin.get_value_as_int()

    def _get_shift_method(self):
        """Get the project method to use for shifting."""

        page = self.application.get_current_page()
        return page.project.shift_frames

    def _init_widgets(self):
        """Initialize the widgets."""

        self._amount_spin.set_numeric(True)
        self._amount_spin.set_digits(0)
        self._amount_spin.set_increments(1, 10)
        self._amount_spin.set_range(-9999999, 9999999)
        self._unit_label.set_text(_("frames"))


class TimeShiftDialog(_PositionShiftDialog):

    """Dialog for shifting times."""

    def _get_amount(self):
        """Get the amount of seconds to shift."""

        return self._amount_spin.get_value()

    def _get_shift_method(self):
        """Get the project method to use for shifting."""

        page = self.application.get_current_page()
        return page.project.shift_seconds

    def _init_widgets(self):
        """Initialize the widgets."""

        self._amount_spin.set_numeric(True)
        self._amount_spin.set_digits(3)
        self._amount_spin.set_increments(0.1, 1)
        self._amount_spin.set_range(-99999, 99999)
        self._unit_label.set_text(_("seconds"))
