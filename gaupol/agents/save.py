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

"""Saving documents."""

import aeidon
import gaupol
import os

from aeidon.i18n   import _
from gi.repository import Gtk


class SaveAgent(aeidon.Delegate):

    """Saving documents."""

    @aeidon.deco.export
    def _on_save_all_documents_activate(self, *args):
        """Save all open documents."""
        for page in self.pages:
            with aeidon.util.silent(gaupol.Default):
                self.save_main(page)
            if page.project.tran_changed is not None:
                with aeidon.util.silent(gaupol.Default):
                    self.save_translation(page)
        self.update_gui()

    @aeidon.deco.export
    def _on_save_all_documents_as_activate(self, *args):
        """Save all open documents with different properties."""
        modes = []
        for page in self.pages:
            if page.project.main_file is not None:
                modes.append(page.project.main_file.mode)
        dialog = gaupol.MultiSaveDialog(self.window, self, modes)
        gaupol.util.flash_dialog(dialog)
        self.update_gui()

    @aeidon.deco.export
    @aeidon.deco.silent(gaupol.Default)
    def _on_save_main_document_activate(self, *args):
        """Save the current main document."""
        page = self.get_current_page()
        self.save_main(page)
        self.update_gui()

    @aeidon.deco.export
    @aeidon.deco.silent(gaupol.Default)
    def _on_save_main_document_as_activate(self, *args):
        """Save the current main document with a different name."""
        page = self.get_current_page()
        self.save_main_as(page)
        self.update_gui()

    @aeidon.deco.export
    @aeidon.deco.silent(gaupol.Default)
    def _on_save_translation_document_activate(self, *args):
        """Save the current translation document."""
        page = self.get_current_page()
        self.save_translation(page)
        self.update_gui()

    @aeidon.deco.export
    @aeidon.deco.silent(gaupol.Default)
    def _on_save_translation_document_as_activate(self, *args):
        """Save the current translation document with a different name."""
        page = self.get_current_page()
        self.save_translation_as(page)
        self.update_gui()

    @aeidon.deco.export
    def save(self, page, doc):
        """Save `doc` of `page` to file."""
        if doc == aeidon.documents.MAIN:
            return self.save_main(page)
        if doc == aeidon.documents.TRAN:
            return self.save_translation(page)
        raise ValueError("Invalid document: {!r}"
                         .format(doc))

    def _save_document(self, page, doc, file=None):
        """Save document to `file` or raise :exc:`gaupol.Default`."""
        try:
            file = file or page.project.get_file(doc)
            gaupol.util.set_cursor_busy(self.window)
            return page.project.save(doc, file)
        except IOError as error:
            gaupol.util.set_cursor_normal(self.window)
            basename = os.path.basename(file.path)
            self._show_io_error_dialog(basename, str(error))
        except UnicodeError:
            gaupol.util.set_cursor_normal(self.window)
            basename = os.path.basename(file.path)
            self._show_encoding_error_dialog(basename, file.encoding)
        finally:
            gaupol.util.set_cursor_normal(self.window)
        raise gaupol.Default

    @aeidon.deco.export
    def save_main(self, page):
        """Save the main document of `page` to file."""
        if (page.project.main_file is None or
            page.project.main_file.path is None or
            page.project.main_file.encoding is None):
            return self.save_main_as(page)
        self._save_document(page, aeidon.documents.MAIN)
        self.emit("page-saved", self, page)

    @aeidon.deco.export
    def save_main_as(self, page, file=None):
        """Save the main document of `page` to a selected file."""
        if file is None:
            file = page.project.main_file
            file = self._select_file(_("Save As"), page, file)
        self._save_document(page, aeidon.documents.MAIN, file)
        self.emit("page-saved", self, page)
        path = page.project.main_file.path
        format = page.project.main_file.format
        self.add_to_recent_files(path, format, aeidon.documents.MAIN)
        self.flash_message(_('Saved main document as "{}"')
                           .format(os.path.basename(path)))

    @aeidon.deco.export
    def save_translation(self, page):
        """Save the translation document of `page` to file."""
        if (page.project.tran_file is None or
            page.project.tran_file.path is None or
            page.project.tran_file.encoding is None):
            return self.save_translation_as(page)
        self._save_document(page, aeidon.documents.TRAN)
        self.emit("page-saved", self, page)

    @aeidon.deco.export
    def save_translation_as(self, page, file=None):
        """Save the translation document of `page` to a selected file."""
        if file is None:
            file = page.project.tran_file
            file = self._select_file(_("Save Translation As"), page, file)
        self._save_document(page, aeidon.documents.TRAN, file)
        self.emit("page-saved", self, page)
        path = page.project.tran_file.path
        format = page.project.tran_file.format
        self.add_to_recent_files(path, format, aeidon.documents.TRAN)
        self.flash_message(_('Saved translation document as "{}"')
                           .format(os.path.basename(path)))

    def _select_file(self, title, page, file=None):
        """Select a file to save or raise :exc:`gaupol.Default`."""
        gaupol.util.set_cursor_busy(self.window)
        mode = page.project.get_mode()
        dialog = gaupol.SaveDialog(self.window, title, mode)
        if file is not None:
            dialog.set_name(file.path)
            dialog.set_format(file.format)
            dialog.set_encoding(file.encoding)
            dialog.set_newline(file.newline)
            dialog.set_framerate(page.project.framerate)
        gaupol.util.set_cursor_normal(self.window)
        response = gaupol.util.run_dialog(dialog)
        format = dialog.get_format()
        path = dialog.get_filename()
        encoding = dialog.get_encoding()
        newline = dialog.get_newline()
        framerate = dialog.get_framerate()
        dialog.destroy()
        if response != Gtk.ResponseType.OK:
            raise gaupol.Default
        if format.mode != mode:
            # Set framerate to the selected one.
            self.set_current_page(page)
            action = self.get_action("set-framerate")
            action.activate(str(framerate))
        gaupol.util.iterate_main()
        return aeidon.files.new(format, path, encoding, newline)

    def _show_encoding_error_dialog(self, basename, codec):
        """Show an error dialog after failing to encode file."""
        codec = aeidon.encodings.code_to_name(codec)
        title = _('Failed to encode file "{basename}" with codec "{codec}"').format(**locals())
        message = _("Please try to save the file with a different character encoding.")
        dialog = gaupol.ErrorDialog(self.window, title, message)
        dialog.add_button(_("_OK"), Gtk.ResponseType.OK)
        dialog.set_default_response(Gtk.ResponseType.OK)
        gaupol.util.flash_dialog(dialog)

    def _show_io_error_dialog(self, basename, message):
        """Show an error dialog after failing to write file."""
        title = _('Failed to save file "{}"').format(basename)
        dialog = gaupol.ErrorDialog(self.window, title, message)
        dialog.add_button(_("_OK"), Gtk.ResponseType.OK)
        dialog.set_default_response(Gtk.ResponseType.OK)
        gaupol.util.flash_dialog(dialog)
