# Copyright (C) 2005-2008 Osmo Salomaa
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

"""Dialog for lengthening or shortening durations."""

import gaupol.gtk
import gtk
_ = gaupol.i18n._

__all__ = ("DurationAdjustDialog",)


class DurationAdjustDialog(gaupol.gtk.GladeDialog):

    """Dialog for lengthening or shortening durations."""

    def __init__(self, parent, application):

        gaupol.gtk.GladeDialog.__init__(self, "duration.glade")
        get_widget = self._glade_xml.get_widget
        self._all_radio = get_widget("all_radio")
        self._current_radio = get_widget("current_radio")
        self._gap_check = get_widget("gap_check")
        self._gap_spin = get_widget("gap_spin")
        self._lengthen_check = get_widget("lengthen_check")
        self._max_check = get_widget("max_check")
        self._max_spin = get_widget("max_spin")
        self._min_check = get_widget("min_check")
        self._min_spin = get_widget("min_spin")
        self._optimal_spin = get_widget("optimal_spin")
        self._selected_radio = get_widget("selected_radio")
        self._shorten_check = get_widget("shorten_check")
        self.application = application
        self.conf = gaupol.gtk.conf.duration_adjust

        self._init_signal_handlers()
        self._init_values()
        self._init_sensitivities()
        self._dialog.set_transient_for(parent)
        self._dialog.set_default_response(gtk.RESPONSE_OK)

    def _adjust_durations(self):
        """Adjust durations in subtitles."""

        target = self._get_target()
        for page in self.application.get_target_pages(target):
            self.application.set_current_page(page)
            rows = page.project.adjust_durations(
                indices=self.application.get_target_rows(target),
                optimal=self.conf.optimal,
                lengthen=self.conf.lengthen,
                shorten=self.conf.shorten,
                maximum=(self.conf.maximum if self.conf.use_maximum else None),
                minimum=(self.conf.minimum if self.conf.use_minimum else None),
                gap=(self.conf.gap if self.conf.use_gap else None),)
            message = gaupol.i18n.ngettext(
                "Adjusted duration of %d subtitle",
                "Adjusted durations of %d subtitles",
                len(rows)) % len(rows)
            self.application.flash_message(message)

    def _get_target(self):
        """Return the selected target."""

        if self._selected_radio.get_active():
            return gaupol.gtk.targets.SELECTED
        if self._current_radio.get_active():
            return gaupol.gtk.targets.CURRENT
        if self._all_radio.get_active():
            return gaupol.gtk.targets.ALL
        raise ValueError

    def _init_sensitivities(self):
        """Initialize the sensitivities of widgets."""

        page = self.application.get_current_page()
        rows = page.view.get_selected_rows()
        target = self.conf.target
        if (not rows) and (target == gaupol.gtk.targets.SELECTED):
            self._current_radio.set_active(True)
        self._selected_radio.set_sensitive(bool(rows))

        self._all_radio.emit("toggled")
        self._current_radio.emit("toggled")
        self._gap_check.emit("toggled")
        self._gap_spin.emit("value-changed")
        self._lengthen_check.emit("toggled")
        self._max_check.emit("toggled")
        self._max_spin.emit("value-changed")
        self._min_check.emit("toggled")
        self._min_spin.emit("value-changed")
        self._optimal_spin.emit("value-changed")
        self._selected_radio.emit("toggled")
        self._shorten_check.emit("toggled")

    def _init_signal_handlers(self):
        """Initialize signal handlers."""

        gaupol.util.connect(self, "_gap_check", "toggled")
        gaupol.util.connect(self, "_lengthen_check", "toggled")
        gaupol.util.connect(self, "_max_check", "toggled")
        gaupol.util.connect(self, "_min_check", "toggled")
        gaupol.util.connect(self, "_shorten_check", "toggled")
        gaupol.util.connect(self, self, "response")

    def _init_values(self):
        """Intialize default values for widgets."""

        self._gap_check.set_active(self.conf.use_gap)
        self._gap_spin.set_value(self.conf.gap)
        self._lengthen_check.set_active(self.conf.lengthen)
        self._max_check.set_active(self.conf.use_maximum)
        self._max_spin.set_value(self.conf.maximum)
        self._min_check.set_active(self.conf.use_minimum)
        self._min_spin.set_value(self.conf.minimum)
        self._optimal_spin.set_value(self.conf.optimal)
        self._shorten_check.set_active(self.conf.shorten)

        targets = gaupol.gtk.targets
        self._selected_radio.set_active(self.conf.target == targets.SELECTED)
        self._current_radio.set_active(self.conf.target == targets.CURRENT)
        self._all_radio.set_active(self.conf.target == targets.ALL)

    def _on_gap_check_toggled(self, check_button):
        """Set the sensitivity of the gap spin button."""

        self._gap_spin.set_sensitive(check_button.get_active())

    def _on_lengthen_check_toggled(self, *args):
        """Set the sensitivity of the optimal spin button."""

        lengthen = self._lengthen_check.get_active()
        shorten = self._shorten_check.get_active()
        self._optimal_spin.set_sensitive(lengthen or shorten)

    def _on_max_check_toggled(self, check_button):
        """Set the sensitivity of the maximum spin button."""

        self._max_spin.set_sensitive(check_button.get_active())

    def _on_min_check_toggled(self, check_button):
        """Set the sensitivity of the minimum spin button."""

        self._min_spin.set_sensitive(check_button.get_active())

    def _on_response(self, dialog, response):
        """Save settings and adjust durations."""

        self.conf.gap = self._gap_spin.get_value()
        self.conf.lengthen = self._lengthen_check.get_active()
        self.conf.maximum = self._max_spin.get_value()
        self.conf.minimum = self._min_spin.get_value()
        self.conf.optimal = self._optimal_spin.get_value()
        self.conf.shorten = self._shorten_check.get_active()
        self.conf.target = self._get_target()
        self.conf.use_gap = self._gap_check.get_active()
        self.conf.use_maximum = self._max_check.get_active()
        self.conf.use_minimum = self._min_check.get_active()
        if response == gtk.RESPONSE_OK:
            self._adjust_durations()

    def _on_shorten_check_toggled(self, *args):
        """Set the sensitivity of the optimal spin button."""

        lengthen = self._lengthen_check.get_active()
        shorten = self._shorten_check.get_active()
        self._optimal_spin.set_sensitive(lengthen or shorten)
