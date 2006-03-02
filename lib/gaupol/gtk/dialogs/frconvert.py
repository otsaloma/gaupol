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


"""Dialog for converting framerate."""


try:
    from psyco.classes import *
except ImportError:
    pass

import gobject
import gtk

from gaupol.constants import Framerate
from gaupol.gtk.util  import config, gtklib


class FramerateConvertDialog(object):

    """Dialog for shifting timings."""

    def __init__(self, parent):

        glade_xml = gtklib.get_glade_xml('frconvert-dialog.glade')
        get_widget = glade_xml.get_widget

        self._all_radio      = get_widget('projects_all_radio_button')
        self._convert_button = get_widget('convert_button')
        self._correct_combo  = get_widget('correct_combo_box')
        self._current_combo  = get_widget('current_combo_box')
        self._current_radio  = get_widget('projects_current_radio_button')
        self._dialog         = get_widget('dialog')

        self._init_signals()
        self._init_data()

        self._dialog.set_transient_for(parent)
        self._dialog.set_default_response(gtk.RESPONSE_OK)

    def _init_data(self):
        """Initialize default values."""

        for combo_box in (self._current_combo, self._correct_combo):
            store = gtk.ListStore(gobject.TYPE_STRING)
            cell_renderer = gtk.CellRendererText()
            combo_box.pack_start(cell_renderer, True)
            combo_box.add_attribute(cell_renderer, 'text', 0)
            combo_box.set_model(store)
            for i in range(len(Framerate.display_names)):
                store.append([Framerate.display_names[i]])
            combo_box.set_active(config.editor.framerate)

    def _init_signals(self):
        """Initialize signals."""

        method = self._on_current_combo_changed
        self._current_combo.connect('changed', method)
        method = self._on_correct_combo_changed
        self._correct_combo.connect('changed', method)

        method = self._on_all_radio_toggled
        self._all_radio.connect('toggled', method)

    def destroy(self):
        """Destroy the dialog."""

        self._dialog.destroy()

    def get_convert_all_projects(self):
        """Return True if selected to convert all projects."""

        return self._all_radio.get_active()

    def get_correct_framerate(self):
        """Return correct framerate."""

        return self._correct_combo.get_active()

    def get_current_framerate(self):
        """Return current framerate."""

        return self._current_combo.get_active()

    def _on_all_radio_toggled(self, radio_button):
        """Save radio button value."""

        config.framerate_convert.all_projects = radio_button.get_active()

    def _on_correct_combo_changed(self, combo_box):
        """Set convert button sensitivity."""

        self._set_convert_button_sensitivity()

    def _on_current_combo_changed(self, combo_box):
        """Set convert button sensitivity."""

        self._set_convert_button_sensitivity()

    def run(self):
        """Show and run the dialog."""

        self._dialog.show()
        return self._dialog.run()

    def _set_convert_button_sensitivity(self):
        """Set sensitivity of the convert button."""

        current = self._current_combo.get_active()
        correct = self._correct_combo.get_active()
        self._convert_button.set_sensitive(not current == correct)


if __name__ == '__main__':

    from gaupol.gtk.application import Application
    from gaupol.test            import Test

    class TestFramerateConvertDialog(Test):

        def __init__(self):

            Test.__init__(self)
            self.application = Application()
            self.application.open_main_files([self.get_subrip_path()])
            self.dialog = FramerateConvertDialog(gtk.Window())

        def destroy(self):

            self.application.window.destroy()

        def test_gets(self):

            assert isinstance(self.dialog.get_convert_all_projects(), bool)
            assert isinstance(self.dialog.get_correct_framerate(), int)
            assert isinstance(self.dialog.get_current_framerate(), int)

        def test_signals(self):

            self.dialog._correct_combo.set_active(0)
            self.dialog._correct_combo.set_active(1)
            self.dialog._current_combo.set_active(0)
            self.dialog._current_combo.set_active(1)

            self.dialog._all_radio.set_active(True)
            self.dialog._all_radio.set_active(False)
            self.dialog._current_radio.set_active(True)
            self.dialog._current_radio.set_active(False)

    TestFramerateConvertDialog().run()
