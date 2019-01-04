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

"""Dialog for selecting properties to save multiple files with."""

import aeidon
import gaupol
import os

from aeidon.i18n   import _
from gi.repository import Gtk

__all__ = ("MultiSaveDialog",)


class MultiSaveDialog(gaupol.BuilderDialog, gaupol.FileDialog):

    """Dialog for selecting properties to save multiple files with."""

    _widgets = [
        "encoding_combo",
        "filechooser_button",
        "format_combo",
        "framerate_combo",
        "framerate_label",
        "newline_combo",
    ]

    def __init__(self, parent, application, modes):
        """Initialize a :class:`MultiSaveDialog` instance."""
        gaupol.BuilderDialog.__init__(self, "multi-save-dialog.ui")
        self.application = application
        self._modes = modes
        self._init_dialog(parent)
        self._init_format_combo()
        self._init_encoding_combo()
        self._init_newline_combo()
        self._init_framerate_combo()
        width = gaupol.util.char_to_px(60)
        self._filechooser_button.set_size_request(width, -1)
        self._init_values()

    def get_directory(self):
        """Return the selected directory."""
        return self._filechooser_button.get_filename()

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

    def _get_pages(self):
        """Return a list of pages to consider."""
        return [x for x in self.application.pages
                if x.project.main_file is not None]

    def _init_dialog(self, parent):
        """Initialize the dialog."""
        self.add_button(_("_Cancel"), Gtk.ResponseType.CANCEL)
        self.add_button(_("_Save"), Gtk.ResponseType.OK)
        self.set_default_response(Gtk.ResponseType.OK)
        self.set_transient_for(parent)
        self.set_modal(True)

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
        view.set_displayed_row(gaupol.util.tree_row_to_path(0))
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
        view.set_displayed_row(gaupol.util.tree_row_to_path(0))
        renderer = Gtk.CellRendererText()
        self._newline_combo.pack_start(renderer, expand=True)
        self._newline_combo.add_attribute(renderer, "text", 0)

    def _init_values(self):
        """Initialize default values for widgets."""
        # Suggest format, encoding and newlines to match
        # those from the first page to consider.
        pages = self._get_pages()
        file = pages[0].project.main_file
        self.set_directory(os.path.dirname(file.path))
        self.set_format(file.format)
        self.set_encoding(file.encoding)
        self.set_newline(file.newline)
        self.set_framerate(gaupol.conf.editor.framerate)
        visible = len(set(self._modes)) > 1
        self._framerate_combo.set_visible(visible)
        self._framerate_label.set_visible(visible)

    def _on_format_combo_changed(self, *args):
        """Change the extension of the current filename."""
        format = self.get_format()
        modes = list(self._modes) + [format.mode]
        visible = len(set(modes)) > 1
        self._framerate_combo.set_visible(visible)
        self._framerate_label.set_visible(visible)

    def _on_response(self, dialog, response):
        """Save default values for widgets."""
        gaupol.conf.file.encoding = self.get_encoding()
        gaupol.conf.file.format = self.get_format()
        gaupol.conf.file.newline = self.get_newline()
        gaupol.conf.editor.framerate = self.get_framerate()
        if response != Gtk.ResponseType.OK: return
        gaupol.util.set_cursor_busy(self._dialog)
        self._save_all_documents_as()
        gaupol.util.set_cursor_normal(self._dialog)

    @aeidon.deco.silent(gaupol.Default)
    def _save_all_documents_as(self):
        """Save all documents with selected properties."""
        pages = self._get_pages()
        files = [None for x in pages]
        for i, page in enumerate(pages):
            if self._framerate_combo.get_visible():
                # Set framerate to the selected one.
                framerate = self.get_framerate()
                self.application.set_current_page(page)
                action = self.application.get_action("set-framerate")
                action.activate(str(framerate))
            path = os.path.basename(page.project.main_file.path)
            path = aeidon.util.replace_extension(path, self.get_format())
            path = os.path.join(self.get_directory(), path)
            files[i] = aeidon.files.new(self.get_format(),
                                        path,
                                        self.get_encoding(),
                                        self.get_newline())

        if sum(os.path.isfile(x.path) for x in files) > 0:
            self._show_overwrite_question_dialog(files, self.get_directory())
        for i, page in enumerate(pages):
            self.application.save_main_as(page, files[i])

    def set_directory(self, path):
        """Set the selected directory."""
        return self._filechooser_button.set_filename(path)

    def set_format(self, format):
        """Set the selected format."""
        if format is None: return
        self._format_combo.set_active(format)

    def set_framerate(self, framerate):
        """Set the selected framerate."""
        if framerate is None: return
        self._framerate_combo.set_active(framerate)

    def set_newline(self, newline):
        """Set the selected newline."""
        if newline is None: return
        self._newline_combo.set_active(newline)

    def _show_overwrite_question_dialog(self, files, path):
        """Show a question dialog if about to overwrite files."""
        n = sum(os.path.isfile(x.path) for x in files)
        title = _("{:d} of the files to be saved already exist. Do you want to replace them?").format(n)
        message = _('The files already exist in "{}". Replacing them will overwrite their contents.').format(path)
        dialog = gaupol.QuestionDialog(self._dialog, title, message)
        dialog.add_button(_("_Cancel"), Gtk.ResponseType.NO)
        dialog.add_button(_("_Replace"), Gtk.ResponseType.YES)
        dialog.set_default_response(Gtk.ResponseType.YES)
        response = gaupol.util.flash_dialog(dialog)
        gaupol.util.raise_default(response != Gtk.ResponseType.YES)
