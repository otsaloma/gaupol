# -*- coding: utf-8 -*-

# Copyright (C) 2005 Osmo Salomaa
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""Dialog for selecting a subtitle file to save."""

import aeidon
import gaupol
import os

from aeidon.i18n   import _
from gi.repository import Gio
from gi.repository import GObject
from gi.repository import Gtk

__all__ = ("SaveDialog",)


class SaveDialog(Gtk.FileChooserDialog, gaupol.FileDialog):

    """Dialog for selecting a subtitle file to save."""

    def __init__(self, parent, title, mode):
        """Initialize a :class:`SaveDialog` instance."""
        GObject.GObject.__init__(self)
        self._mode = mode
        self._init_dialog(parent, title)
        self._init_extra_widget()
        self._init_filters()
        self._init_format_combo()
        self._init_encoding_combo()
        self._init_newline_combo()
        self._init_framerate_combo()
        self._init_values()

    def get_format(self):
        """Return the selected format."""
        index = self._format_combo.get_active()
        return aeidon.formats[index]

    def get_framerate(self):
        """Return the selected framerate."""
        index = self._framerate_combo.get_active()
        return aeidon.framerates[index]

    def get_newline(self):
        """Return the selected newline."""
        index = self._newline_combo.get_active()
        return aeidon.newlines[index]

    def _init_dialog(self, parent, title):
        """Initialize the dialog."""
        self.add_button(_("_Cancel"), Gtk.ResponseType.CANCEL)
        self.add_button(_("_Save"), Gtk.ResponseType.OK)
        self.set_default_response(Gtk.ResponseType.OK)
        self.set_transient_for(parent)
        self.set_title(title)
        self.connect("response", self._on_response)
        # Add a possibly missing filename extension before GTK's
        # overwrite confirmation runs on save button click.
        save_button = self.get_widget_for_response(Gtk.ResponseType.OK)
        gesture = Gtk.GestureClick()
        gesture.set_propagation_phase(Gtk.PropagationPhase.CAPTURE)
        gesture.connect("pressed", self._on_save_button_pressed)
        save_button.add_controller(gesture)
        self.set_action(Gtk.FileChooserAction.SAVE)

    def _init_extra_widget(self):
        """Initialize the extra widget with format etc. combos."""
        self._format_combo = Gtk.ComboBox(hexpand=True)
        self._format_combo.connect("changed", self._on_format_combo_changed)
        format_label = Gtk.Label(label=_("For_mat:"),
                                 halign=Gtk.Align.START,
                                 use_underline=True)

        format_label.set_mnemonic_widget(self._format_combo)
        self._encoding_combo = Gtk.ComboBox(hexpand=True)
        self._encoding_combo.connect(
            "changed", self._on_encoding_combo_changed)
        encoding_label = Gtk.Label(label=_("_Encoding:"),
                                   halign=Gtk.Align.START,
                                   use_underline=True)

        encoding_label.set_mnemonic_widget(self._encoding_combo)
        self._newline_combo = Gtk.ComboBox(hexpand=True)
        newline_label = Gtk.Label(label=_("Ne_wlines:"),
                                  halign=Gtk.Align.START,
                                  use_underline=True)

        newline_label.set_mnemonic_widget(self._newline_combo)
        self._framerate_combo = Gtk.ComboBox(hexpand=True)
        self._framerate_label = Gtk.Label(label=_("F_ramerate:"),
                                          halign=Gtk.Align.START,
                                          use_underline=True)

        self._framerate_label.set_mnemonic_widget(self._framerate_combo)
        grid = Gtk.Grid(row_spacing=6,
                        column_spacing=12,
                        margin_top=12,
                        margin_bottom=12,
                        margin_start=12,
                        margin_end=12)

        grid.attach(format_label, 0, 0, 1, 1)
        grid.attach(self._format_combo, 1, 0, 1, 1)
        grid.attach(encoding_label, 0, 1, 1, 1)
        grid.attach(self._encoding_combo, 1, 1, 1, 1)
        grid.attach(newline_label, 0, 2, 1, 1)
        grid.attach(self._newline_combo, 1, 2, 1, 1)
        grid.attach(self._framerate_label, 0, 3, 1, 1)
        grid.attach(self._framerate_combo, 1, 3, 1, 1)
        # GTK 4 file choosers don't support an extra widget,
        # add to the content area below the file chooser widget.
        self.get_content_area().append(grid)

    def _init_format_combo(self):
        """Initialize the format combo box."""
        store = Gtk.ListStore(str)
        self._format_combo.set_model(store)
        for name in (x.label for x in aeidon.formats):
            if name == "SubRip":
                # Mark the SubRip format as recommended, since
                # it's the most common one and best supported,
                # both in Gaupol and elsewhere.
                name = _("{} (recommended)").format(name)
            store.append((name,))
        view = self._format_combo.get_child()
        path = gaupol.util.tree_row_to_path(0)
        view.set_displayed_row(path)
        renderer = Gtk.CellRendererText()
        self._format_combo.pack_start(renderer, expand=True)
        self._format_combo.add_attribute(renderer, "text", 0)

    def _init_framerate_combo(self):
        """Initialize the framerate combo box."""
        store = Gtk.ListStore(str)
        self._framerate_combo.set_model(store)
        for name in (x.label for x in aeidon.framerates):
            store.append((name,))
        view = self._framerate_combo.get_child()
        path = gaupol.util.tree_row_to_path(0)
        view.set_displayed_row(path)
        renderer = Gtk.CellRendererText()
        self._framerate_combo.pack_start(renderer, expand=True)
        self._framerate_combo.add_attribute(renderer, "text", 0)

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
            directory = Gio.File.new_for_path(gaupol.conf.file.directory)
            self.set_current_folder(directory)
        self.set_encoding(gaupol.conf.file.encoding)
        self.set_format(gaupol.conf.file.format)
        self.set_newline(gaupol.conf.file.newline)
        self.set_framerate(gaupol.conf.editor.framerate)
        self._framerate_combo.set_visible(False)
        self._framerate_label.set_visible(False)

    def _on_format_combo_changed(self, *args):
        """Change the extension of the current filename."""
        format = self.get_format()
        basename = self.get_current_name()
        if basename and not basename.endswith(format.extension):
            basename = aeidon.util.replace_extension(basename, format)
            self.set_current_name(basename)
        visible = (format.mode != self._mode)
        self._framerate_combo.set_visible(visible)
        self._framerate_label.set_visible(visible)

    def _on_response(self, dialog, response):
        """Save default values for widgets."""
        directory = self.get_current_folder()
        if directory is not None and directory.get_path() is not None:
            gaupol.conf.file.directory = directory.get_path()
        gaupol.conf.file.encoding = self.get_encoding()
        gaupol.conf.file.format = self.get_format()
        gaupol.conf.file.newline = self.get_newline()
        gaupol.conf.editor.framerate = self.get_framerate()
        if response == Gtk.ResponseType.OK:
            # If the filename is lacking the extension, add it. This already
            # happened in self._on_save_button_pressed, before overwrite
            # confirmation, if the save button was clicked, but not
            # necessarily if the user hit Enter on the keyboard.
            self._format_combo.emit("changed")

    def _on_save_button_pressed(self, gesture, n_press, x, y):
        """Ensure that the filename contains an extension."""
        # Add possibly lacking extension to the filename.
        self._format_combo.emit("changed")

    def set_format(self, format):
        """Set the selected format."""
        if format is None: return
        self._format_combo.set_active(format)

    def set_framerate(self, framerate):
        """Set the selected framerate."""
        if framerate is None: return
        self._framerate_combo.set_active(framerate)

    def set_name(self, path):
        """Set the selected filename."""
        if os.path.isfile(path):
            return self.set_file(Gio.File.new_for_path(path))
        return self.set_current_name(os.path.basename(path))

    def set_newline(self, newline):
        """Set the selected newline."""
        if newline is None: return
        self._newline_combo.set_active(newline)
