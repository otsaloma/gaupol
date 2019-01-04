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
from gi.repository import GObject
from gi.repository import Gtk

__all__ = ("SaveDialog",)


class SaveDialog(Gtk.FileChooserDialog, gaupol.FileDialog):

    """Dialog for selecting a subtitle file to save."""

    _widgets = [
        "encoding_combo",
        "format_combo",
        "framerate_combo",
        "framerate_label",
        "newline_combo",
    ]

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
        save_button = self.get_widget_for_response(Gtk.ResponseType.OK)
        save_button.connect("event", self._on_save_button_event)
        self.set_action(Gtk.FileChooserAction.SAVE)
        self.set_do_overwrite_confirmation(True)

    def _init_extra_widget(self):
        """Initialize the extra widget from UI definition file."""
        ui_file_path = os.path.join(aeidon.DATA_DIR, "ui", "save-dialog.ui")
        builder = Gtk.Builder()
        builder.set_translation_domain("gaupol")
        builder.add_from_file(ui_file_path)
        builder.connect_signals(self)
        for name in self._widgets:
            widget = builder.get_object(name)
            setattr(self, "_{}".format(name), widget)
        vbox = gaupol.util.new_vbox(spacing=0)
        main_vbox = builder.get_object("main_vbox")
        main_vbox.get_parent().remove(main_vbox)
        vbox.add(main_vbox)
        vbox.show_all()
        self.set_extra_widget(vbox)

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
            self.set_current_folder(gaupol.conf.file.directory)
        self.set_encoding(gaupol.conf.file.encoding)
        self.set_format(gaupol.conf.file.format)
        self.set_newline(gaupol.conf.file.newline)
        self.set_framerate(gaupol.conf.editor.framerate)
        self._framerate_combo.hide()
        self._framerate_label.hide()

    def _on_format_combo_changed(self, *args):
        """Change the extension of the current filename."""
        format = self.get_format()
        path = self.get_filename()
        if path is not None:
            dirname = os.path.dirname(path)
            basename = os.path.basename(path)
            if not path.endswith(format.extension):
                basename = aeidon.util.replace_extension(basename, format)
                path = os.path.join(dirname, basename)
                self.unselect_filename(path)
                self.set_current_name(basename)
                self.set_filename(path)
        visible = (format.mode != self._mode)
        self._framerate_combo.set_visible(visible)
        self._framerate_label.set_visible(visible)

    def _on_response(self, dialog, response):
        """Save default values for widgets."""
        directory = self.get_current_folder()
        if directory is not None:
            gaupol.conf.file.directory = directory
        gaupol.conf.file.encoding = self.get_encoding()
        gaupol.conf.file.format = self.get_format()
        gaupol.conf.file.newline = self.get_newline()
        gaupol.conf.editor.framerate = self.get_framerate()
        if (response == Gtk.ResponseType.OK and
            not self.get_filename().endswith(self.get_format().extension)):
            # If the filename is lacking the extension, add it, stop this
            # response and emit a new one so that overwrite confirmation gets
            # called with the full filename. The filename extension might have
            # already been added in self._on_save_button_event, but not
            # necessarily if the user hit Enter on the keyboard.
            self._format_combo.emit("changed")
            gaupol.util.iterate_main()
            self.stop_emission("response")
            return self.response(Gtk.ResponseType.OK)

    def _on_save_button_event(self, button, event):
        """Ensure that the filename contains an extension."""
        # Add possibly lacking extension to the filename.
        self._format_combo.emit("changed")
        gaupol.util.iterate_main()

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
            return self.set_filename(path)
        return self.set_current_name(path)

    def set_newline(self, newline):
        """Set the selected newline."""
        if newline is None: return
        self._newline_combo.set_active(newline)
