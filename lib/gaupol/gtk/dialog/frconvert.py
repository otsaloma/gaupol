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


"""Dialog for converting framerate."""


import gtk

from gaupol.gtk      import cons
from gaupol.gtk.util import conf, gtklib


class FramerateConvertDialog(object):

    """Dialog for converting framerate."""

    def __init__(self, parent):

        glade_xml = gtklib.get_glade_xml('frconvert-dialog')
        self._all_radio     = glade_xml.get_widget('all_radio')
        self._correct_combo = glade_xml.get_widget('correct_combo')
        self._current_combo = glade_xml.get_widget('current_combo')
        self._current_radio = glade_xml.get_widget('current_radio')
        self._dialog        = glade_xml.get_widget('dialog')

        self._init_signals()
        self._init_data()
        self._dialog.set_transient_for(parent)
        self._dialog.set_default_response(gtk.RESPONSE_OK)

    def _init_data(self):
        """Initialize default values."""

        for combo_box in (self._current_combo, self._correct_combo):
            store = combo_box.get_model()
            store.clear()
            for name in cons.Framerate.display_names:
                store.append([name])
            combo_box.set_active(conf.editor.framerate)

        target = conf.framerate_convert.target
        self._all_radio.set_active(target == cons.Target.ALL)
        self._current_radio.set_active(target == cons.Target.CURRENT)

    def _init_signals(self):
        """Initialize signals."""

        gtklib.connect(self, '_correct_combo', 'changed' )
        gtklib.connect(self, '_current_combo', 'changed' )
        gtklib.connect(self, '_dialog'       , 'response')

    def _on_correct_combo_changed(self, *args):
        """Set response sensitivity."""

        current = self._current_combo.get_active()
        correct = self._correct_combo.get_active()
        sensitive = current != correct
        self._dialog.set_response_sensitive(gtk.RESPONSE_OK, sensitive)

    def _on_current_combo_changed(self, *args):
        """Set response sensitivity."""

        current = self._current_combo.get_active()
        correct = self._correct_combo.get_active()
        sensitive = current != correct
        self._dialog.set_response_sensitive(gtk.RESPONSE_OK, sensitive)

    def _on_dialog_response(self, dialog, response):
        """Save settings."""

        if response == gtk.RESPONSE_OK:
            conf.framerate_convert.target = self.get_target()

    def destroy(self):
        """Destroy dialog."""

        self._dialog.destroy()

    def get_correct(self):
        """Get correct framerate."""

        return self._correct_combo.get_active()

    def get_current(self):
        """Get current framerate."""

        return self._current_combo.get_active()

    def get_target(self):
        """Get target."""

        if self._all_radio.get_active():
            return cons.Target.ALL
        elif self._current_radio.get_active():
            return cons.Target.CURRENT

    def run(self):
        """Run dialog."""

        self._dialog.show()
        return self._dialog.run()
