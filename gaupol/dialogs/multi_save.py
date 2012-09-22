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

"""Dialog for selecting properties to save multiple files with."""

import aeidon
import gaupol
import os
_ = aeidon.i18n._

from gi.repository import Gtk

__all__ = ("MultiSaveDialog",)


class MultiSaveDialog(gaupol.FileDialog):

    """Dialog for selecting properties to save multiple files with."""

    _widgets = ("encoding_combo",
                "filechooser_button",
                "format_combo",
                "newline_combo")

    def __init__(self, parent, application):
        """Initialize a :class:`MultiSaveDialog` object."""
        gaupol.FileDialog.__init__(self, "multi-save-dialog.ui")
        self.application = application
        self._init_format_combo()
        self._init_encoding_combo()
        self._init_newline_combo()
        width = gaupol.util.char_to_px(60)
        self._filechooser_button.set_size_request(width, -1)
        self._init_values()
        self.set_transient_for(parent)

    def _init_format_combo(self):
        """Initialize the format combo box."""
        store = Gtk.ListStore(str)
        self._format_combo.set_model(store)
        for name in (x.label for x in aeidon.formats):
            store.append((name,))
        view = self._format_combo.get_child()
        view.set_displayed_row(gaupol.util.tree_row_to_path(0))
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
        view.set_displayed_row(gaupol.util.tree_row_to_path(0))
        renderer = Gtk.CellRendererText()
        self._newline_combo.pack_start(renderer, expand=True)
        self._newline_combo.add_attribute(renderer, "text", 0)

    def _init_values(self):
        """Initialize default values for widgets."""
        pages = [x for x in self.application.pages
                 if x.project.main_file is not None]

        ## Suggest format, encoding and newlines to match those
        ## from the first page to consider.
        file = pages[0].project.main_file
        self.set_directory(os.path.dirname(file.path))
        self.set_format(file.format)
        self.set_encoding(file.encoding)
        self.set_newline(file.newline)

    def _on_response(self, dialog, response):
        """Save default values for widgets."""
        gaupol.conf.file.encoding = self.get_encoding()
        gaupol.conf.file.format = self.get_format()
        gaupol.conf.file.newline = self.get_newline()
        if response != Gtk.ResponseType.OK: return
        gaupol.util.set_cursor_busy(self._dialog)
        self._save_all_documents_as()
        gaupol.util.set_cursor_normal(self._dialog)

    @aeidon.deco.silent(gaupol.Default)
    def _save_all_documents_as(self):
        """Save all documents with selected properties."""
        pages = [x for x in self.application.pages
                 if x.project.main_file is not None]

        files = [None for x in pages]
        for i, page in enumerate(pages):
            path = os.path.basename(page.project.main_file.path)
            path = aeidon.util.replace_extension(path, self.get_format())
            path = os.path.join(self.get_directory(), path)
            files[i] = aeidon.files.new(self.get_format(),
                                        path,
                                        self.get_encoding(),
                                        self.get_newline())

        overwrite_count = sum(os.path.isfile(x.path) for x in files)
        if overwrite_count > 0:
            self._show_overwrite_question_dialog(overwrite_count,
                                                 self.get_directory())

        for i, page in enumerate(pages):
            self.application.save_main_as(page, files[i])

    def _show_overwrite_question_dialog(self, overwrite_count, path):
        """
        Show a question dialog if about to overwrite files.

        Raise :exc:`gaupol.Default` if opening cancelled.
        """
        title = _("{:d} of the files to be saved already exist. "
            "Do you want to replace them?").format(overwrite_count)
        message = _('The files already exist in "{}". '
            'Replacing them will overwrite their contents.').format(path)
        dialog = gaupol.QuestionDialog(self._dialog, title, message)
        dialog.add_button(Gtk.STOCK_CANCEL, Gtk.ResponseType.NO)
        dialog.add_button(_("_Replace"), Gtk.ResponseType.YES)
        dialog.set_default_response(Gtk.ResponseType.YES)
        response = gaupol.util.flash_dialog(dialog)
        gaupol.util.raise_default(response != Gtk.ResponseType.YES)

    def get_format(self):
        """Return the selected format."""
        index = self._format_combo.get_active()
        return aeidon.formats[index]

    def get_directory(self):
        """Return the selected directory."""
        return self._filechooser_button.get_filename()

    def get_newline(self):
        """Return the selected newline."""
        index = self._newline_combo.get_active()
        return aeidon.newlines[index]

    def set_directory(self, path):
        """Set the selected directory."""
        return self._filechooser_button.set_filename(path)

    def set_format(self, format):
        """Set the selected format."""
        if format is None: return
        self._format_combo.set_active(format)

    def set_newline(self, newline):
        """Set the selected newline."""
        if newline is None: return
        self._newline_combo.set_active(newline)
