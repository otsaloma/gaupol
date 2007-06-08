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


"""Dialog for adjusting durations."""


import gtk

from gaupol.gtk import conf, const, util
from gaupol.gtk.i18n import _, ngettext
from .glade import GladeDialog


class DurationAdjustDialog(GladeDialog):

    """Dialog for adjusting positions.

    Instance variables:
        _all_radio:      gtk.RadioButton
        _current_radio:  gtk.RadioButton
        _gap_check:      gtk.CheckButton
        _gap_spin:       gtk.SpinButton
        _lengthen_check: gtk.CheckButton
        _max_check:      gtk.CheckButton
        _max_spin:       gtk.SpinButton
        _min_check:      gtk.CheckButton
        _min_spin:       gtk.SpinButton
        _optimal_spin:   gtk.SpinButton
        _selected_radio: gtk.RadioButton
        _shorten_check:  gtk.CheckButton
        application:     Associated Application
    """

    def __init__(self, parent, application):

        GladeDialog.__init__(self, "duradjust-dialog")
        get_widget = self._glade_xml.get_widget
        self._all_radio      = get_widget("all_radio")
        self._current_radio  = get_widget("current_radio")
        self._gap_check      = get_widget("gap_check")
        self._gap_spin       = get_widget("gap_spin")
        self._lengthen_check = get_widget("lengthen_check")
        self._max_check      = get_widget("max_check")
        self._max_spin       = get_widget("max_spin")
        self._min_check      = get_widget("min_check")
        self._min_spin       = get_widget("min_spin")
        self._optimal_spin   = get_widget("optimal_spin")
        self._selected_radio = get_widget("selected_radio")
        self._shorten_check  = get_widget("shorten_check")
        self.application = application

        self._init_signal_handlers()
        self._init_data()
        self._dialog.set_transient_for(parent)
        self._dialog.set_default_response(gtk.RESPONSE_OK)

    def _adjust(self):
        """Adjust durations in subtitles."""

        kwargs = {}
        kwargs["optimal"] = gaupol.gtk.conf.duration_adjust.optimal
        kwargs["lengthen"] = gaupol.gtk.conf.duration_adjust.lengthen
        kwargs["shorten"] = gaupol.gtk.conf.duration_adjust.shorten
        if gaupol.gtk.conf.duration_adjust.use_max:
            kwargs["maximum"] = gaupol.gtk.conf.duration_adjust.maximum
        if gaupol.gtk.conf.duration_adjust.use_min:
            kwargs["minimum"] = gaupol.gtk.conf.duration_adjust.minimum
        if gaupol.gtk.conf.duration_adjust.use_gap:
            kwargs["gap"] = gaupol.gtk.conf.duration_adjust.gap
        kwargs["rows"] = self._get_target_rows()

        for page in self._get_target_pages():
            index = self.application.pages.index(page)
            self.application.notebook.set_current_page(index)
            rows = page.project.adjust_durations(**kwargs)
            message = ngettext(
                "Adjusted duration of %d subtitle",
                "Adjusted durations of %d subtitles",
                len(rows)) % len(rows)
            self.application.push_message(message)

    def _get_target(self):
        """Get the selected target."""

        if self._selected_radio.get_active():
            return gaupol.gtk.TARGET.SELECTED
        if self._current_radio.get_active():
            return gaupol.gtk.TARGET.CURRENT
        if self._all_radio.get_active():
            return gaupol.gtk.TARGET.ALL
        raise ValueError

    def _get_target_pages(self):
        """Get pages corresponding to target."""

        target = self._get_target()
        if target == gaupol.gtk.TARGET.ALL:
            return self.application.pages
        return [self.application.get_current_page()]

    def _get_target_rows(self):
        """Get rows corresponding to target."""

        target = self._get_target()
        if target == gaupol.gtk.TARGET.SELECTED:
            page = self.application.get_current_page()
            return page.view.get_selected_rows()
        return None

    def _init_data(self):
        """Intialize default values for widgets."""

        self._gap_check.set_active(gaupol.gtk.conf.duration_adjust.use_gap)
        self._gap_spin.set_value(gaupol.gtk.conf.duration_adjust.gap)
        self._lengthen_check.set_active(gaupol.gtk.conf.duration_adjust.lengthen)
        self._max_check.set_active(gaupol.gtk.conf.duration_adjust.use_max)
        self._max_spin.set_value(gaupol.gtk.conf.duration_adjust.maximum)
        self._min_check.set_active(gaupol.gtk.conf.duration_adjust.use_min)
        self._min_spin.set_value(gaupol.gtk.conf.duration_adjust.minimum)
        self._optimal_spin.set_value(gaupol.gtk.conf.duration_adjust.optimal)
        self._shorten_check.set_active(gaupol.gtk.conf.duration_adjust.shorten)

        target = gaupol.gtk.conf.duration_adjust.target
        self._all_radio.set_active(target == gaupol.gtk.TARGET.ALL)
        self._current_radio.set_active(target == gaupol.gtk.TARGET.CURRENT)
        self._selected_radio.set_active(target == gaupol.gtk.TARGET.SELECTED)

        page = self.application.get_current_page()
        rows = page.view.get_selected_rows()
        if not rows and target == gaupol.gtk.TARGET.SELECTED:
            self._current_radio.set_active(True)
            self._selected_radio.set_sensitive(False)

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

        gaupol.gtk.util.connect(self, "_gap_check"     , "toggled")
        gaupol.gtk.util.connect(self, "_lengthen_check", "toggled")
        gaupol.gtk.util.connect(self, "_max_check"     , "toggled")
        gaupol.gtk.util.connect(self, "_min_check"     , "toggled")
        gaupol.gtk.util.connect(self, "_shorten_check" , "toggled")
        gaupol.gtk.util.connect(self, self, "response")

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

    @gaupol.gtk.util.asserted_return
    def _on_response(self, dialog, response):
        """Save settings and adjust durations."""

        gaupol.gtk.conf.duration_adjust.gap      = self._gap_spin.get_value()
        gaupol.gtk.conf.duration_adjust.lengthen = self._lengthen_check.get_active()
        gaupol.gtk.conf.duration_adjust.maximum  = self._max_spin.get_value()
        gaupol.gtk.conf.duration_adjust.minimum  = self._min_spin.get_value()
        gaupol.gtk.conf.duration_adjust.optimal  = self._optimal_spin.get_value()
        gaupol.gtk.conf.duration_adjust.shorten  = self._shorten_check.get_active()
        gaupol.gtk.conf.duration_adjust.target   = self._get_target()
        gaupol.gtk.conf.duration_adjust.use_gap  = self._gap_check.get_active()
        gaupol.gtk.conf.duration_adjust.use_max  = self._max_check.get_active()
        gaupol.gtk.conf.duration_adjust.use_min  = self._min_check.get_active()
        assert response == gtk.RESPONSE_OK
        self._adjust()

    def _on_shorten_check_toggled(self, *args):
        """Set the sensitivity of the optimal spin button."""

        lengthen = self._lengthen_check.get_active()
        shorten = self._shorten_check.get_active()
        self._optimal_spin.set_sensitive(lengthen or shorten)
