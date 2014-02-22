# -*- coding: utf-8 -*-

# Copyright (C) 2005-2010,2013 Osmo Salomaa
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

"""Saving documents."""

import aeidon
import gaupol
import os
_ = aeidon.i18n._

from gi.repository import Gtk


class SaveAgent(aeidon.Delegate):

    """Saving documents."""

    @aeidon.deco.export
    def _on_save_all_documents_activate(self, *args):
        """Save all open documents."""
        silent = aeidon.deco.silent(gaupol.Default)
        save_main = silent(self.save_main)
        save_tran = silent(self.save_translation)
        for page in self.pages:
            save_main(page)
            if page.project.tran_changed is not None:
                save_tran(page)
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

    def _save_document(self, page, doc, file=None):
        """
        Save `doc` of `page` to `file`.

        Raise :exc:`gaupol.Default` if saving failed.
        """
        file = file or page.project.get_file(doc)
        gaupol.util.set_cursor_busy(self.window)
        try:
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

    def _select_file(self, title, page, file=None):
        """
        Select a file and return a :class:`aeidon.SubtitleFile`.

        Raise :exc:`gaupol.Default` if cancelled.
        """
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
            action = self.get_framerate_action(framerate)
            action.set_active(True)
        gaupol.util.iterate_main()
        return aeidon.files.new(format, path, encoding, newline)

    def _show_encoding_error_dialog(self, basename, codec):
        """Show an error dialog after failing to encode file."""
        codec = aeidon.encodings.code_to_name(codec)
        title = _('Failed to encode file "{basename}" '
            'with codec "{codec}"').format(**locals())
        message = _("Please try to save the file with "
            "a different character encoding.")
        dialog = gaupol.ErrorDialog(self.window, title, message)
        dialog.add_button(Gtk.STOCK_OK, Gtk.ResponseType.OK)
        gaupol.util.flash_dialog(dialog)

    def _show_io_error_dialog(self, basename, message):
        """Show an error dialog after failing to write file."""
        title = _('Failed to save file "{}"').format(basename)
        dialog = gaupol.ErrorDialog(self.window, title, message)
        dialog.add_button(Gtk.STOCK_OK, Gtk.ResponseType.OK)
        gaupol.util.flash_dialog(dialog)

    @aeidon.deco.export
    def save_main(self, page):
        """
        Save the main document of `page`.

        Raise :exc:`gaupol.Default` if cancelled or saving failed.
        """
        if (page.project.main_file is None or
            page.project.main_file.path is None or
            page.project.main_file.encoding is None):
            return self.save_main_as(page)

        self._save_document(page, aeidon.documents.MAIN)

    @aeidon.deco.export
    def save_main_as(self, page, file=None):
        """
        Save the main document of `page` to a selected file.

        If `file` is ``None`` show a filechooser dialog.
        Raise :exc:`gaupol.Default` if cancelled or saving failed.
        """
        if file is None:
            file = self._select_file(_("Save As"),
                                     page,
                                     page.project.main_file)

        self._save_document(page, aeidon.documents.MAIN, file)
        self.add_to_recent_files(page.project.main_file.path,
                                 page.project.main_file.format,
                                 aeidon.documents.MAIN)

        basename = os.path.basename(page.project.main_file.path)
        self.flash_message(_('Saved main document as "{}"')
                           .format(basename))

    @aeidon.deco.export
    def save_translation(self, page):
        """
        Save the translation document of `page`.

        Raise :exc:`gaupol.Default` if cancelled or saving failed.
        """
        if (page.project.tran_file is None or
            page.project.tran_file.path is None or
            page.project.tran_file.encoding is None):
            return self.save_translation_as(page)

        self._save_document(page, aeidon.documents.TRAN)

    @aeidon.deco.export
    def save_translation_as(self, page, file=None):
        """
        Save the translation document of `page` to a selected file.

        If `file` is ``None`` show a filechooser dialog.
        Raise :exc:`gaupol.Default` if cancelled or saving failed.
        """
        if file is None:
            file = self._select_file(_("Save Translation As"),
                                     page,
                                     page.project.tran_file)

        self._save_document(page, aeidon.documents.TRAN, file)
        self.add_to_recent_files(page.project.tran_file.path,
                                 page.project.tran_file.format,
                                 aeidon.documents.TRAN)

        basename = os.path.basename(page.project.tran_file.path)
        self.flash_message(_('Saved translation document as "{}"')
                           .format(basename))
