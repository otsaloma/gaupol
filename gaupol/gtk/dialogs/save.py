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

"""Dialog for selecting a subtitle file to save."""

import gaupol.gtk
import os

__all__ = ("SaveDialog",)


class SaveDialog(gaupol.gtk.FileDialog):

    """Dialog for selecting a subtitle file to save."""

    # pylint: disable-msg=E1101

    def __init__(self, parent, title):
        """Initialize a SaveDialog object."""

        gaupol.gtk.FileDialog.__init__(self, "save.glade")
        get_widget = self._glade_xml.get_widget
        self._encoding_combo = get_widget("encoding_combo")
        self._format_combo = get_widget("format_combo")
        self._newline_combo = get_widget("newline_combo")
        self.conf = gaupol.gtk.conf.file

        self._init_filters()
        self._init_format_combo()
        self._init_encoding_combo()
        self._init_newline_combo()
        self._init_values()
        self._init_signal_handlers()
        self.set_title(title)
        self.set_transient_for(parent)

    def _init_format_combo(self):
        """Initialize the format combo box."""

        store = self._format_combo.get_model()
        for name in (x.label for x in gaupol.formats):
            store.append((name,))
        self._format_combo.set_active(0)

    def _init_newline_combo(self):
        """Initialize the newline combo box."""

        store = self._newline_combo.get_model()
        for name in (x.label for x in gaupol.newlines):
            store.append((name,))
        self._newline_combo.set_active(0)

    def _init_signal_handlers(self):
        """Initialize signal handlers."""

        gaupol.util.connect(self, self, "response")
        gaupol.util.connect(self, "_format_combo", "changed")
        gaupol.util.connect(self, "_encoding_combo", "changed")

        def update_filename(button, event, self):
            self._format_combo.emit("changed")
        # Use an ugly way to add the lacking extension to the filename
        # so that the overwrite confirmation check is done correctly.
        save_button = self.action_area.get_children()[0]
        save_button.connect("event", update_filename, self)

    def _init_values(self):
        """Initialize default values for widgets."""

        if os.path.isdir(self.conf.directory):
            self.set_current_folder(self.conf.directory)
        self.set_encoding(self.conf.encoding)
        self.set_format(self.conf.format)
        self.set_newline(self.conf.newline)

    def _on_format_combo_changed(self, combo_box):
        """Change the extension of the current filename."""

        path = self.get_filename()
        if path is None: return
        self.unselect_filename(path)
        dirname = os.path.dirname(path)
        basename = os.path.basename(path)
        extensions = [x.extension for x in gaupol.formats]
        if basename.endswith(tuple(extensions)):
            index = basename.rfind(".")
            basename = basename[:index]
        format = self.get_format()
        basename += format.extension
        path = os.path.join(dirname, basename)
        self.set_current_name(basename)
        self.set_filename(path)

    def _on_response(self, dialog, response):
        """Save widget values."""

        self.conf.encoding = self.get_encoding()
        self.conf.format = self.get_format()
        self.conf.newline = self.get_newline()
        self.conf.directory = self.get_current_folder()

    def get_format(self):
        """Return the selected format."""

        index = self._format_combo.get_active()
        return gaupol.formats[index]

    def get_newline(self):
        """Return the selected newline."""

        index = self._newline_combo.get_active()
        return gaupol.newlines[index]

    def set_format(self, format):
        """Set the selected format."""

        if format is None: return
        self._format_combo.set_active(format)

    def set_name(self, path):
        """Set either filename or current name."""

        if os.path.isfile(path):
            return self.set_filename(path)
        return self.set_current_name(path)

    def set_newline(self, newline):
        """Set the selected newline."""

        if newline is None: return
        self._newline_combo.set_active(newline)
