# Copyright (C) 2005-2008,2010 Osmo Salomaa
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

import aeidon
import gaupol
from gi.repository import Gtk
_ = aeidon.i18n._

__all__ = ("DurationAdjustDialog",)


class DurationAdjustDialog(gaupol.BuilderDialog):

    """Dialog for lengthening or shortening durations."""

    _widgets = ("all_radio",
                "current_radio",
                "gap_check",
                "gap_spin",
                "lengthen_check",
                "max_check",
                "max_spin",
                "min_check",
                "min_spin",
                "selected_radio",
                "shorten_check",
                "speed_spin")

    def __init__(self, parent, application):
        """Initialize a :class:`DurationAdjustDialog` object."""
        gaupol.BuilderDialog.__init__(self, "duration-dialog.ui")
        self.application = application
        self._init_values()
        self._init_sensitivities()
        self._dialog.set_transient_for(parent)
        self._dialog.set_default_response(Gtk.ResponseType.OK)

    def _adjust_durations(self):
        """Adjust durations of subtitles."""
        conf = gaupol.conf.duration_adjust
        target = self._get_target()
        for page in self.application.get_target_pages(target):
            self.application.set_current_page(page)
            rows = page.project.adjust_durations(
                indices=self.application.get_target_rows(target),
                speed=conf.speed,
                lengthen=conf.lengthen,
                shorten=conf.shorten,
                maximum=(conf.maximum if conf.use_maximum else None),
                minimum=(conf.minimum if conf.use_minimum else None),
                gap=(conf.gap if conf.use_gap else None))

            self.application.flash_message(aeidon.i18n.ngettext(
                    "Adjusted duration of %d subtitle",
                    "Adjusted durations of %d subtitles",
                    len(rows)) % len(rows))

    def _get_target(self):
        """Return the selected target."""
        if self._selected_radio.get_active():
            return gaupol.targets.SELECTED
        if self._current_radio.get_active():
            return gaupol.targets.CURRENT
        if self._all_radio.get_active():
            return gaupol.targets.ALL
        raise ValueError("Invalid target radio state")

    def _init_sensitivities(self):
        """Initialize sensitivities of widgets."""
        self._all_radio.emit("toggled")
        self._current_radio.emit("toggled")
        self._gap_check.emit("toggled")
        self._gap_spin.emit("value-changed")
        self._lengthen_check.emit("toggled")
        self._max_check.emit("toggled")
        self._max_spin.emit("value-changed")
        self._min_check.emit("toggled")
        self._min_spin.emit("value-changed")
        self._selected_radio.emit("toggled")
        self._shorten_check.emit("toggled")
        self._speed_spin.emit("value-changed")

    def _init_values(self):
        """Intialize default values for widgets."""
        conf = gaupol.conf.duration_adjust
        self._gap_check.set_active(conf.use_gap)
        self._gap_spin.set_value(conf.gap)
        self._lengthen_check.set_active(conf.lengthen)
        self._max_check.set_active(conf.use_maximum)
        self._max_spin.set_value(conf.maximum)
        self._min_check.set_active(conf.use_minimum)
        self._min_spin.set_value(conf.minimum)
        self._shorten_check.set_active(conf.shorten)
        self._speed_spin.set_value(conf.speed)
        self._selected_radio.set_active(conf.target == gaupol.targets.SELECTED)
        self._current_radio.set_active(conf.target == gaupol.targets.CURRENT)
        self._all_radio.set_active(conf.target == gaupol.targets.ALL)
        page = self.application.get_current_page()
        rows = page.view.get_selected_rows()
        if (not rows) and (conf.target == gaupol.targets.SELECTED):
            self._current_radio.set_active(True)
        self._selected_radio.set_sensitive(bool(rows))

    def _on_gap_check_toggled(self, check_button):
        """Set sensitivity of the gap spin button."""
        self._gap_spin.set_sensitive(check_button.get_active())

    def _on_lengthen_check_toggled(self, *args):
        """Set sensitivity of the speed spin button."""
        lengthen = self._lengthen_check.get_active()
        shorten = self._shorten_check.get_active()
        self._speed_spin.set_sensitive(lengthen or shorten)

    def _on_max_check_toggled(self, check_button):
        """Set sensitivity of the maximum spin button."""
        self._max_spin.set_sensitive(check_button.get_active())

    def _on_min_check_toggled(self, check_button):
        """Set sensitivity of the minimum spin button."""
        self._min_spin.set_sensitive(check_button.get_active())

    def _on_response(self, dialog, response):
        """Save settings and adjust durations."""
        conf = gaupol.conf.duration_adjust
        conf.gap = self._gap_spin.get_value()
        conf.lengthen = self._lengthen_check.get_active()
        conf.maximum = self._max_spin.get_value()
        conf.minimum = self._min_spin.get_value()
        conf.speed = self._speed_spin.get_value()
        conf.shorten = self._shorten_check.get_active()
        conf.target = self._get_target()
        conf.use_gap = self._gap_check.get_active()
        conf.use_maximum = self._max_check.get_active()
        conf.use_minimum = self._min_check.get_active()
        if response == Gtk.ResponseType.OK:
            self._adjust_durations()

    def _on_shorten_check_toggled(self, *args):
        """Set sensitivity of the speed spin button."""
        lengthen = self._lengthen_check.get_active()
        shorten = self._shorten_check.get_active()
        self._speed_spin.set_sensitive(lengthen or shorten)
