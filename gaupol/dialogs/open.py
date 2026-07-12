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
# along with this program. If not, see <https://www.gnu.org/licenses/>.

"""Dialog for selecting subtitle files to open."""

import aeidon
import gaupol

from aeidon.i18n   import _
from gi.repository import Gio
from gi.repository import GObject
from gi.repository import Gtk
from pathlib import Path

class OpenDialog(Gtk.FileChooserDialog, gaupol.FileDialog):

    """Dialog for selecting subtitle files to open."""

    def __init__(self, parent, title, doc, directory=None):
        """Initialize an :class:`OpenDialog` instance."""
        GObject.GObject.__init__(self)
        self._use_autodetection = aeidon.util.chardet_available()
        self._init_dialog(parent, title)
        self._init_extra_widget()
        self._init_filters()
        self._init_encoding_combo()
        self._init_align_combo()
        self._init_values(doc, directory)

    def _init_align_combo(self):
        """Initialize the align method combo box."""
        store = Gtk.ListStore(str)
        self._align_combo.set_model(store)
        for align_method in aeidon.align_methods:
            store.append((align_method.label,))
        view = self._align_combo.get_child()
        path = gaupol.util.tree_row_to_path(0)
        view.set_displayed_row(path)
        renderer = Gtk.CellRendererText()
        self._align_combo.pack_start(renderer, expand=True)
        self._align_combo.add_attribute(renderer, "text", 0)

    def _init_dialog(self, parent, title):
        """Initialize the dialog."""
        self.add_button(_("_Cancel"), Gtk.ResponseType.CANCEL)
        self.add_button(_("_Open"), Gtk.ResponseType.OK)
        self.set_default_response(Gtk.ResponseType.OK)
        self.set_transient_for(parent)
        self.set_modal(True)
        self.set_title(title)
        self.connect("response", self._on_response)
        self.set_action(Gtk.FileChooserAction.OPEN)

    def _init_extra_widget(self):
        """Initialize the extra widget with encoding and align combos."""
        self._encoding_combo = Gtk.ComboBox(hexpand=True)
        self._encoding_combo.connect(
            "changed", self._on_encoding_combo_changed)
        encoding_label = Gtk.Label(label=_("_Encoding:"),
                                   halign=Gtk.Align.START,
                                   use_underline=True)

        encoding_label.set_mnemonic_widget(self._encoding_combo)
        self._align_combo = Gtk.ComboBox(hexpand=True)
        self._align_label = Gtk.Label(label=_("Align _method:"),
                                      halign=Gtk.Align.START,
                                      use_underline=True)

        self._align_label.set_mnemonic_widget(self._align_combo)
        grid = Gtk.Grid(row_spacing=6,
                        column_spacing=12,
                        margin_top=12,
                        margin_bottom=12,
                        margin_start=12,
                        margin_end=12)

        grid.attach(encoding_label, 0, 0, 1, 1)
        grid.attach(self._encoding_combo, 1, 0, 1, 1)
        grid.attach(self._align_label, 0, 1, 1, 1)
        grid.attach(self._align_combo, 1, 1, 1, 1)
        # GTK-4 file choosers don't support an extra widget,
        # add to the content area below the file chooser widget.
        self.get_content_area().append(grid)

    def _init_values(self, doc, directory):
        """Initialize default values for widgets."""
        self.set_select_multiple(doc == aeidon.documents.MAIN)
        # Set the location with exactly one call: a second folder load
        # would cancel the first one mid-flight and GTK pops up that
        # cancellation as a modal "Operation was cancelled" error dialog.
        directory = directory or gaupol.conf.file.directory
        if directory and Path(directory).is_dir():
            self.set_current_folder(Gio.File.new_for_path(str(directory)))
        self.set_encoding(gaupol.conf.file.encoding)
        self._align_combo.set_active(gaupol.conf.file.align_method)
        self._align_combo.set_visible(doc == aeidon.documents.TRAN)
        self._align_label.set_visible(doc == aeidon.documents.TRAN)

    def _on_response(self, dialog, response):
        """Save default values for widgets."""
        gaupol.conf.file.encoding = self.get_encoding()
        directory = self.get_current_folder()
        if directory is not None and directory.get_path() is not None:
            gaupol.conf.file.directory = directory.get_path()
        index = self._align_combo.get_active()
        gaupol.conf.file.align_method = aeidon.align_methods[index]
