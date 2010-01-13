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

"""Dialog for converting framerates."""

import gaupol
import gtk

__all__ = ("FramerateConvertDialog",)


class FramerateConvertDialog(gaupol.GladeDialog):

    """Dialog for converting framerates."""

    def __init__(self, parent, application):
        """Initialize a FramerateConvertDialog object."""

        gaupol.GladeDialog.__init__(self, "framerate.glade")
        get_widget = self._glade_xml.get_widget
        self._all_radio = get_widget("all_radio")
        self._current_radio = get_widget("current_radio")
        self._input_combo = get_widget("input_combo")
        self._output_combo = get_widget("output_combo")
        self.application = application
        self.conf = gaupol.conf.framerate_convert

        self._init_signal_handlers()
        self._init_values()
        self._dialog.set_transient_for(parent)
        self._dialog.set_default_response(gtk.RESPONSE_OK)

    def _convert_framerates(self):
        """Convert framerates in target projects."""

        target = self._get_target()
        input = aeidon.framerates[self._input_combo.get_active()]
        output = aeidon.framerates[self._output_combo.get_active()]
        for page in self.application.get_target_pages(target):
            self.application.set_current_page(page)
            page.project.convert_framerate(None, input, output)

    def _get_target(self):
        """Return the selected target."""

        if self._current_radio.get_active():
            return gaupol.targets.CURRENT
        if self._all_radio.get_active():
            return gaupol.targets.ALL
        raise ValueError("Invalid target radio state")

    def _init_signal_handlers(self):
        """Initialize signal handlers."""

        aeidon.util.connect(self, "_input_combo", "changed")
        aeidon.util.connect(self, "_output_combo", "changed")
        aeidon.util.connect(self, self, "response")

    def _init_values(self):
        """Intialize default values for widgets."""

        store = self._input_combo.get_model()
        for label in (x.label for x in aeidon.framerates):
            store.append((label,))
        page = self.application.get_current_page()
        framerate = page.project.framerate
        self._input_combo.set_active(framerate)
        store = self._output_combo.get_model()
        for label in (x.label for x in aeidon.framerates):
            store.append((label,))
        framerate = gaupol.conf.editor.framerate
        self._output_combo.set_active(framerate)

        targets = gaupol.targets
        self._current_radio.set_active(self.conf.target == targets.CURRENT)
        self._all_radio.set_active(self.conf.target == targets.ALL)

    def _on_input_combo_changed(self, *args):
        """Set the response sensitivity."""

        input = self._input_combo.get_active()
        output = self._output_combo.get_active()
        sensitive = input != output
        self._dialog.set_response_sensitive(gtk.RESPONSE_OK, sensitive)

    def _on_output_combo_changed(self, *args):
        """Set the response sensitivity."""

        input = self._input_combo.get_active()
        output = self._output_combo.get_active()
        sensitive = input != output
        self._dialog.set_response_sensitive(gtk.RESPONSE_OK, sensitive)

    def _on_response(self, dialog, response):
        """Save settings and convert framerates."""

        self.conf.target = self._get_target()
        if response == gtk.RESPONSE_OK:
            self._convert_framerates()
