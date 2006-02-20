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


"""Dialog for adjusting durations."""


try:
    from psyco.classes import *
except ImportError:
    pass

import gobject
import gtk

from gaupol.gtk.util  import config, gtklib


class DurationAdjustDialog(object):

    """Dialog for adjusting timings."""

    def __init__(self, parent, page):

        glade_xml = gtklib.get_glade_xml('duradjust-dialog.glade')
        get = glade_xml.get_widget

        self._adjust_button      = get('adjust_button')
        self._dialog             = get('dialog')
        self._gap_check          = get('gap_check_button')
        self._gap_spin           = get('gap_spin_button')
        self._lengthen_check     = get('lengthen_check_button')
        self._max_check          = get('maximum_check_button')
        self._max_spin           = get('maximum_spin_button')
        self._min_check          = get('minimum_check_button')
        self._min_spin           = get('minimum_spin_button')
        self._optimal_spin       = get('optimal_spin_button')
        self._prj_all_radio      = get('projects_all_radio_button')
        self._prj_current_radio  = get('projects_current_radio_button')
        self._shorten_check      = get('shorten_check_button')
        self._sub_all_radio      = get('subtitles_all_radio_button')
        self._sub_selected_radio = get('subtitles_selected_radio_button')

        self._init_sensitivities(page)
        self._init_signals()
        self._init_data()

        self._dialog.set_transient_for(parent)
        self._dialog.set_default_response(gtk.RESPONSE_OK)

    def _init_data(self):
        """Initialize default values."""

        self._optimal_spin.set_value(float(config.duration_adjust.optimal))
        self._min_spin.set_value(float(config.duration_adjust.minimum))
        self._max_spin.set_value(float(config.duration_adjust.maximum))
        self._gap_spin.set_value(float(config.duration_adjust.gap))

        self._lengthen_check.set_active(config.duration_adjust.lengthen)
        self._shorten_check.set_active(config.duration_adjust.shorten)
        self._min_check.set_active(config.duration_adjust.use_minimum)
        self._max_check.set_active(config.duration_adjust.use_maximum)
        self._gap_check.set_active(config.duration_adjust.use_gap)
        self._prj_all_radio.set_active(config.duration_adjust.all_projects)
        self._sub_all_radio.set_active(config.duration_adjust.all_subtitles)

    def _init_sensitivities(self, page):
        """Initialize widget sensitivities."""

        if not page.view.get_selected_rows():
            self._sub_all_radio.set_active(True)
            self._sub_selected_radio.set_sensitive(False)

    def _init_signals(self):
        """Initialize signals."""

        connections = (
            ('_gap_check'     , 'toggled'      ),
            ('_gap_spin'      , 'value-changed'),
            ('_lengthen_check', 'toggled'      ),
            ('_max_check'     , 'toggled'      ),
            ('_max_spin'      , 'value-changed'),
            ('_min_check'     , 'toggled'      ),
            ('_min_spin'      , 'value-changed'),
            ('_optimal_spin'  , 'value-changed'),
            ('_prj_all_radio' , 'toggled'      ),
            ('_shorten_check' , 'toggled'      ),
            ('_sub_all_radio' , 'toggled'      ),
        )

        for widget, signal in connections:
            method = '_on' + widget + '_' + signal.replace('-', '_')
            widget = getattr(self, widget)
            method = getattr(self, method)
            widget.connect(signal, method)

    def destroy(self):
        """Destroy the dialog."""

        self._dialog.destroy()

    def get_all_projects(self):
        """Get all projects setting."""

        return self._prj_all_radio.get_active()

    def get_all_subtitles(self):
        """Get all subtitles setting."""

        return self._sub_all_radio.get_active()

    def get_gap(self):
        """Get gap setting."""

        return self._gap_spin.get_value()

    def get_lengthen(self):
        """Get lengthen setting."""

        return self._lengthen_check.get_active()

    def get_maximum(self):
        """Get maximum setting."""

        return self._max_spin.get_value()

    def get_minimum(self):
        """Get minimum setting."""

        return self._min_spin.get_value()

    def get_optimal(self):
        """Get optimal setting."""

        return self._optimal_spin.get_value()

    def get_shorten(self):
        """Get shorten setting."""

        return self._shorten_check.get_active()

    def get_use_gap(self):
        """Get use gap setting."""

        return self._gap_check.get_active()

    def get_use_maximum(self):
        """Get use maximum setting."""

        return self._max_check.get_active()

    def get_use_minimum(self):
        """Get use minimum setting."""

        return self._min_check.get_active()

    def _on_gap_check_toggled(self, check_button):
        """Save use gap setting."""

        config.duration_adjust.use_gap = check_button.get_active()
        self._set_adjust_button_sensitivity()

    def _on_gap_spin_value_changed(self, spin_button):
        """Save gap setting."""

        config.duration_adjust.gap = '%.3f' % spin_button.get_value()

    def _on_lengthen_check_toggled(self, check_button):
        """Save lengthen setting."""

        config.duration_adjust.lengthen = check_button.get_active()
        self._set_adjust_button_sensitivity()

    def _on_max_check_toggled(self, check_button):
        """Save use maximum setting."""

        config.duration_adjust.use_maximum = check_button.get_active()
        self._set_adjust_button_sensitivity()

    def _on_max_spin_value_changed(self, spin_button):
        """Save maximum setting."""

        config.duration_adjust.maximum = '%.3f' % spin_button.get_value()

    def _on_min_check_toggled(self, check_button):
        """Save use minimum setting."""

        config.duration_adjust.use_minimum = check_button.get_active()
        self._set_adjust_button_sensitivity()

    def _on_min_spin_value_changed(self, spin_button):
        """Save minimum setting."""

        config.duration_adjust.minimum = '%.3f' % spin_button.get_value()

    def _on_optimal_spin_value_changed(self, spin_button):
        """Save optimal setting."""

        config.duration_adjust.optimal = '%.3f' % spin_button.get_value()

    def _on_prj_all_radio_toggled(self, radio_button):
        """Save all projects setting."""

        config.duration_adjust.all_projects = radio_button.get_active()

    def _on_shorten_check_toggled(self, check_button):
        """Save shorten setting."""

        config.duration_adjust.shorten = check_button.get_active()
        self._set_adjust_button_sensitivity()

    def _on_sub_all_radio_toggled(self, radio_button):
        """Save all subtitles setting."""

        config.duration_adjust.all_subtitles = radio_button.get_active()

    def run(self):
        """Show and run the dialog."""

        self._dialog.show()
        return self._dialog.run()

    def _set_adjust_button_sensitivity(self):
        """Set sensitivity of the adjust button."""

        actions = (
            self.get_lengthen(),
            self.get_shorten(),
            self.get_use_gap(),
            self.get_use_maximum(),
            self.get_use_minimum(),
        )

        self._adjust_button.set_sensitive(True in actions)


