# -*- coding: utf-8-unix -*-

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

"""Dialog for converting framerates."""

import aeidon
import gaupol

from gi.repository import Gtk

__all__ = ("FramerateConvertDialog",)


class FramerateConvertDialog(gaupol.BuilderDialog):

    """Dialog for converting framerates."""

    _widgets = ("all_radio", "current_radio", "input_combo", "output_combo")

    # XXX: This shit segfaults.

    def __init__(self, parent, application):
        """Initialize a FramerateConvertDialog object."""
        gaupol.BuilderDialog.__init__(self, "framerate-convert-dialog.ui")
        self.application = application
        self._init_input_combo()
        self._init_output_combo()
        self._init_values()
        self._dialog.set_transient_for(parent)
        self._dialog.set_default_response(Gtk.ResponseType.OK)

    def _convert_framerates(self):
        """Convert framerates in target projects."""
        target = self._get_target()
        fri = aeidon.framerates[self._input_combo.get_active()]
        fro = aeidon.framerates[self._output_combo.get_active()]
        for page in self.application.get_target_pages(target):
            self.application.set_current_page(page)
            page.project.convert_framerate(None, fri, fro)

    def _get_target(self):
        """Return the selected target."""
        if self._current_radio.get_active():
            return gaupol.targets.CURRENT
        if self._all_radio.get_active():
            return gaupol.targets.ALL
        raise ValueError("Invalid target radio state")

    def _init_input_combo(self):
        """Initialize the input framerate combo box."""
        store = Gtk.ListStore(str)
        self._input_combo.set_model(store)
        for label in (x.label for x in aeidon.framerates):
            store.append((label,))
        renderer = Gtk.CellRendererText()
        self._input_combo.pack_start(renderer, expand=True)
        self._input_combo.add_attribute(renderer, "text", 0)

    def _init_output_combo(self):
        """Initialize the output framerate combo box."""
        store = Gtk.ListStore(str)
        self._output_combo.set_model(store)
        for label in (x.label for x in aeidon.framerates):
            store.append((label,))
        renderer = Gtk.CellRendererText()
        self._output_combo.pack_start(renderer, expand=True)
        self._output_combo.add_attribute(renderer, "text", 0)

    def _init_values(self):
        """Intialize default values for widgets."""
        page = self.application.get_current_page()
        target = gaupol.conf.framerate_convert.target
        self._input_combo.set_active(page.project.framerate)
        self._output_combo.set_active(page.project.framerate)
        self._all_radio.set_active(target == gaupol.targets.ALL)
        self._current_radio.set_active(target == gaupol.targets.CURRENT)

    def _on_input_combo_changed(self, *args):
        """Set response sensitivity."""
        index_in = self._input_combo.get_active()
        index_out = self._output_combo.get_active()
        sensitive = (index_in != index_out)
        self._dialog.set_response_sensitive(Gtk.ResponseType.OK, sensitive)

    def _on_output_combo_changed(self, *args):
        """Set response sensitivity."""
        index_in = self._input_combo.get_active()
        index_out = self._output_combo.get_active()
        sensitive = (index_in != index_out)
        self._dialog.set_response_sensitive(Gtk.ResponseType.OK, sensitive)

    def _on_response(self, dialog, response):
        """Save target and convert framerates."""
        gaupol.conf.framerate_convert.target = self._get_target()
        if response == Gtk.ResponseType.OK:
            self._convert_framerates()
