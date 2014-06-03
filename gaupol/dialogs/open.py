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

"""Dialog for selecting subtitle files to open."""

import aeidon
import gaupol
import os

from gi.repository import Gtk

__all__ = ("OpenDialog",)


class OpenDialog(gaupol.FileDialog):

    """Dialog for selecting subtitle files to open."""

    _widgets = ("align_combo", "align_label", "encoding_combo")

    def __init__(self, parent, title, doc):
        """Initialize an :class:`OpenDialog` instance."""
        gaupol.FileDialog.__init__(self)
        self._use_autodetection = aeidon.util.chardet_available()
        self._init_extra_widget()
        self._init_filters()
        self._init_encoding_combo()
        self._init_align_combo()
        self._init_values(doc)
        self.set_title(title)
        self.set_transient_for(parent)
        self.set_action(Gtk.FileChooserAction.OPEN)
        self.add_button(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL)
        self.add_button(Gtk.STOCK_OPEN, Gtk.ResponseType.OK)
        self.set_default_response(Gtk.ResponseType.OK)
        self.connect("response", self._on_response)

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

    def _init_extra_widget(self):
        """Initialize the extra widget from UI definition file."""
        ui_file_path = os.path.join(aeidon.DATA_DIR, "ui", "open-dialog.ui")
        builder = Gtk.Builder()
        builder.set_translation_domain("gaupol")
        builder.add_from_file(ui_file_path)
        builder.connect_signals(self)
        for name in self._widgets:
            widget = builder.get_object(name)
            setattr(self, "_{}".format(name), widget)
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        builder.get_object("main_vbox").reparent(vbox)
        vbox.show_all()
        self.set_extra_widget(vbox)

    def _init_values(self, doc):
        """Initialize default values for widgets."""
        self.set_select_multiple(doc == aeidon.documents.MAIN)
        if os.path.isdir(gaupol.conf.file.directory):
            self.set_current_folder(gaupol.conf.file.directory)
        self.set_encoding(gaupol.conf.file.encoding)
        self._align_combo.set_active(gaupol.conf.file.align_method)
        self._align_combo.props.visible = (doc == aeidon.documents.TRAN)
        self._align_label.props.visible = (doc == aeidon.documents.TRAN)

    def _on_response(self, dialog, response):
        """Save default values for widgets."""
        gaupol.conf.file.encoding = self.get_encoding()
        directory = self.get_current_folder()
        if directory is not None:
            gaupol.conf.file.directory = directory
        index = self._align_combo.get_active()
        gaupol.conf.file.align_method = aeidon.align_methods[index]