if __name__ == '__main__':

    from gaupol.gtk.application import Application
    from gaupol.test            import Test

    class TestDurationAdjustDialog(Test):

        def __init__(self):

            Test.__init__(self)
            self.application = Application()
            self.application.open_main_files([self.get_subrip_path()])
            self.page = self.application.get_current_page()
            self.dialog = DurationAdjustDialog(gtk.Window(), self.page)

        def destroy(self):

            self.application.window.destroy()

        def test_gets(self):

            gets = (
                ('get_all_projects' , bool ),
                ('get_all_subtitles', bool ),
                ('get_gap'          , float),
                ('get_lengthen'     , bool ),
                ('get_maximum'      , float),
                ('get_minimum'      , float),
                ('get_optimal'      , float),
                ('get_shorten'      , bool ),
                ('get_use_gap'      , bool ),
                ('get_use_maximum'  , bool ),
                ('get_use_minimum'  , bool ),
            )

            for method, return_type in gets:
                method = getattr(self.dialog, method)
                assert isinstance(method(), return_type)

        def test_signals(self):

            self.dialog._optimal_spin.set_value(3.333)
            self.dialog._min_spin.set_value(3.333)
            self.dialog._max_spin.set_value(3.333)
            self.dialog._gap_spin.set_value(3.333)

            self.dialog._lengthen_check.set_active(True)
            self.dialog._shorten_check.set_active(True)
            self.dialog._min_check.set_active(True)
            self.dialog._max_check.set_active(True)
            self.dialog._gap_check.set_active(True)
            self.dialog._prj_all_radio.set_active(True)
            self.dialog._sub_all_radio.set_active(True)

            self.dialog._lengthen_check.set_active(False)
            self.dialog._shorten_check.set_active(False)
            self.dialog._min_check.set_active(False)
            self.dialog._max_check.set_active(False)
            self.dialog._gap_check.set_active(False)
            self.dialog._prj_all_radio.set_active(False)
            self.dialog._sub_all_radio.set_active(False)

    TestDurationAdjustDialog().run()
