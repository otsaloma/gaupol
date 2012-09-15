# -*- coding: utf-8 -*-

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

"""Dialog for selecting a subtitle file to save."""

import aeidon
import gaupol
import os

from gi.repository import Gtk

__all__ = ("SaveDialog",)


class SaveDialog(gaupol.FileDialog):

    """Dialog for selecting a subtitle file to save."""

    _widgets = ("encoding_combo", "format_combo", "newline_combo")

    def __init__(self, parent, title):
        """Initialize a :class:`SaveDialog` object."""
        gaupol.FileDialog.__init__(self, "save-dialog.ui")
        self._init_filters()
        self._init_format_combo()
        self._init_encoding_combo()
        self._init_newline_combo()
        self._init_values()
        self.set_title(title)
        self.set_transient_for(parent)

    def _init_format_combo(self):
        """Initialize the format combo box."""
        store = Gtk.ListStore(str)
        self._format_combo.set_model(store)
        for name in (x.label for x in aeidon.formats):
            store.append((name,))
        view = self._format_combo.get_child()
        path = gaupol.util.tree_row_to_path(0)
        view.set_displayed_row(path)
        renderer = Gtk.CellRendererText()
        self._format_combo.pack_start(renderer, expand=True)
        self._format_combo.add_attribute(renderer, "text", 0)

    def _init_newline_combo(self):
        """Initialize the newline combo box."""
        store = Gtk.ListStore(str)
        self._newline_combo.set_model(store)
        for name in (x.label for x in aeidon.newlines):
            store.append((name,))
        view = self._newline_combo.get_child()
        path = gaupol.util.tree_row_to_path(0)
        view.set_displayed_row(path)
        renderer = Gtk.CellRendererText()
        self._newline_combo.pack_start(renderer, expand=True)
        self._newline_combo.add_attribute(renderer, "text", 0)

    def _init_values(self):
        """Initialize default values for widgets."""
        if os.path.isdir(gaupol.conf.file.directory):
            self.set_current_folder(gaupol.conf.file.directory)
        self.set_encoding(gaupol.conf.file.encoding)
        self.set_format(gaupol.conf.file.format)
        self.set_newline(gaupol.conf.file.newline)

    def _on_format_combo_changed(self, combo_box):
        """Change the extension of the current filename."""
        path = self.get_filename()
        if path is None: return
        dirname = os.path.dirname(path)
        basename = os.path.basename(path)
        format = self.get_format()
        if path.endswith(format.extension): return
        basename = aeidon.util.replace_extension(basename, format)
        path = os.path.join(dirname, basename)
        self.unselect_filename(path)
        self.set_current_name(basename)
        self.set_filename(path)

    def _on_response(self, dialog, response):
        """Save default values for widgets."""
        directory = self.get_current_folder()
        if directory is not None:
            gaupol.conf.file.directory = directory
        gaupol.conf.file.encoding = self.get_encoding()
        gaupol.conf.file.format = self.get_format()
        gaupol.conf.file.newline = self.get_newline()

    def _on_save_button_event(self, button, event):
        """Ensure that the filename contains an extension."""
        # Catch all events on save button to ensure that a possibly
        # lacking extension is added to the filename so that overwrite
        # confirmation check is done correctly.
        self._format_combo.emit("changed")

    def get_format(self):
        """Return the selected format."""
        index = self._format_combo.get_active()
        return aeidon.formats[index]

    def get_newline(self):
        """Return the selected newline."""
        index = self._newline_combo.get_active()
        return aeidon.newlines[index]

    def set_format(self, format):
        """Set the selected format."""
        if format is None: return
        self._format_combo.set_active(format)

    def set_name(self, path):
        """Set the selected filename."""
        if os.path.isfile(path):
            return self.set_filename(path)
        return self.set_current_name(path)

    def set_newline(self, newline):
        """Set the selected newline."""
        if newline is None: return
        self._newline_combo.set_active(newline)
