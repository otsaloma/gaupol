# Copyright (C) 2005-2009 Osmo Salomaa
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

import gaupol
import gtk
import os
_ = aeidon.i18n._


class SaveAgent(aeidon.Delegate):

    """Saving documents."""

    def _get_main_props(self, page):
        """Return the properties of the main file of page's project.

        Return path, format, encoding, newline.
        """
        props = [None, None, None, None]
        if page.project.main_file is not None:
            props[0] = page.project.main_file.path
            props[1] = page.project.main_file.format
            props[2] = page.project.main_file.encoding
            props[3] = page.project.main_file.newline
        return tuple(props)

    def _get_translation_props(self, page):
        """Return the properties of the translation file of page's project.

        Return path, format, encoding, newline.
        """
        props = [None, None, None, None]
        if page.project.tran_file is not None:
            props[0] = page.project.tran_file.path
            props[1] = page.project.tran_file.format
            props[2] = page.project.tran_file.encoding
            props[3] = page.project.tran_file.newline
        elif page.project.main_file is not None:
            props[1] = page.project.main_file.format
            props[2] = page.project.main_file.encoding
            props[3] = page.project.main_file.newline
        return tuple(props)

    def _save_document(self, page, doc, props):
        """Save document to a file defined by properties.

        props is a sequence of path, format, encoding, newline.
        Raise Default if an error occurs and document is not saved.
        """
        gaupol.util.set_cursor_busy(self.window)
        basename = os.path.basename(props[0])
        try: return page.project.save(doc, props)
        except IOError, (no, message):
            gaupol.util.set_cursor_normal(self.window)
            self._show_io_error_dialog(basename, message)
        except UnicodeError:
            gaupol.util.set_cursor_normal(self.window)
            self._show_encoding_error_dialog(basename, props[2])
        finally:
            gaupol.util.set_cursor_normal(self.window)
        raise gaupol.Default

    def _select_file(self, title, props):
        """Select a file and return path, format, encoding, newline.

        Raise Default if cancelled and file should not be opened.
        """
        path, format, encoding, newline = props
        props = [None, None, None, None]
        gaupol.util.set_cursor_busy(self.window)
        dialog = gaupol.SaveDialog(self.window, title)
        dialog.set_name(path)
        dialog.set_format(format)
        dialog.set_encoding(encoding)
        dialog.set_newline(newline)
        gaupol.util.set_cursor_normal(self.window)
        response = self.run_dialog(dialog)
        props[0] = dialog.get_filename()
        props[1] = dialog.get_format()
        props[2] = dialog.get_encoding()
        props[3] = dialog.get_newline()
        dialog.destroy()
        if response != gtk.RESPONSE_OK:
            raise gaupol.Default
        gaupol.util.iterate_main()
        return tuple(props)

    def _show_encoding_error_dialog(self, basename, codec):
        """Show an error dialog after failing to encode file."""

        codec = aeidon.encodings.code_to_name(codec)
        title = _('Failed to encode file "%(basename)s" '
            'with codec "%(codec)s"') % locals()
        message = _("Please try to save the file with "
            "a different character encoding.")
        dialog = gaupol.ErrorDialog(self.window, title, message)
        dialog.add_button(gtk.STOCK_OK, gtk.RESPONSE_OK)
        self.flash_dialog(dialog)

    def _show_io_error_dialog(self, basename, message):
        """Show an error dialog after failing to write file."""

        title = _('Failed to save file "%s"') % basename
        message = _("%s.") % message
        dialog = gaupol.ErrorDialog(self.window, title, message)
        dialog.add_button(gtk.STOCK_OK, gtk.RESPONSE_OK)
        self.flash_dialog(dialog)

    def on_save_all_documents_activate(self, *args):
        """Save all open documents."""

        silent = aeidon.deco.silent(gaupol.Default)
        save_main_document = silent(self.save_main_document)
        save_tran_document = silent(self.save_translation_document)
        for page in self.pages:
            save_main_document(page)
            if page.project.tran_changed is not None:
                save_tran_document(page)
        self.flash_message(_("Saved all open documents"))
        self.update_gui()

    @aeidon.deco.silent(gaupol.Default)
    def on_save_main_document_activate(self, *args):
        """Save the current main document."""

        page = self.get_current_page()
        self.save_main_document(page)
        self.update_gui()

    @aeidon.deco.silent(gaupol.Default)
    def on_save_main_document_as_activate(self, *args):
        """Save the current main document with a different name."""

        page = self.get_current_page()
        self.save_main_document_as(page)
        self.update_gui()

    @aeidon.deco.silent(gaupol.Default)
    def on_save_translation_document_activate(self, *args):
        """Save the current translation document."""

        page = self.get_current_page()
        self.save_translation_document(page)
        self.update_gui()

    @aeidon.deco.silent(gaupol.Default)
    def on_save_translation_document_as_activate(self, *args):
        """Save the current translation document with a different name."""

        page = self.get_current_page()
        self.save_translation_document_as(page)
        self.update_gui()

    def save_main_document(self, page):
        """Save the main document of page.

        Raise Default if cancelled or failed and document is not saved.
        """
        props = self._get_main_props(page)
        if None in props:
            return self.save_main_document_as(page)
        self._save_document(page, aeidon.documents.MAIN, props)
        self.flash_message(_("Saved main document"))

    def save_main_document_as(self, page):
        """Save the main document of page to a selected file.

        Raise Default if cancelled or failed and document is not saved.
        """
        props = list(self._get_main_props(page))
        props[0] = props[0] or page.get_main_basename()
        props = self._select_file(_("Save As"), props)
        self._save_document(page, aeidon.documents.MAIN, props)
        format = page.project.main_file.format
        self.add_to_recent_files(props[0], format, aeidon.documents.MAIN)
        message = _('Saved main document as "%s"')
        self.flash_message(message % os.path.basename(props[0]))

    def save_translation_document(self, page):
        """Save the translation document of page.

        Raise Default if cancelled or failed and document is not saved.
        """
        props = self._get_translation_props(page)
        if None in props:
            return self.save_translation_document_as(page)
        self._save_document(page, aeidon.documents.TRAN, props)
        self.flash_message(_("Saved translation document"))

    def save_translation_document_as(self, page):
        """Save the translation document of page to a selected file.

        Raise Default if cancelled or failed and document is not saved.
        """
        props = list(self._get_translation_props(page))
        props[0] = props[0] or page.get_translation_basename()
        props = self._select_file(_("Save Translation As"), props)
        self._save_document(page, aeidon.documents.TRAN, props)
        format = page.project.tran_file.format
        self.add_to_recent_files(props[0], format, aeidon.documents.TRAN)
        message = _('Saved translation document as "%s"')
        self.flash_message(message % os.path.basename(props[0]))
